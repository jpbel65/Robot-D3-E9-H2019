#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod

class Zone(metaclass=ABCMeta):
	@classmethod
	def getDimensions(self):
		pass

	@classmethod
	def __init__(self):
		self.___coordinate = None
