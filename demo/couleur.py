import cv2
import numpy as np


def color(big_img,i):
  big_img = cv2.GaussianBlur(big_img , (5, 5), 0)
  big_img = cv2.medianBlur(big_img , ksize=3)
  # define green value range
  image_hsv = cv2.cvtColor(big_img, cv2.COLOR_BGR2HSV)
  #cv2.imshow("img", big_img)

  big_img_hsv = cv2.cvtColor(big_img, cv2.COLOR_BGR2HSV)
  #cv2.imshow("img2", big_img_hsv)
  str=""
  # black
  # mask = cv2.inRange(big_img_hsv , np.array([0, 0, 0]), np.array([180, 255, 90]))
  # white
  # mask = cv2.inRange(big_img_hsv , np.array([0, 0, 0]), np.array([0, 0, 255]))
  # blue
  if i == "0":
    mask=cv2.inRange(big_img_hsv,np.array([90,110,80]),np.array([110,255,255]))
    str="blue"
    #  alternative mask = cv2.inRange(big_img_hsv ,np.array([80,50,50]), np.array([130,255,255]))
  elif i == "1":
       #yellow
       mask = cv2.inRange(big_img_hsv ,np.array([15, 95, 60]), np.array([35, 255, 255]))
       str="jaune"
  elif i == "2":
       # red
       mask = cv2.inRange(big_img_hsv ,np.array([0, 150, 100]), np.array([15, 255, 255]))
       str="rouge"

  elif i == "3":

       # green
       mask = cv2.inRange(big_img_hsv, np.array([40, 36, 50]), np.array([80, 255, 255]))
       str="vert"
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
  mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
  mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
  contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
  color_img = cv2.drawContours(color_img, contours, -1, (0, 255, 0), 2)
  cv2.imshow("Contour"+" "+str, color_img)
if __name__ == "__main__":
  big_img = cv2.imread("multi.jpg", 1)
  color(big_img,"0")
  color(big_img, "1")
  color(big_img, "2")
  color(big_img, "3")
  cv2.waitKey()
