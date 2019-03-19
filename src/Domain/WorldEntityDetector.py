#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod

class WorldEntityDetector(metaclass=ABCMeta):
	"""@Interface"""

	@abstractmethod
	def detect(self,image):
		pass

