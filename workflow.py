import cv2
from pyzbar.pyzbar import decode
import pygame
import time
import arms  # Import the arms module

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

try:
    while True:
        # Capture frame-by-frame
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
                    arms.happy_mode()  # Call the happy_mode function
                elif qr_data == "qr_code_2":
                    arms.sad_mode()  # Call the sad_mode function
            else:
                print("No sound associated with this QR code")

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass
finally:
    # Clean up GPIO and stop PWM signals
    arms.cleanup()

# When everything is done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()
