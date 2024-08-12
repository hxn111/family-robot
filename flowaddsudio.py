import cv2
from pyzbar.pyzbar import decode
import pygame
import time
import threading
from datetime import datetime
import os
import hat_arms
import subprocess

# Initialize pygame mixer
pygame.mixer.init()

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 10)

# Generate filename based on current timestamp
current_time = datetime.now().strftime('%Y%m%d%H%M')
video_filename = f'./test video/{current_time}.avi'
audio_filename = f'./test audio/{current_time}.wav'

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
out = cv2.VideoWriter(video_filename, fourcc, 10.0, (1280, 720))

def play_sound(sound_file):
    """Play the loaded sound."""
    os.system(f"sudo aplay /home/Tina/Downloads/family-robot/sound/{sound_file}")

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

        # Take a screenshot every 2 seconds
        if int(time.time()) % 2 == 0:
            screenshot_filename = f'./test pic/{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
            cv2.imwrite(screenshot_filename, frame)

            # Scan the screenshot for QR codes
            qr_data = scan_qr_code(frame)
            if qr_data:
                print(f"QR Code detected: {qr_data}")
                
                if qr_data == "qr_code_1":
                    print("Happy mode triggered")
                    threading.Thread(target=play_sound, args=("teeth.wav",)).start()
                    hat_arms.happy_mode()
                elif qr_data == "qr_code_2":
                    print("Sad mode triggered")
            else:
                print("No QR code")

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

def start_audio_recording():
    """Start continuous audio recording."""
    global audio_process
    audio_process = subprocess.Popen([
        'arecord',
        '-D', 'plughw:2,0',  # Specify the device
        '-f', 'cd',  # CD quality
        '-r', '44100',  # Sample rate
        '-c', '1',  # Mono audio
        '-t', 'wav',  # Output file type
        '-q',  # Quiet mode
        audio_filename  # Output file name
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    # Start the QR code scanning thread
    threading.Thread(target=qr_code_scanner, daemon=True).start()

    # Start the video recording thread
    threading.Thread(target=video_recorder, daemon=True).start()

    # Start the continuous audio recording
    start_audio_recording()

except KeyboardInterrupt:
    pass
finally:
    # Clean up GPIO and stop PWM signals
    # hat_arms.cleanup()

    # Terminate the audio recording process
    if 'audio_process' in globals():
        audio_process.terminate()

    # When everything is done, release the capture, video writer, and close windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()
