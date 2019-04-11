#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import World
from Domain import Zone

class TargetZone():
	def getDimensions(self):
		pass

	def __init__(self,coord, points):
		self.center= (coord[0],coord[1])
		self.width= coord[2]
		self.hieght = coord[3]
		self._trueCenter = (coord[0]+self.width/2, coord[1]+self.hieght/2)
		self._points = points

