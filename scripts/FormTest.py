import cv2
import numpy as np
import imutils
from PIL import Image
import random as rng
def detect(c):
    shape = "unidentified"
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    # if the shape is a triangle, it will have 3 vertices
    if len(approx) == 3:
        shape = "triangle"

    # if the shape has 4 vertices, it is either a square or
    # a rectangle
    elif len(approx) == 4:
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)

        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

    # if the shape is a pentagon, it will have 5 vertices
    elif len(approx) == 5:
        shape = "pentagon"

    # otherwise, we assume the shape is a circle
    else:
        shape = "circle"

    # return the name of the shape
    return shape
	
def main():
        capture = cv2.VideoCapture(0)

            
        ret, frame = capture.read()
        resized=  imutils.resize(frame,width=300)
        ratio = frame.shape[0]/float(resized.shape[0])
        #cv2.imshow('Current', frame)
        
        gray=cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
        blurred=cv2.GaussianBlur(gray,(5,5),0)
        #thresh=cv2.threshold(blurred,127,255,cv2.THRESH_BINARY)[1]
        #th2=cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        #cv2.imshow('image',thresh)
        #cv2.imshow('image2',th2)
        canny_output = cv2.Canny(resized,60,120)
        cv2.imshow('canny',canny_output)
        noyau = np.ones((5,5), np.uint8)
        canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_CLOSE, noyau)
        cv2.imshow('Fermeture',canny_output_close)
        hierachy = cv2.findContours(canny_output_close,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        drawing = np.zeros((canny_output_close.shape[0],canny_output_close.shape[1],3),dtype=np.uint8)
        cnts = imutils.grab_contours(hierachy)
        #for i in range(len(contours)):
           # color = (rng.randint(0,256),rng.randint(0,256),rng.randint(0,256))
            #cv2.drawContours(drawing,contours,i,color,2,cv2.LINE_8, hierachy,0)
        for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
           M = cv2.moments(c)
           if M["m00"] != 0 :
               cX = int((M["m10"] / M["m00"]) * ratio)
               cY = int((M["m01"] / M["m00"]) * ratio)
           else :
               cX, cY = 0, 0
           shape = detect(c)

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
           c = c.astype("float")
           c *= ratio
           c = c.astype("int")
           cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
           cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
           print(shape)
        # show the output image
           cv2.imshow("Image", frame)
           
        cv2.imshow('COntours',drawing)
        cv2.waitKey(0)
        
        


if __name__ == "__main__":
   code = main()