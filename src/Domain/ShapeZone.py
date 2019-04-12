#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import World
from Domain.Zone import Zone

class ShapeZone(Zone):
	def getDimensions(self):
		pass

	def __init__(self,x,y,w,h,center):
		self._center =(x,y)
		self._width= w
		self._height = h
		self._trueCenter = center


