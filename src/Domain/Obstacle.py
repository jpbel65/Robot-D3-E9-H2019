#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import World
from Domain import ObstaclesDetector


class Obstacle:
	def __init__(self, center, radius):
		self._coordinate = center
		self._radius = radius

