import cv2
import RPi.GPIO as GPIO
import time

# 设置舵机引脚
SERVO_PIN = 18  # 根据你的连接选择适当的 GPIO 引脚

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)  # 初始化 PWM，50Hz
pwm.start(7.5)  # 设置初始位置

def set_servo_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.1)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

# 加载 Haar Cascade 分类器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    # 读取图像
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测面部
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # 如果检测到面部
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_center_x = x + w // 2
        frame_center_x = frame.shape[1] // 2

        # 计算角度并控制舵机
        angle = (face_center_x - frame_center_x) / frame_center_x * 90
        set_servo_angle(90 + angle)  # 调整角度偏移以适应舵机

        # 绘制面部检测框
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # 显示图像
    cv2.imshow('Face Tracking', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 清理资源
cap.release()
cv2.destroyAllWindows()
pwm.stop()
GPIO.cleanup()
