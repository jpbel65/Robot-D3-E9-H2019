#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import ShapeDetector
from Domain import ScaleConverter
from Application import MainController
from Domain import WorldEntityDetector
from Domain.SquareDetector import SquareDetector
from Domain.TriangleDetector import TriangleDetector
from Domain.PentagoneDetector import PentagoneDetector
from Domain.CircleDetector import CircleDetector
from Domain.ObstaclesDetector import ObstaclesDetector
from Domain.ZoneDetector import ZoneDetector
from Domain.HSVColorsAndConfig import *
from Domain.World import World
from Domain.RobotDetector import RobotDetector
from Domain.Robot import Robot
import numpy as np
import cv2


class ShapeNotValidError(Exception):
    pass


class VisionController:

    def __init__(self):
        self._robotDetector = RobotDetector()
        self._converter = None
        self._shapeDetector_ = None
        self._obstaclesDetector_ = ObstaclesDetector()
        self._zoneDetector_ = ZoneDetector()
        self._robot = Robot()


    def detectShapes(self, image, shape):
        specifiShapeDetector = None
        if (shape == "carre"):
            specifiShapeDetector = SquareDetector()
        elif (shape == "cercle"):
            specifiShapeDetector = CircleDetector()

        elif (shape == "triangle"):
            specifiShapeDetector = TriangleDetector()
        elif (shape == "pentagone"):
            specifiShapeDetector = PentagoneDetector()
        else:
            raise ShapeNotValidError

        processedImage = self.processImage(image)
        return specifiShapeDetector.detect(processedImage)

    def detectShapeWithColor(self, image, color):
        image = cv2.GaussianBlur(image, (5, 5), 0)
        image = cv2.medianBlur(image, ksize=3)
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # blue
        if color == "blue":
            mask = cv2.inRange(image_hsv, LOWER_BLUE_HSV, UPPER_BLUE_HSV)
        elif color == "jaune":
            # yellow
            mask = cv2.inRange(image_hsv, LOWER_YELLOW_HSV, UPPER_YELLOW_HSV)
        elif color == "rouge":
            # red
            mask = cv2.inRange(image_hsv, LOWER_RED_HSV, UPPER_RED_HSV)
        elif color == "vert":
            # green
            mask = cv2.inRange(image_hsv, LOWER_GREEN_HSV, UPPER_RED_HSV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        color_img = cv2.drawContours(color_img, contours, -1, (0, 255, 0), 2)

    def detectRobotAndGetAngle(self, image):
        #self._robotDetector.thread_start_Detector(image)
        self._robotDetector.detect(image)
        self._robot._coordinate = (self._robotDetector.centerX,self._robotDetector.centerY)
        self._robot._angle = self._robotDetector.angle

    def detectEntities(self, image):
       # try:
            image = cv2.GaussianBlur(image, (5, 5), 0)
            image = cv2.medianBlur(image, ksize=1)

            #table = self._zoneDetector_.detectTableAlternative(image)

            table = self._zoneDetector_.detectTable(image)
            x1, y1, w1, h1 = table.getOriginX(), table.getOriginY(), table.getWidth(), table.getHeight()
            crop_img = image[y1:y1 + h1, x1:x1 + w1]
            obstacles = self._obstaclesDetector_.detect(crop_img)
            zones = self._zoneDetector_.detect(crop_img, table)
            world = World(table, zones, obstacles)
            return world



       # except Exception as e:
          #  print("impossibe de detecter les zones: {}".format(type(e).__name__))

    def processImage(self, image):
        image = cv2.GaussianBlur(image, (5, 5), 0)
        image = cv2.medianBlur(image, ksize=3)
        resized = image
        # resized = imutils.resize(frame, width=300)
        ratio = image.shape[0] / float(resized.shape[0])

        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny_output = cv2.Canny(resized, 150, 150)
        canny_output = cv2.GaussianBlur(canny_output, (5, 5), 0)
        canny_output = cv2.Canny(resized, 150, 150)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
        canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_OPEN, kernel=kernel)
        canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
        return canny_output_close
