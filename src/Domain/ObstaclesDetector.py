#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Application import VisionController
from Domain import Obstacle
from Domain.WorldEntityDetector import WorldEntityDetector

class ObstaclesDetector(WorldEntityDetector):

	def __init__(self):
		self.___obstaclesList = None


	def detect(self,image):
		pass
