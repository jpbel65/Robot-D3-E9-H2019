#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Application import VisionController
from Domain import Obstacle
from Domain.WorldEntityDetector import WorldEntityDetector
from Domain.Obstacle import  Obstacle
import cv2
import numpy as np

class ObstacleNotFoundError(Exception):
    pass

class ObstaclesDetector(WorldEntityDetector):

    def __init__(self):
        self._obstaclesList = []

    def detect(self, image):
        image = cv2.medianBlur(image, 5)
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=20, minRadius=5, maxRadius=30)
        if circles == None:
            raise ObstacleNotFoundError
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            self._obstaclesList.append(Obstacle((i[0], i[1]),i[2]))
        return self._obstaclesList

