# motion_preview_opencv.py
import os, time, datetime as dt, cv2
from gpiozero import MotionSensor
from picamera2 import Picamera2

pir = MotionSensor(17)

picam = Picamera2()
picam.configure(picam.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}  # RGB for easy OpenCV conversion
))
picam.start()

os.makedirs("captures", exist_ok=True)
i = 1

try:
    while True:
        # Get current frame (RGB)
        frame_rgb = picam.capture_array()
        # Show live preview (convert to BGR for OpenCV display)
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        cv2.imshow("Real-Time Camera Feed (press q)", frame_bgr)

        # If motion, save the CURRENT frame
        if pir.motion_detected:
            ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"captures/motion_{ts}_{i}.jpg"
            cv2.imwrite(path, frame_bgr)
            print(f"[SAVED] {path}")
            i += 1
            time.sleep(3)  # debounce so you don't spam images

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    picam.stop()
