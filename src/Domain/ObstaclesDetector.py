#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Application import VisionController
from Domain import Obstacle
from Domain.WorldEntityDetector import WorldEntityDetector
from Domain.Obstacle import  Obstacle
import cv2
import numpy as np
import math

class ObstacleNotFoundError(Exception):
    pass

class ObstaclesDetector(WorldEntityDetector):

    def __init__(self):
        self._obstaclesList = []
    def detect(self,crop_img):
        gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=70, param2=20, minRadius=20, maxRadius=35)

        circles = np.int64(np.around(circles))
        j = 0
        base = []
        for i in circles[0, :]:
            base.append((i[0], i[1]))
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=70, param2=20, minRadius=40, maxRadius=60)
        circles = np.int64(np.around(circles))
        haut = []
        for i in circles[0, :]:
            print(j)
            haut.append((i[0], i[1]))
        for x in base:
            for y in haut:
                dis = math.sqrt((x[0] - y[0]) ** 2 + (y[1] - y[1]) ** 2)
                if dis <= 100:
                    haut.remove(y)

        if len(haut) != 0:
            for x in haut:
                base.append(x)
        for i in base:
            self._obstaclesList.append(Obstacle((i[0], i[1]), i[2]))
        return self._obstaclesList
