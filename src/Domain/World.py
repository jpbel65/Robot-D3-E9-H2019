#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import TargetZone
from Domain import ShapeZone
from Domain import StartZone
from Domain import ChargeZone
from Domain import TableZone
from Application import MainController
from Domain import Obstacle

class World(object):
	def __init__(self):
		self.___axisX = None
		"""@AttributeType Float"""
		self.___axisY = None
		"""@AttributeType Float"""
		self.___shapes = None
		"""@AttributeType List"""
		self.___obstacles = None
		"""@AttributeType List"""
		self.___targetZone = None
		"""@AttributeType Domain.TargetZone"""
		self.___shapeZone = None
		"""@AttributeType Domain.ShapeZone"""
		self.___startZone = None
		"""@AttributeType Domain.StartZone"""
		self.___chargeZone = None
		"""@AttributeType Domain.ChargeZone"""
		self.___tableZone = None
		"""@AttributeType Domain.TableZone"""
		self. = None
		# @AssociationType Application.MainController
		self._unnamed_ShapeZone_ = None
		# @AssociationType Domain.ShapeZone
		# @AssociationKind Composition
		self. = None
		# @AssociationType Domain.Obstacle
		# @AssociationKind Aggregation
		self._unnamed_TableZone_ = None
		# @AssociationType Domain.TableZone
		# @AssociationKind Composition

