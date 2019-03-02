#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Application import VisionController
from Domain import __abstract___Zone
from Domain import WorldEntityDetector

class ZoneDetector(WorldEntityDetector):
	def detect(self):
		"""@ReturnType List"""
		pass

	def __init__(self):
		self.___zoneList = None
		"""@AttributeType List"""
		self._unnamed_VisionController_ = None
		# @AssociationType Application.VisionController
		# @AssociationMultiplicity 1
		self._unnamed___abstract___Zone_ = None
		# @AssociationType Domain.<<abstract>> Zone
		# @AssociationKind Aggregation

