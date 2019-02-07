import cv2
import numpy as np
from PIL import Image

def main():
    capture = cv2.VideoCapture(0)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = capture.read()
        cv2.imshow('Current', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)

        qrDetector=cv2.QRCodeDetector() 
        retval , points ,straight_qrcode = qrDetector.detectAndDecode(frame)
        if len(retval)>0:
            print(retval)
            straight_qrcode = np.uint8(straight_qrcode)
            cv2.imshow('rectified qr code',straight_qrcode)



if __name__ == "__main__":
   code = main()
