#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import World

class Robot(object):
	def __init__(self):
		self._coordinate = None
		self._isMoving = None
		self._hasShape = None
		self._securityRadius = None
		self._angle = None
		self.previousPos = []

