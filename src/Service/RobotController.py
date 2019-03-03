#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Service import QrCalculator
from Service import PiVisionController
from Service import TourelleController
from Service import ArmController
from Application import MainController

class RobotController(object):
	def __moveUpward(self):
		pass

	def __moveBackward(self):
		pass

	def __moveLeft(self):
		pass

	def __moveRight(self):
		pass

	def chargeCondensator(self):
		pass

	def moveRobotToFollowPath(self):
		pass

	def sendMessageToStation(self, aString_message):
		pass

	def toggleLedSignal(self, aValue_val):
		pass

	def moveToQRZone(self):
		pass

	def __init__(self):
		self.___isMoving = None
		self.___qrCalculator = None
		self.___piVision = None
		self.___tourelle = None
		self.___armController = None
		self._unnamed_QrCalculator_ = None


