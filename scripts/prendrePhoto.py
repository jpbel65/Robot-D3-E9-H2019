import cv2
import numpy as np
from PIL import Image

def main():
    capture = cv2.VideoCapture(1)

    while True:

        ret, frame = capture.read()
        cv2.imshow('Current', frame)
        cv2.imwrite("Photos&Calibration/Screen/wadawdwa.jpg", frame )
        exit(0)




if __name__ == "__main__":
   code = main()
