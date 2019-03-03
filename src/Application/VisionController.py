#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import ShapeDetector
from Domain import ScaleConverter
from Application import MainController
from Domain import WorldEntityDetector
from Domain.ObstaclesDetector import ObstaclesDetector
from Domain.ZoneDetector import ZoneDetector
import cv2


class VisionController():

    def __init__(self):
        self._triangleDetector = None
        self._circleDetector = None
        self._pentagoneDetector = None
        self._squareDetector = None
        self._robotDetector = None
        self._converter = None
        self._shapeDetector_ = None
        self._obstaclesDetector_ = ObstaclesDetector()
        self._zoneDetector_ = ZoneDetector()


    def detectShapes(self):
        pass

    def detectEntities(self, image):
        try:
            image = cv2.GaussianBlur(image, (5, 5), 0)
            image = cv2.medianBlur(image, ksize=1)
            zones = self._zoneDetector_.detect(image)
            obstacles = self._obstaclesDetector_.detect(image)


        except Exception as e:
                   print("impossibe de detecter les zones: {}".format(type(e).__name__))


