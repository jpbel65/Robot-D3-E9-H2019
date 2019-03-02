#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod

class WorldEntityDetector(object):
	"""@Interface"""
	__metaclass__ = ABCMeta
	@abstractmethod
	def detect(self):
		"""@ReturnType List"""
		pass

