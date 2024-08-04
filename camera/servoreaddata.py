import cv2

def simulate_servo_angle(angle):
    print(f"Simulated servo angle: {angle} degrees")

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
        simulate_servo_angle(90 + angle)  # 调整角度偏移以适应舵机

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
