#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import World
from Domain import __abstract___Zone

class TargetZone(__abstract___Zone):
	def getDimensions(self):
		"""@ReturnType Tuple(Float,Float)"""
		pass

	def __init__(self):
		self._unnamed_World_ = None
		# @AssociationType Domain.World

