#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Domain.WorldEntityDetector import WorldEntityDetector
import cv2
import numpy as np
import math
import imutils
import threading


class RobotNotFoundError(Exception):
    pass
class RobotDetector(WorldEntityDetector):

    def __init__(self):
        self.angle = None
        self.centerX = None
        self.centerY = None

    def thread_start_Detector(self, crop_img):
        """Button action event"""
        t5 = threading.Thread(target=self.detect, args=crop_img)
        t5.start()

    def detect(self, crop_img):
        found= False
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
       # cv2.imshow('canny_output_close',  canny_output_close )
        #cv2.waitKey()

        hierachy = cv2.findContours(canny_output_close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(hierachy)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:15]

        for c in cnts:
            M = cv2.moments(c)
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            area =cv2.contourArea(approx)
            if len(approx) == 3 and area >= 000:
                found=True
                print(area)
                centerX = int((M["m10"] / M["m00"]))
                centerY = int((M["m01"] / M["m00"]))
                #cv2.circle(crop_img, (centerX, centerY), 40, (0, 255, 255), 10)



                peak = self.getTrianglePeak(approx)
                dy = peak[1] - centerY
                dx = peak[0] - centerX

                angle = math.atan2(-dy, dx)
                angle = np.rad2deg(angle)
                centerX=int(round(centerX+peak[0])/2)
                centerY=int(round(centerY+peak[1])/2)
                self.angle = angle
                self.centerX = centerX
                self.centerY = centerY
                return angle, (centerX, centerY)
        if found == False:
            raise RobotNotFoundError


    def getTrianglePeak(self,markers):
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