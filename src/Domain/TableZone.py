#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Domain import World
from Domain.Zone import Zone


class TableZone(Zone):

    def __init__(self, coordinate):
        self.origin = (coordinate[0], coordinate[1])
        self.width = coordinate[2]
        self.height  = coordinate[3]

    def getOriginX(self):
        return self.origin[0]

    def getOriginY(self):
        return self.origin[1]

    def getWidth(self):
        return self.width

    def getHeight(self):
        return  self.height
    def getDimensions(self):
        pass
