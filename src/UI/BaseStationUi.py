#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Application import MainController

class BaseStationUi(object):
	def start(self):
		"""@ReturnType void"""
		pass

	def stop(self):
		"""@ReturnType void"""
		pass

	def startTime(self):
		"""@ReturnType void"""
		pass

	def stopTime(self):
		"""@ReturnType void"""
		pass

	def __init__(self):
		self.___mainController = None
		"""@AttributeType Application.MainController"""
		self._unnamed_MainController_ = None
		# @AssociationType Application.MainController
		# @AssociationKind Composition

