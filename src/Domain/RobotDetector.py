#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Domain.WorldEntityDetector import WorldEntityDetector
import cv2
import numpy as np
import math
import imutils
import threading
import cv2.aruco as aruco


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
        #cv2.imshow('canny_output_close', crop_img)
        #cv2.waitKey()
        found= False
        image = cv2.GaussianBlur(crop_img, (5, 5), 0)
        image = cv2.medianBlur(image, ksize=3)
        resized = image

        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny_output = cv2.Canny(resized, 150, 150)
        canny_output = cv2.GaussianBlur(canny_output, (5, 5), 0)
        canny_output = cv2.Canny(resized, 150, 150)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(1, 1))
        canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_OPEN, kernel=kernel)
        canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
       # cv2.imshow('canny_output_close',  canny_output_close)
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
               # cv2.circle(crop_img, (centerX, centerY), 40, (0, 255, 255), 10)
               # print("robot")
                #cv2.imshow("robot",crop_img)
                #cv2.waitKey()
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

    def detectAruco(self, crop_img, table):
        coinS = (0,0)
        coinO = (coinS[0] + table.width, coinS[1] + table.height)

        LongTableCm = 231
        LargTableCm = 111

        LongTablePx = coinO[0] - coinS[0]
        LargTablePx = coinO[1] - coinS[1]

        hauteurTable = 197
        hauteurRobot = 24

        CentreTablePx = ((coinO[0] + coinS[0]) / 2, ((coinO[1] + coinS[1]) / 2))


        def pixXtoCM(SizePixel):
            SizeCM = (LongTableCm / LongTablePx) * SizePixel
            return SizeCM

        def CMxtopix(SizeCM):
            SizePixel = SizeCM * LongTablePx / LongTableCm
            return SizePixel

        def pixYtoCM(SizePixel):
            SizeCM = (LargTableCm / LargTablePx) * SizePixel
            return SizeCM

        def CMytopix(SizeCM):
            SizePixel = SizeCM * LargTablePx / LargTableCm
            return SizePixel

        def posReal(detX, detY):
            distXPx = CentreTablePx[0] - detX
            distYPx = CentreTablePx[1] - detY
            distXCm = pixXtoCM(distXPx)
            distYCm = pixXtoCM(distYPx)

            angleCamX = np.arctan(distXCm / hauteurTable)
            angleCamY = np.arctan(distYCm / hauteurTable)

            offsetCMX = hauteurRobot * np.tan(angleCamX)
            offsetCMY = hauteurRobot * np.tan(angleCamY)

            offsetPxX = CMxtopix(offsetCMX)
            offsetPxY = CMytopix(offsetCMY)

            position = (detX + offsetPxX, detY + offsetPxY)

            return (position)

        found = False
        id_to_find = 8
        marker_size = 100  # - [cm]
        calibrationFile = "data.xml"
        calibrationParams = cv2.FileStorage(calibrationFile, cv2.FILE_STORAGE_READ)
        camera_matrix = calibrationParams.getNode("Camera_Matrix").mat()
        dist_coeffs = calibrationParams.getNode("Distortion_Coefficients").mat()
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        parameters = aruco.DetectorParameters_create()
        gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)

        # Capture frame-by-frame

        # Our operations on the frame come here

        res = cv2.aruco.detectMarkers(gray, dictionary)

        if len(res[0]) > 0:
            corners = res[0]

            coinA = (corners[0][0][0][0], corners[0][0][0][1])
            coinB = (corners[0][0][1][0], corners[0][0][1][1])
            coinC = (corners[0][0][2][0], corners[0][0][2][1])
            coinD = (corners[0][0][3][0], corners[0][0][3][1])

            centreX = (coinA[0] + coinB[0] + coinC[0] + coinD[0]) / 4
            centreY = (coinA[1] + coinB[1] + coinC[1] + coinD[1]) / 4

            centre = (centreX, centreY)

            centreReal = posReal(centreX, centreY)

            coinAreal = posReal(coinA[0], coinA[1])

            dx = coinAreal[0] - centreReal[0]
            dy = coinAreal[1] - centreReal[1]
            angle = math.atan2(-dy, dx)
            angle = np.rad2deg(angle)
            self.angle = angle
            self.centerX = centreReal[0] + coinS[0]
            self.centerY = centreReal[1] + coinS[1]
            cv2.circle(crop_img, (int(centreReal[0]), int(centreReal[1])), 3, (0,0,255), 3)
            # cv2.imshow('Image', crop_img)
            # cv2.waitKey()

            return angle, centre


        if found == False:
            raise RobotNotFoundError

