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

    def detect(self, image):
        zones = []
        mask, image_copy = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
        table = self.detectTable(image_copy)
        zones.append(table)
        StartZone = self.detectStartZone(mask)
        zones.append(StartZone)
        croppedImage = self.CropTableFromImage(image_copy, table)
        shapeZone = self.detectShapeZone(croppedImage)
        zones.append(shapeZone)
        deposit = self.detectTargetZone(image)
        zones.append(deposit)
        return zones

    def detectTable(self, image):
        mask = self._threshold_black(image)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        table_found = False
        for c in contours:
            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= MIN_TABLE_AREA and area < MAX_TABLE_AREA:
                x, y, w, h = cv2.boundingRect(polygon_points)
                return mask, TableZone((x, y, w, h))

        if table_found == "False":
            raise TableZoneNotFoundError

    def detectStartZone(self, image):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        square_found = False
        for c in contours:
            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= MIN_START_ZONE_AREA and area < MAX_START_ZONE_AREA:
                x, y, w, h = cv2.boundingRect(polygon_points)
                return StartZone(Square((x, y, w, h)))

        if square_found == "False":
            raise StartZoneNotFoundError

    def detectShapeZone(self, image):
        found = False
        mask = cv2.GaussianBlur(image.copy(), (7, 7), 0)
        mask = cv2.GaussianBlur(mask, (7, 7), 0)

        mask = cv2.adaptiveThreshold(cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY), 255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=5)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

        for c in contours:

            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= 11500 and area <= 14500:
                x, y, w, h = cv2.boundingRect(polygon_points)
                return ShapeZone((x, y, w, h))
        if found == False:
            raise ShapeZoneNotFoundError

    def detectTargetZone(self, image):
        found = False
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cimage = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel=kernel, iterations=3)
        cimage = cv2.Canny(cimage, 150, 150)
        cimage = cv2.GaussianBlur(cimage, (1, 1), 0)
        cimage = cv2.Canny(cimage, 150, 150)
        contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        for c in contours:
            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= 4000 and area <= 6200 and len(polygon_points) == 4:
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
