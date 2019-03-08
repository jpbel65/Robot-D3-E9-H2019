#!/usr/bin/python
# -*- coding: UTF-8 -*-
from src.Service.PiVisionController import PiVisionController
from src.Service import TourelleController
from src.Service import ArmController
from src.Application import MainController
from src.Service.QrCalculator import QrCalculator


class RobotController():
    def __init__(self):
        self._isMoving = None
        self._qrCalculator = QrCalculator()
        self._piVision = PiVisionController()
        self._tourelle = None
        self._armController = None

    def getShapeOrColor(self):
        image = self._piVision.takePhoto()
        return self.get_qrCalculator.getShapeOrColor(image)

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
