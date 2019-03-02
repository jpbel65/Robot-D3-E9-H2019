#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from Domain import ZoneDetector

class __abstract___Zone(object):
	__metaclass__ = ABCMeta
	@classmethod
	def getDimensions(self):
		"""@ReturnType Tuple(Float,Float)"""
		pass

	@classmethod
	def __init__(self):
		self.___coordinate = None
		"""@AttributeType Tuple(Float,Float)"""
		self._unnamed_ZoneDetector_ = []
		# @AssociationType Domain.ZoneDetector[]
		# @AssociationMultiplicity 1..*

