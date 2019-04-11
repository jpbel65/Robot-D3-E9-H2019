import cv2
import numpy as np
from PIL import Image

def main():
    capture = cv2.VideoCapture(1)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,760)
    capture.set(cv2.CAP_PROP_FPS,15)

    while True:

        ret, frame = capture.read()
        cv2.imshow('Current', frame)
        cv2.imwrite("Aruko3.jpg", frame )
        exit(0)




if __name__ == "__main__":
   code = main()
