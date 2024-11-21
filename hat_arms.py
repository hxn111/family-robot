from robot_hat import Servo
import time

servo1 = Servo("P0")
servo2 = Servo("P4")

servo1.angle(0)
servo2.angle(0)

def happy_mode():
    for i in range(0,90,2):
        servo1.angle(i)
        servo2.angle(-i)
        time.sleep(0.01)

    for i in range(90,30,-1):
        servo1.angle(i)
        servo2.angle(-i)
        time.sleep(0.01)

    for i in range(30,90,1):
        servo1.angle(i)
        servo2.angle(-i)
        time.sleep(0.01)

    for i in range(90,30,-1):
        servo1.angle(i)
        servo2.angle(-i)
        time.sleep(0.01)

    for i in range(30,90,1):
        servo1.angle(i)
        servo2.angle(-i)
        time.sleep(0.01)

    for i in range(90,0,-1):
        servo1.angle(i)
        servo2.angle(-i)
        time.sleep(0.01)

def ready():
    # hi, are you ready?
    for i in range(0,90,1):
        servo1.angle(i)
        servo2.angle(-i)
        time.sleep(0.01)
    time.sleep(1)
    for i in range(90,0,-1):
        servo1.angle(i)
        servo2.angle(-i)
        time.sleep(0.01)

    for i in range(0,90,1):
        servo1.angle(i)
        time.sleep(0.01)
    time.sleep(2)
    for i in range(90,0,-1):
        servo1.angle(i)
        time.sleep(0.01)

def teeth():
    ready()

    for i in range(0,45,1):
        servo1.angle(i)
        time.sleep(0.01)
    for j in range(0,5):
        for i in range(45,-45,-1):
            servo1.angle(i)
            time.sleep(0.01)
        for i in range(-45,45,1):
            servo1.angle(i)
            time.sleep(0.01)
    for i in range(45,0,-1):
        servo1.angle(i)
        time.sleep(0.01)

    happy_mode()

def cleanup():
    servo1.stop()
    servo2.stop()

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

def finish():
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
if __name__ == "__main__":
    try:
        listen()
        time.sleep(2)
        finish()
    except KeyboardInterrupt:
        cleanup()