#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from PIL import Image
import cv2


class QrCodeNotDetected(Exception):
    pass


class QrCalculator():
    def __init__(self):
        pass

    def getShapeOrColor(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)

        qrDetector = cv2.QRCodeDetector()
        retval, points, straight_qrcode = qrDetector.detectAndDecode(image)
        if len(retval) > 0:
            return retval
        else:
            raise QrCodeNotDetected
