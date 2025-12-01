# face_led_onlinecascade.py
# Works in Thonny + VNC even when OpenCV's haarcascade data isn't installed.

import os, cv2, time, urllib.request
from gpiozero import LED
from picamera2 import Picamera2

LED_PIN = 17

def get_cascade():
    """Download Haar cascade XML if it's missing, then return its path."""
    local_xml = os.path.expanduser("~/haarcascade_frontalface_default.xml")
    if not os.path.exists(local_xml):
        print("[INFO] Downloading Haar cascade file...")
        url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        urllib.request.urlretrieve(url, local_xml)
        print(f"[INFO] Saved cascade to {local_xml}")
    return local_xml

def main():
    led = LED(LED_PIN)

    picam = Picamera2()
    picam.configure(picam.create_preview_configuration(main={"size": (640,480), "format":"RGB888"}))
    picam.start()

    cascade = cv2.CascadeClassifier(get_cascade())
    print("[INFO] Press 'q' to quit.")

    try:
        while True:
            frame = picam.capture_array()
            gray  = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = cascade.detectMultiScale(gray, 1.2, 5, minSize=(60,60))

            # LED logic
            led.on() if len(faces) else led.off()

            # Draw rectangles + show preview
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imshow("Face-Based Light Control (q to quit)", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        led.off()
        picam.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
