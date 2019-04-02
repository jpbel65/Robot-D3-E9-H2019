#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Application import VisionController
from Domain import Zone
from Domain.WorldEntityDetector import WorldEntityDetector
from Domain.HSVColorsAndConfig import *
from Domain.TableZone import TableZone
from Domain.StartZone import StartZone
from Domain.Square import Square
from Domain.ShapeZone import ShapeZone
from Domain.TargetZone import TargetZone
import cv2


class TableZoneNotFoundError(Exception):
    pass


class StartZoneNotFoundError(Exception):
    pass


class ShapeZoneNotFoundError(Exception):
    pass


class TargetZoneNotFoundError(Exception):
    pass


class ZoneDetector(WorldEntityDetector):

    def __init__(self):
        self.___zoneList = None

    def detect(self, image, table):
        x1, y1, w1, h1 = table.getOriginX(), table.getOriginY(), table.getWidth(), table.getHeight()
        zones = []
        image_copy = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
        StartZone = self.detectStartZone(image_copy)
        zones.append(StartZone)
        deposit = self.detectTargetZone(image)
        zones.append(deposit)
        shapeZone = self.detectShapeZone(image_copy, w1, h1)
        zones.append(shapeZone)

        return zones

    def detectTable(self, image):
        image_copy = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_copy, LOWER_BLACK_HSV, UPPER_BLACK_HSV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8]
        table_found = False
        for c in contours:
            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= MIN_TABLE_AREA and area < MAX_TABLE_AREA:
                x, y, w, h = cv2.boundingRect(polygon_points)
                return TableZone((x, y, w, h))

        if table_found == "False":
            raise TableZoneNotFoundError

    def detectTableAlternative(self, image):
        image_copy = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
        mask = cv2.adaptiveThreshold(cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY), 255,
                                     cv2.THRESH_BINARY, cv2.THRESH_BINARY, 11, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=2)
        cv2.imshow('',mask)
        cv2.waitKey()
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
        table_found = False
        for c in contours :
            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= 600000 and area <= 800000:
                  x, y, w, h = cv2.boundingRect(polygon_points)
                  return TableZone((x, y, w, h))

        if table_found == "False":
            raise TableZoneNotFoundError

    def detectStartZone(self, image):
        mask = cv2.inRange(image, np.array([0, 0, 0]), np.array([180, 255, 110]))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8]
        square_found = False
        for c in contours:
            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= MIN_START_ZONE_AREA and area < MAX_START_ZONE_AREA:
                x, y, w, h = cv2.boundingRect(polygon_points)
                M = cv2.moments(c)
                centerX = int((M["m10"] / M["m00"]))
                centerY = int((M["m01"] / M["m00"]))
                return StartZone(Square((x, y, w, h)))

        if square_found == "False":
            raise StartZoneNotFoundError

    def detectShapeZone(self, crop_img, w1, h1):

        found = False
        x1, y1 = 0, 0
        cv2.line(crop_img, (x1, y1), (x1 + w1, y1), (255, 0, 0), 15)
        mask = cv2.inRange(crop_img, np.array([0, 0, 0]), np.array([180, 255, 110]))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8]
        for c in contours:
            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= 5000 and area < 8000 and len(polygon_points) == 4:
                x, y, w, h = cv2.boundingRect(polygon_points)
                M = cv2.moments(c)
                centerX = int((M["m10"] / M["m00"]))
                centerY = int((M["m01"] / M["m00"]))
                return ShapeZone(x, y, w, h)
        if found == False:
            raise ShapeZoneNotFoundError

    def detectTargetZone(self, big_img):

          found = False
          kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))

          cimage = cv2.morphologyEx(big_img, cv2.MORPH_OPEN, kernel=kernel, iterations=3)
          cimage = cv2.Canny(cimage, 100, 150)
          cimage = cv2.GaussianBlur(cimage, (1, 1), 0)
        # cimage = cv2.Canny(cimage, 150, 150)
          cimage = cv2.dilate(cimage, kernel)
          contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
          color_img = cv2.cvtColor(cimage, cv2.COLOR_GRAY2BGR)
          contours = sorted(contours, key=cv2.contourArea, reverse=True)[:70]
          i = -1


          for c in contours:
             i += 1
             contour_length = cv2.arcLength(c, True)
             polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
             area = cv2.contourArea(polygon_points)
             if area >= 4000 and area <= 8000 and len(polygon_points) == 4:
                   x, y,  w, h = cv2.boundingRect(polygon_points)
                   M = cv2.moments(c)
                   centerX = int((M["m10"] / M["m00"]))
                   centerY = int((M["m01"] / M["m00"]))
                   return TargetZone((x, y, w, h))
             elif area >= 20 and area <= 100 and len(polygon_points) == 4:
                     x, y, w, h = cv2.boundingRect(polygon_points)
                     return TargetZone((x, y, w, h))

          if found == False:
                raise TargetZoneNotFoundError


def _threshold_black(self, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, LOWER_BLACK_HSV, UPPER_BLACK_HSV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    return mask


def CropTableFromImage(self, mask, table):
    return mask[table.getOriginY():table.getOriginY() + table.getHeight(),
           table.getOriginX():table.getOriginX() + table.getWidth()]
