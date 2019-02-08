import cv2
import numpy as np
from PIL import Image

def main():
    capture = cv2.VideoCapture(0)

    while True:

        ret, frame = capture.read()
        cv2.imshow('Current', frame)
        cv2.imwrite("/home/pi/Documents/Robot-D3-E9-H2019/PhotoForme/Pentagon.jpg", frame )
        exit(0)




if __name__ == "__main__":
   code = main()
