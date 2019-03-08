#!/usr/bin/python
# -*- coding: UTF-8 -*-
from src.Domain.ShapeDetector import ShapeDetector
from src.Domain.Cercle import Cercle
import cv2
import imutils

class CircleNotFoundException(Exception):
	pass

class CircleDetector(ShapeDetector):
	def detect(self,image):
		hierachy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(hierachy)
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
		found = False
		for c in cnts:
			# compute the center of the contour, then detect the name of the
			# shape using only the contour
			M = cv2.moments(c)
			if M["m00"] != 0:
				centerX = int((M["m10"] / M["m00"]))
				centerY = int((M["m01"] / M["m00"]))
			else:
				centerX, centerY = 0, 0
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		if len(approx)  > 5:
			return Cercle((centerX, centerY))
		if found == False:
			raise CircleNotFoundException

