#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Application import MainController
from Domain.HSVColorsAndConfig import *

class TrajectoryMapper(object):

    def __init__(self,ratio):
        self._ratio = None
        self._yCells = int(TABLE_WIDTH * ratio)
        self._xCells = int(TABLE_LENGTH * ratio)
        pass

    def mapTableObjects(self,world):
        tableMap = self.createTable(self._xCells, self._yCells)

        self.addWallsToTable(tableMap)
        for obstacle in world.obstacle:
            self.addObstacle(obstacle.y, obstacle.x, tableMap)



    def createTable(self, x, y):
        table = []
        for i in range(y):
            array = []
            for j in range(x):
                array.insert(0, ' ')

            table.insert(0, array)
        return table

    def addWallsToTable(self, table):
        y = len(table)
        x = len(table[0])
        for i in range(x):
            table[0][i] = 'W'
            table[y - 1][i] = 'W'

        for j in range(y):
            table[j][0] = 'W'
            table[j][x - 1] = 'W'

    def addObstacle(self, y, x, table):
        initialX = int(x * self._ratio)
        initialY = int(y * self._ratio)
        obstacleRay = OBSTACLE_WIDTH / 2

        table[initialY][initialX] = 'W'

        for i in range(len(table)):
            for j in range(len(table[0])):
                deltaX = (x - j / self._ratio)
                deltaY = (y - i / self._ratio)
                if deltaX ** 2 + deltaY ** 2 < obstacleRay ** 2:
                    table[i][j] = 'W'

    def addSpacing(self, table):
        robotRay = ROBOT_LENGHT / 2
        for i in range(len(table)):
            for j in range(len(table[0])):
                if table[i][j] is 'W':

                    for k in range(len(table)):
                        for l in range(len(table[0])):
                            if table[k][l] is not 'W' and table[k][l] is not 'o':
                                deltaX = (l / self._ratio - j /self._ratio)
                                deltaY = (k / self._ratio - i / self._ratio)
                                if deltaX ** 2 + deltaY ** 2 < robotRay ** 2:
                                    table[k][l] = 'o'
