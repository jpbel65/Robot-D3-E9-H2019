import cv2
import numpy as np
import math
import imutils


def detect(crop_img):
    image = cv2.GaussianBlur(crop_img, (5, 5), 0)
    image = cv2.medianBlur(image, ksize=3)
    resized = image

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny_output = cv2.Canny(resized, 150, 150)
    canny_output = cv2.GaussianBlur(canny_output, (5, 5), 0)
    canny_output = cv2.Canny(resized, 150, 150)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_OPEN, kernel=kernel)
    canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    hierachy = cv2.findContours(canny_output_close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(hierachy)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    for c in cnts:
        M = cv2.moments(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
            centerX = int((M["m10"] / M["m00"]))
            centerY = int((M["m01"] / M["m00"]))

            peak = getTrianglePeak(approx)
            dy = peak[1] - centerY
            dx = peak[0] - centerX

            angle = math.atan2(-dy, dx)
            angle = np.rad2deg(angle)
            angle = angle
            centerX = centerX
            centerY = centerY
            return angle, (centerX, centerY)


def getTrianglePeak(markers):
    dis1 = math.sqrt((markers[0][0][0] - markers[1][0][0]) ** 2 + (markers[0][0][1] - markers[1][0][1]) ** 2)
    dis2 = math.sqrt((markers[0][0][0] - markers[2][0][0]) ** 2 + (markers[0][0][1] - markers[2][0][1]) ** 2)
    dis3 = math.sqrt((markers[1][0][0] - markers[2][0][0]) ** 2 + (markers[1][0][1] - markers[2][0][1]) ** 2)
    # distance_1 = euc_distance(markers[0], markers[1])
    # distance_2 = euc_distance(markers[0], markers[2])
    # distance_3 = euc_distance(markers[1], markers[2])

    if dis1 > dis2 and dis3 > dis2:
        return markers[1][0]
    if dis1 > dis3 and dis2 > dis3:
        return markers[0][0]
    else:
        return markers[2][0]


if __name__ == "__main__":
    # execute only if run as a script
    capture = cv2.VideoCapture(1)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1200);
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 760);
    capture.set(cv2.CAP_PROP_FPS, 15)

    while True:
        ret, frame = capture.read()
        crop_img = frame
        angle = detect(crop_img)
        print(angle)
        angle = angle[1]
        cv2.circle(crop_img, (angle[0], angle[1]), 80, (0, 0, 255), 4)
        cv2.imshow("Robot detecte",crop_img)
        cv2.waitKey()


