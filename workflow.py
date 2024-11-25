import cv2
import time
import threading
from multiprocessing import Process
from datetime import datetime
import sys
import os
from rpi_ws281x import Color
import hardware
from utils import decode_ndarr
from config import (
    PICS_DIR,
    redis_client, R_KEY_LAST_FRAME,
)

# Generate filename based on current timestamp
current_time = datetime.now().strftime('%Y%m%d%H%M')

qrcode_5_count = 0


def qr_code_scanner():
    """Thread function to continuously scan QR codes."""
    while True:
        last_shot_taken = 0
        # Take a screenshot every 3 seconds
        if time.time() - last_shot_taken > 3:
            last_shot_taken = time.time()
            # read last frame from redis 
            frame = redis_client.get(R_KEY_LAST_FRAME)
            if frame:
                frame = decode_ndarr(frame)
                screenshot_filename = os.path.join(
                    PICS_DIR, f'{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg')
                # Don't necessarily need these
                cv2.imwrite(screenshot_filename, frame)
                # scan QR codes
                routine_flow(frame)
            time.sleep(0.5)


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
                hardware.listen()
                qrcode_5_count = 1 
            else:
                if not hardware.scanned_qrcodes["qrcode_1"]:
                    print("QR Code 1 missing at ",current_time)
                    threading.Thread(target=hardware.play_sound, args=("reminder1.WAV",)).start()
                    hardware.wrong()
                    hardware.lightup(hardware.strip, 1, Color(255,0,0))
                    time.sleep(6)
                    return
                if not hardware.scanned_qrcodes["qrcode_2"]:
                    print("QR Code 2 missing at ",current_time)
                    threading.Thread(target=hardware.play_sound, args=("reminder2.WAV",)).start()
                    hardware.wrong()
                    hardware.lightup(hardware.strip, 2, Color(255,0,0))
                    time.sleep(6)
                    return
                if not hardware.scanned_qrcodes["qrcode_3"]:
                    print("QR Code 3 missing at ",current_time)
                    threading.Thread(target=hardware.play_sound, args=("reminder3.WAV",)).start()
                    hardware.wrong()
                    hardware.lightup(hardware.strip, 3, Color(255,0,0))
                    time.sleep(6)
                    return
                
        elif qr_data == "qrcode_5":
            if qrcode_5_count > 0 & qrcode_5_count <= 6:
                print("Diary ",qrcode_5_count," is recording at ",current_time)
                sound_to_play = hardware.diary_questions[qrcode_5_count-1]
                threading.Thread(target=hardware.play_sound, args=(sound_to_play,)).start()
                hardware.listen()
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
        # print(qrcode_5_count)
        sys.stdout.flush()
        time.sleep(8)

    else:
        pass


try:
    # Start the video recording subprocess
    proc_video = Process(target=hardware.video_recorder, daemon=True)
    proc_video.start()
    # threading.Thread(target=hardware.video_recorder, daemon=True).start()

    # Start the continuous audio recording
    threading.Thread(target=hardware.audio_recorder, daemon=True).start()

    # Start the QR code scanning thread
    qr_code_scanner()


except KeyboardInterrupt:
    pass
finally:
    # Terminate the audio recording process
    if 'audio_process' in globals():
        hardware.audio_process.terminate()
    # Ensure that video recording is finalized properly
    proc_video.terminate()
    
    # Restore the original stdout
    sys.stdout = hardware.original_stdout
    # Close the log file
    if 'log_file' in globals():
        hardware.log_file.close()

    # When everything is done, close windows
    cv2.destroyAllWindows()
    hardware.colorWipe(hardware.strip, Color(0, 0, 0), 10)
