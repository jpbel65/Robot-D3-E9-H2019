#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import Any


class World(object):

	def __init__(self, table, zones, obstacles):
		self._axisX = table.getOriginX()
		self._axisY = table.getOriginY()
		self._width = table.getWidth()
		self._height = table.getHeight()
		self._shapes = None
		self._obstacles = obstacles
		self._targetZone = zones[2]
		self._shapeZone = zones[1]
		self._startZone = zones[0]
		self._chargeZone = None
		self._tableZone = table

	def set_shapes(self, shapes):
		self._shapes = shapes

	def set_charge_zone(self, charge_zone):
		self._chargeZone = charge_zone


