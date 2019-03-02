#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Application import VisionController
from Domain import Obstacle
from Domain import WorldEntityDetector

class ObstaclesDetector(WorldEntityDetector):
	def detect(self):
		"""@ReturnType List"""
		pass

	def __init__(self):
		self.___obstaclesList = None
		"""@AttributeType List"""
		self._unnamed_VisionController_ = None
		# @AssociationType Application.VisionController
		# @AssociationMultiplicity 1
		self._unnamed_Obstacle_ = None
		# @AssociationType Domain.Obstacle
		# @AssociationKind Aggregation

