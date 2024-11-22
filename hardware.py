import cv2
from pyzbar.pyzbar import decode
import pygame
import time
import threading
from datetime import datetime
import os
import arms
from robot_hat import Servo
import subprocess
import sys
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 16        # number of leds
LED_PIN = 10          # GPIO18,spi 10
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 30  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Define arms motion
servo1 = Servo("P0")
servo1.angle(0)

def finish_arms():
    for i in range(0,12,1):
        servo1.angle(i)
        time.sleep(0.01)
    for i in range(15,-15,-1):
        servo1.angle(i)
        time.sleep(0.01)
    for i in range(-15,15,1):
        servo1.angle(i)
        time.sleep(0.01)
    for i in range(15,0,-1):
        servo1.angle(i)
        time.sleep(0.01)

def listen():
    for i in range(0,15,1):
        servo1.angle(i)
        time.sleep(0.03)
    time.sleep(1)
    for i in range(15,-15,-1):
        servo1.angle(i)
        time.sleep(0.03)
    time.sleep(1)
    for i in range(-15,0,1):
        servo1.angle(i)
        time.sleep(0.03)

def wrong():
    for i in range(0,45,1):
        servo1.angle(i)
        time.sleep(0.01)
    for i in range(45,-45,-1):
        servo1.angle(i)
        time.sleep(0.01)
    for i in range(-45,45,1):
        servo1.angle(i)
        time.sleep(0.01)
    for i in range(45,0,-1):
        servo1.angle(i)
        time.sleep(0.01)

# Global variable to store the original stdout and the log file object
global original_stdout, log_file
# Save the original stdout so you can restore it later
original_stdout = sys.stdout
# Redirect stdout to a log file
log_filename = f"/home/Tina/Downloads/family-robot/logs/log_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
log_file = open(log_filename, 'w')
sys.stdout = log_file

# Initialize pygame mixer
pygame.mixer.init()

# Dictionary to track which QR codes have been scanned
scanned_qrcodes = {
    "qrcode_1": False, # teeth and face
    "qrcode_2": False, # pajamas
    "qrcode_3": False # story
}
qrcode_5_count = 0
diary_questions = ["diary1.wav","diary2.wav","diary3.wav","diary4.wav","diary5.wav","diary6.wav"]

def play_sound(sound_file):
    """Play the loaded sound."""
    os.system(f"sudo aplay /home/Tina/Downloads/family-robot/sound/{sound_file}")

def scan_qr_code(frame):
    """Scan the frame for QR codes and return the data."""
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        return obj.data.decode('utf-8')
    return None

def check_all_scanned():
    """Check if all QR codes 1, 2, and 3 have been scanned."""
    return all(scanned_qrcodes.values())


            

#light strip
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def lightup(strip,led_index, color):
    strip.setPixelColor(led_index,color)
    strip.show()


# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 10)

# Generate filename based on current timestamp
current_time = datetime.now().strftime('%Y%m%d%H%M')
video_filename = f'/home/Tina/Downloads/family-robot/test video/{current_time}.avi'
audio_filename = f'/home/Tina/Downloads/family-robot/test audio/{current_time}.wav'

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
out = cv2.VideoWriter(video_filename, fourcc, 10.0, (1280, 720))

def video_recorder():
    """Thread function to continuously record video."""
    global out
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Write the frame to the video file
            out.write(frame)
            # out.flush()  # immedeiate save

            # Display the resulting frame
            cv2.imshow('frame', frame)
    
    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # Release the video capture and writer
        cap.release()
        out.release()
        cv2.destroyAllWindows()


def audio_recorder():
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

     # Check for errors
    stderr = audio_process.communicate()[1]
    if stderr:
        print(f"Audio recording error: {stderr.decode()}")

