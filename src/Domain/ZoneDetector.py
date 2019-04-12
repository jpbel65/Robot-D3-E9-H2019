#!/usr/bin/python
# -*- coding: UTF-8 -*-


from Domain.WorldEntityDetector import WorldEntityDetector
from Domain.HSVColorsAndConfig import *
from Domain.TableZone import TableZone
from Domain.StartZone import StartZone
from Domain.Square import Square
from Domain.ShapeZone import ShapeZone
from Domain.TargetZone import TargetZone
import cv2
import math

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

    def detect(self, image, table,wRot):
        x1, y1, w1, h1 = table.getOriginX(), table.getOriginY(), table.getWidth(), table.getHeight()
        zones = []
        image_copy = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
        StartZone = self.detectStartZone(image_copy)
        zones.append(StartZone)
        deposit = self.detectTargetZone(image)
        print(deposit.center)
        zones.append(deposit)
        image_copy = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
        cv2.line(image_copy, (0, 0), (wRot[0] - x1, wRot[1] - y1), (255, 255, 0), 25)
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
        mask = cv2.adaptiveThreshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 255,
                                     cv2.THRESH_BINARY, cv2.THRESH_BINARY, 11, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=2)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
        table_found = False
        for c in contours :
            contour_length = cv2.arcLength(c, True)
            polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
            area = cv2.contourArea(polygon_points)
            if area >= 600000 and area <= 800000:
                  x, y, w, h = cv2.boundingRect(polygon_points)
                  rect = cv2.minAreaRect(c)
                  angle = rect[2]
                  wRot = [w, 0]

                  box = cv2.boxPoints(rect)
                  box = np.int0(box)
                  x1, x2, x3, x4 = box[0], box[1], box[2], box[3]
                  if abs(w - x1[0]) < 200 and abs(y - x1[1]) < 100:
                      wRot = x1
                  elif abs(w - x2[0]) < 200 and abs(y - x2[1]) < 100:
                      wRot = x2
                  elif abs(w - x3[0]) < 200 and abs(y - x3[1]) < 100:
                      wRot = x3
                  elif abs(w - x4[0]) < 200 and abs(y - x4[1]) < 100:
                      wRot = x4
                  return TableZone((x, y, w, h)),wRot

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
                return StartZone(x, y, w, h)

        if square_found == "False":
            raise StartZoneNotFoundError

    def detectShapeZone(self, crop_img, w1, h1):

        found = False
        x1, y1 = 0, 0

        cv2.line(crop_img, (x1, y1), (x1, y1 + h1), (255, 0, 0), 15)
        cv2.line(crop_img, (x1 + w1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 15)
        cv2.line(crop_img, (x1, h1), (x1 + w1, y1 + h1), (255, 0, 0), 15)

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
            if area >= 4000 and area < 8000 and len(polygon_points) == 4:
                x, y, w, h = cv2.boundingRect(polygon_points)
                M = cv2.moments(c)
                centerX = int((M["m10"] / M["m00"]))
                centerY = int((M["m01"] / M["m00"]))
                cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # cv2.imshow("color",color_img)
                # cv2.waitKey()


                return ShapeZone(x, y, w, h,(centerX,centerY))
        if found == False:
            raise ShapeZoneNotFoundError

    def detectTargetZone(self, big_img):
          gray = cv2.cvtColor(big_img.copy(), cv2.COLOR_BGR2GRAY)
          found = False
          kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

          cimage = cv2.morphologyEx(big_img, cv2.MORPH_OPEN, kernel=kernel, iterations=3)
          cimage = cv2.Canny(cimage, 100, 150)
          cimage = cv2.GaussianBlur(cimage, (1, 1), 0)
          cimage = cv2.dilate(cimage, kernel)

          contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

          color_img = cv2.cvtColor(cimage, cv2.COLOR_GRAY2BGR)
          contours = sorted(contours, key=cv2.contourArea, reverse=True)[:70]
          for c in contours:
              contour_length = cv2.arcLength(c, True)
              polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
              area = cv2.contourArea(polygon_points)
              if area >= 4000 and area <= 8000 and len(polygon_points) == 4:
                  x, y, w, h = cv2.boundingRect(polygon_points)
                  M = cv2.moments(c)
                  centerX = int((M["m10"] / M["m00"]))
                  centerY = int((M["m01"] / M["m00"]))
                  points = self.detectPointOfTargetZone(gray, (centerX, centerY))
                  if len(points) == 4:
                      cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                      return TargetZone((x, y, w, h), points)

          if found == False:
              raise TargetZoneNotFoundError
    def detectPointOfTargetZone(self, crop_img, centerOfZone):
        # gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
        gray = crop_img

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        cimage = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel=kernel, iterations=3)
        cimage = cv2.Canny(cimage, 150, 150)
        cimage = cv2.GaussianBlur(cimage, (5, 5), 0)
        cimage = cv2.Canny(cimage, 150, 150)
        cimage = cv2.dilate(cimage, kernel)
        contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        color_img = cv2.cvtColor(cimage, cv2.COLOR_GRAY2BGR)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:200]
        points = []
        for c in contours:
            M = cv2.moments(c)
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            area = cv2.contourArea(approx)
            centerX = int((M["m10"] / M["m00"]))
            centerY = int((M["m01"] / M["m00"]))
            disAvecCentre = math.sqrt((centerOfZone[0] - centerX) ** 2 + (centerOfZone[1] - centerY) ** 2)
            if area <= 400 and area >= 30 and disAvecCentre <= 60:
                cv2.circle(crop_img, (centerX, centerY), 2, (0, 0, 255), 3)
                points.append((centerX, centerY))
                PointInOrder = []
        for i in range(len(points)):
            if i == 0 and abs(points[i][0] - points[i][0]) >= 6:
                points.sort(key=lambda tup: tup[1])
            else:
                points.sort(key=lambda tup: tup[0])

                cv2.circle(crop_img, (centerOfZone[0], centerOfZone[1]), 2, (0, 0, 255), 3)
        return points


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

def fakeAZoneList():
    zone = []
    zone.append(StartZone(Square((115+33, 115+54, 3*115, 3*115))))
    zone.append(TargetZone((720+33, 54, 115, 114/3)))
    zone.append(ShapeZone(720+33, 580+54-114/3, 115, 114/3))
    return zone
