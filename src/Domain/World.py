#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import Any


class World(object):
	def __init__(self, table, zones, obstacles):
		self.___axisX = table.getOriginX
		self.___axisY = table.getOriginY
		self.___width = table.getWidth
		self.___height = table.getHeight
		self.___shapes = None
		self.___obstacles = obstacles
		self.___targetZone = zones[2]
		self.___shapeZone = zones[1]
		self.___startZone = zones[0]
		self.___chargeZone = None
		self.___tableZone = table

	def set_shapes(self, shapes):
		self.___shapes = shapes

	def set_charge_zone(self, charge_zone):
		self.___chargeZone = charge_zone


