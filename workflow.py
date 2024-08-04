import cv2
from pyzbar.pyzbar import decode
import pygame
import time
import threading
from datetime import datetime
import arms_moving

# Initialize pygame mixer
pygame.mixer.init()

# Dictionary mapping QR code data to sound files
qr_data_to_sound = {
    "qr_code_1": "sound/test.wav",
    # "qr_code_2": "sound/sound2.wav",
    # "qr_code_3": "sound/sound3.wav"
}

# Preload sounds
sounds = {data: pygame.mixer.Sound(sound_file) for data, sound_file in qr_data_to_sound.items()}

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 10)

# Generate filename based on current timestamp
current_time = datetime.now().strftime('%Y%m%d%H%M')
video_filename = f'{current_time}.avi'

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
out = cv2.VideoWriter(video_filename, fourcc, 10.0, (1280, 720))

def play_sound(sound):
    """Play the loaded sound."""
    sound.play()
    time.sleep(sound.get_length())  # Wait for the sound to finish

def scan_qr_code(frame):
    """Scan the frame for QR codes and return the data."""
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        return obj.data.decode('utf-8')
    return None

def qr_code_scanner():
    """Thread function to continuously scan QR codes."""
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale (optional but can improve accuracy)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Scan for QR codes
        qr_data = scan_qr_code(gray)
        if qr_data:
            print(f"QR Code detected: {qr_data}")
            if qr_data in sounds:
                play_sound(sounds[qr_data])
                if qr_data == "qr_code_1":
                    arms_moving.happy_mode()  # Call the happy_mode function
                elif qr_data == "qr_code_2":
                    arms_moving.sad_mode()  # Call the sad_mode function
            else:
                print("No sound associated with this QR code")

def video_recorder():
    """Thread function to continuously record video."""
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Write the frame to the video file
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

try:
    # Start QR code scanner thread
    scanner_thread = threading.Thread(target=qr_code_scanner, daemon=True)
    scanner_thread.start()

    # Run the video recorder function in the main thread
    video_recorder()

except KeyboardInterrupt:
    pass
finally:
    # Clean up GPIO and stop PWM signals
    arms_moving.cleanup()

    # When everything is done, release the capture, video writer, and close windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()