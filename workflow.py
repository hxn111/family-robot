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
import hardware

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

def routine_flow(frame):
    """ reminder and diary routine """
    qr_data = hardware.scan_qr_code(frame)
    if qr_data:
        print(f"QR Code detected: {qr_data}")
        
        if qr_data == "qrcode_1":
            print("teeth brushing triggered at ",current_time)
            threading.Thread(target=hardware.play_sound, args=("finished1.WAV",)).start()
            hardware.finish_arms()
            hardware.lightup(hardware.strip, 1, Color(255,255,0))
            hardware.strip.show()
            hardware.scanned_qrcodes["qrcode_1"] = True
        
        elif qr_data == "qrcode_2":
            print("pajamas triggered at ",current_time)
            threading.Thread(target=hardware.play_sound, args=("finished2.WAV",)).start()
            hardware.finish_arms()
            hardware.lightup(hardware.strip, 2, Color(255,255,0))
            hardware.strip.show()
            hardware.scanned_qrcodes["qrcode_2"] = True
        
        elif qr_data == "qrcode_3":
            print("story triggered at ",current_time)
            threading.Thread(target=hardware.play_sound, args=("finished3.WAV",)).start()
            hardware.finish_arms()
            hardware.lightup(hardware.strip, 3, Color(255,255,0))
            hardware.strip.show()
            hardware.scanned_qrcodes["qrcode_3"] = True
        
        elif qr_data == "qrcode_4":
            if hardware.check_all_scanned():
                print("Playing diary at ",current_time)
                threading.Thread(target=hardware.play_sound, args=("diary1.WAV",)).start()
                qrcode_5_count = 1 
            else:
                if not hardware.scanned_qrcodes["qrcode_1"]:
                    print("QR Code 1 missing at ",current_time)
                    threading.Thread(target=hardware.play_sound, args=("reminder1.WAV",)).start()
                    hardware.lightup(hardware.strip, 1, Color(255,0,0))
                    time.sleep(6)
                    return
                if not hardware.scanned_qrcodes["qrcode_2"]:
                    print("QR Code 2 missing at ",current_time)
                    threading.Thread(target=hardware.play_sound, args=("reminder2.WAV",)).start()
                    hardware.lightup(hardware.strip, 2, Color(255,0,0))
                    time.sleep(6)
                    return
                if not hardware.scanned_qrcodes["qrcode_3"]:
                    print("QR Code 3 missing at ",current_time)
                    threading.Thread(target=hardware.play_sound, args=("reminder3.WAV",)).start()
                    hardware.lightup(hardware.strip, 3, Color(255,0,0))
                    time.sleep(6)
                    return
                
        elif qr_data == "qrcode_5":
            if qrcode_5_count > 0 & qrcode_5_count <= 6:
                print("Diary ",qrcode_5_count," is recording at ",current_time)
                sound_to_play = hardware.diary_questions[qrcode_5_count-1]
                threading.Thread(target=hardware.play_sound, args=(sound_to_play,)).start()
                hardware.lightup(hardware.strip, qrcode_5_count+3, Color(255,255,0))
                qrcode_5_count += 1
                if qrcode_5_count == 6:
                    hardware.colorWipe(hardware.strip,Color(255,255,0),20)
                
            elif qrcode_5_count == 0:
                print("Haven't finished routines at ",current_time)
                threading.Thread(target=hardware.play_sound, args=("instructions.WAV",)).start()
            elif qrcode_5_count > 6:
                print("All final sounds have been played at ",current_time)
                threading.Thread(target=hardware.play_sound, args=("ending.WAV",)).start()
        
        sys.stdout.flush()
        time.sleep(8)

    else:
        pass


try:
    # Start the video recording thread
    threading.Thread(target=hardware.video_recorder, daemon=True).start()

    # Start the continuous audio recording
    threading.Thread(target=hardware.audio_recorder, daemon=True).start()

    # Start the QR code scanning thread
    hardware.qr_code_scanner()


except KeyboardInterrupt:
    pass
finally:
    # Terminate the audio recording process
    if 'audio_process' in globals():
        hardware.audio_process.terminate()
    # Ensure that video recording is finalized properly
    if 'out' in globals():
        out.release()
    # Release the video capture and close any OpenCV windows
    if 'cap' in globals():
        cap.release()
    # Restore the original stdout
    sys.stdout = hardware.original_stdout
    # Close the log file
    if 'log_file' in globals():
        hardware.log_file.close()

    # When everything is done, close windows
    cv2.destroyAllWindows()
    hardware.colorWipe(hardware.strip, Color(0, 0, 0), 10)
