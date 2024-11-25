import cv2
from ..config import PICS_DIR

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 10)


def qr_code_scanner():
    """Thread function to continuously scan QR codes."""
    last_shot_taken = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Take a screenshot every 2 seconds
        if time.time() - last_shot_taken > 2:
        	last_shot_taken = time.time()
            screenshot_filename = os.path.join(
            	PICS_DIR, f'{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg')
            cv2.imwrite(screenshot_filename, frame)
            time.sleep(1)
            # # scan QR codes
            # routine_flow(frame)


qr_code_scanner()