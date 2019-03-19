#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import World
from Domain.Zone import Zone
from Domain.Square import Square

class StartZone(Zone):
	def getDimensions(self):
		pass

	def __init__(self,square):
		self.square = square

