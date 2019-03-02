#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Service import QrCalculator
from Service import PiVisionController
from Service import TourelleController
from Service import ArmController
from Application import MainController

class RobotController(object):
	def __moveUpward(self):
		"""@ReturnType void"""
		pass

	def __moveBackward(self):
		"""@ReturnType void"""
		pass

	def __moveLeft(self):
		"""@ReturnType void"""
		pass

	def __moveRight(self):
		"""@ReturnType void"""
		pass

	def chargeCondensator(self):
		"""@ReturnType bool"""
		pass

	def moveRobotToFollowPath(self):
		pass

	def sendMessageToStation(self, aString_message):
		pass

	def toggleLedSignal(self, aValue_val):
		pass

	def moveToQRZone(self):
		"""@ReturnType void"""
		pass

	def __init__(self):
		self.___isMoving = None
		"""@AttributeType boolean"""
		self.___qrCalculator = None
		"""@AttributeType Service.QrCalculator"""
		self.___piVision = None
		"""@AttributeType Service.PiVisionController"""
		self.___tourelle = None
		"""@AttributeType Service.TourelleController"""
		self.___armController = None
		"""@AttributeType Service.ArmController"""
		self. = None
		# @AssociationType Application.MainController
		self._unnamed_QrCalculator_ = None
		# @AssociationType Service.QrCalculator
		# @AssociationKind Aggregation

