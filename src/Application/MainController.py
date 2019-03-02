#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Service import RobotController
from Domain import World
from Application import VisionController
from Application import TrajectoryMapper
from Application import TrajectoryCalculator
from Domain import ScaleConverter
from Domain import Robot
from UI import BaseStationUi

class MainController(object):
	def sendMessageToRobot(self, aString_message):
		pass

	def setPieceToTakeInfo(self):
		pass

	def main(self):
		"""@ReturnType void"""
		pass

	def __init__(self):
		self.___robotController = None
		"""@AttributeType Service.RobotController"""
		self.___table = None
		"""@AttributeType Domain.World"""
		self.___visionController = None
		"""@AttributeType Application.VisionController"""
		self.___trajectoryMapper = None
		"""@AttributeType Application.TrajectoryMapper"""
		self.___trajectoryCalculator = None
		"""@AttributeType Application.TrajectoryCalculator"""
		self.___pieceToTakeInfo = None
		"""@AttributeType String"""
		self.___converter = None
		"""@AttributeType Domain.ScaleConverter"""
		self.___robot = None
		"""@AttributeType Domain.Robot"""
		self.___zoneList = None
		"""@AttributeType List"""
		self.___shapeList = None
		"""@AttributeType List"""
		self. = None
		# @AssociationType UI.BaseStationUi
		self._unnamed_RobotController_ = None
		# @AssociationType Service.RobotController
		# @AssociationKind Composition
		self._unnamed_TrajectoryMapper_ = None
		# @AssociationType Application.TrajectoryMapper
		# @AssociationKind Aggregation
		self._unnamed_ScaleConverter_ = None
		# @AssociationType Domain.ScaleConverter
		# @AssociationMultiplicity 1
		# @AssociationKind Aggregation

