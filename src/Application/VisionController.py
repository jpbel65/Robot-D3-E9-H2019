#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import ShapeDetector
from Domain import WorldEntityDetector
from Domain import ScaleConverter
from Application import MainController
from Domain import ObstaclesDetector
from Domain import ZoneDetector

class VisionController(object):
	def detectShapes(self):
		"""@ReturnType List"""
		pass

	def detectEntities(self):
		"""@ReturnType List"""
		pass

	def __init__(self):
		self.___triangleDetector = None
		"""@AttributeType Domain.ShapeDetector"""
		self.___circleDetector = None
		"""@AttributeType Domain.ShapeDetector"""
		self.___pentagoneDetector = None
		"""@AttributeType Domain.ShapeDetector"""
		self.___squareDetector = None
		"""@AttributeType Domain.ShapeDetector"""
		self.___obstaclesDetector = None
		"""@AttributeType Domain.WorldEntityDetector"""
		self.___zoneDetector = None
		"""@AttributeType Domain.WorldEntityDetector"""
		self.___robotDetector = None
		"""@AttributeType Domain.WorldEntityDetector"""
		self.___converter = None
		"""@AttributeType Domain.ScaleConverter"""
		self. = None
		# @AssociationType Application.MainController
		self._unnamed_ShapeDetector_ = None
		# @AssociationType Domain.ShapeDetector
		# @AssociationKind Composition
		self._unnamed_ObstaclesDetector_ = None
		# @AssociationType Domain.ObstaclesDetector
		# @AssociationKind Aggregation
		self._unnamed_ZoneDetector_ = None
		# @AssociationType Domain.ZoneDetector
		# @AssociationKind Aggregation

