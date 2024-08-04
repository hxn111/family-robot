import RPi.GPIO as GPIO
import time

# GPIO
GPIO.setmode(GPIO.BCM)

# define GPIO pin
servo_pin1 = 18  
servo_pin2 = 12  
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)

# set pwm frequency
pwm1 = GPIO.PWM(servo_pin1, 50)  # 50Hz
pwm2 = GPIO.PWM(servo_pin2, 50)  # 50Hz

# start pwm
pwm1.start(90)
pwm2.start(90)

def set_angle(pwm, angle):
    duty_cycle = 2.5 + (angle / 18.0)  # convert angle to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)

def happy_mode():
    for angle in range(90, 181, 2):
            set_angle(pwm1, angle)
            set_angle(pwm2, 270-angle)
            time.sleep(0.01)

    for angle in range(180, 120, -1):
        set_angle(pwm1, angle)
        set_angle(pwm2, 270-angle)
        time.sleep(0.01)

    for angle in range(120, 181, 1):
        set_angle(pwm1, angle)
        set_angle(pwm2, 270-angle)
        time.sleep(0.01)
    
    for angle in range(180, 120, -1):
        set_angle(pwm1, angle)
        set_angle(pwm2, 270-angle)
        time.sleep(0.01)

    for angle in range(120, 181, 1):
        set_angle(pwm1, angle)
        set_angle(pwm2, 270-angle)
        time.sleep(0.01)
    
    for angle in range(180, 90, -1):
        set_angle(pwm1, angle)
        set_angle(pwm2, 270-angle)
        time.sleep(0.01)


def cleanup():
    """Clean up GPIO resources."""
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    try:
        happy_mode()  # Run the happy mode pattern
    except KeyboardInterrupt:
        cleanup()





