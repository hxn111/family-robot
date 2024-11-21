import cv2
from pyzbar.pyzbar import decode
import pygame
import time
import threading
from datetime import datetime
import os
import hat_arms
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
# Intialize the library (must be called once before other functions).
strip.begin()

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
diary_questions = ["diary1.WAV","diary2.WAV","diary3.WAV","diary4.WAV","diary5.WAV","diary6.WAV"]

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

def qr_code_scanner():
    """Thread function to continuously scan QR codes."""
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Take a screenshot every 2 seconds
        if int(time.time()) % 2 == 0:
            screenshot_filename = f'/home/Tina/Downloads/family-robot/test pic/{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
            cv2.imwrite(screenshot_filename, frame)

            # scan QR codes
            routine_flow(frame)
            
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def lightup(strip,led_index, color):
    strip.setPixelColor(led_index,color)
    strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def routine_flow(frame):
    """ reminder and diary routine """
    qr_data = scan_qr_code(frame)
    global qrcode_5_count
    if qr_data:
        print(f"QR Code detected: {qr_data}")
        
        if qr_data == "qrcode_1":
            print("teeth brushing triggered at ",current_time)
            threading.Thread(target=play_sound, args=("finished1.WAV",)).start()
            hat_arms.finish()
            lightup(strip, 1, Color(0,255,0))
            strip.show()
            scanned_qrcodes["qrcode_1"] = True
        
        elif qr_data == "qrcode_2":
            print("pajamas triggered at ",current_time)
            threading.Thread(target=play_sound, args=("finished2.WAV",)).start()
            hat_arms.finish()
            lightup(strip, 2, Color(0,255,0))
            strip.show()
            scanned_qrcodes["qrcode_2"] = True
        
        elif qr_data == "qrcode_3":
            print("story triggered at ",current_time)
            threading.Thread(target=play_sound, args=("finished3.WAV",)).start()
            hat_arms.finish()
            lightup(strip, 3, Color(0,255,0))
            strip.show()
            scanned_qrcodes["qrcode_3"] = True
        
        elif qr_data == "qrcode_4":
            if check_all_scanned():
                print("Playing diary at ",current_time)
                threading.Thread(target=play_sound, args=("diary1.WAV",)).start()
                hat_arms.listen()
                qrcode_5_count = 1
                
            else:
                if not scanned_qrcodes["qrcode_1"]:
                    print("QR Code 1 missing at ",current_time)
                    threading.Thread(target=play_sound, args=("reminder1.WAV",)).start()
                    hat_arms.wrong()
                    lightup(strip, 1, Color(255,0,0))
                    time.sleep(6)
                    return
                if not scanned_qrcodes["qrcode_2"]:
                    print("QR Code 2 missing at ",current_time)
                    threading.Thread(target=play_sound, args=("reminder2.WAV",)).start()
                    hat_arms.wrong()
                    lightup(strip, 2, Color(255,0,0))
                    time.sleep(6)
                    return
                if not scanned_qrcodes["qrcode_3"]:
                    print("QR Code 3 missing at ",current_time)
                    threading.Thread(target=play_sound, args=("reminder3.WAV",)).start()
                    hat_arms.wrong()
                    lightup(strip, 3, Color(255,0,0))
                    time.sleep(6)
                    return
        elif qr_data == "qrcode_5":
            if qrcode_5_count > 0 & qrcode_5_count <= 6:
                print("Diary ",qrcode_5_count," is recording at ",current_time)
                sound_to_play = diary_questions[qrcode_5_count]
                threading.Thread(target=play_sound, args=(sound_to_play,)).start()
                hat_arms.listen()
                lightup(strip, qrcode_5_count+3, Color(0,255,0))
                qrcode_5_count += 1
                if qrcode_5_count == 6:
                    colorWipe(strip,Color(255,255,0),20)

            elif qrcode_5_count == 0:
                print("Haven't finished routines at ",current_time)
                # threading.Thread(target=play_sound, args=("instructions.WAV",)).start()
            elif qrcode_5_count > 6:
                print("All final sounds have been played at ",current_time)
                threading.Thread(target=play_sound, args=("ending.WAV",)).start()
        print(qrcode_5_count)
        sys.stdout.flush()
        time.sleep(8)

    else:
        pass


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

try:
    # Start the video recording thread
    threading.Thread(target=video_recorder, daemon=True).start()

    # Start the continuous audio recording
    threading.Thread(target=audio_recorder, daemon=True).start()

    # Start the QR code scanning thread
    qr_code_scanner()



except KeyboardInterrupt:
    pass
finally:
    # Terminate the audio recording process
    if 'audio_process' in globals():
        audio_process.terminate()
    # Ensure that video recording is finalized properly
    if 'out' in globals():
        out.release()
    # Release the video capture and close any OpenCV windows
    if 'cap' in globals():
        cap.release()
    # Restore the original stdout
    sys.stdout = original_stdout
    # Close the log file
    if 'log_file' in globals():
        log_file.close()

    # When everything is done, close windows
    cv2.destroyAllWindows()
    colorWipe(strip, Color(0, 0, 0), 10)
