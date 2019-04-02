import threading

class Node():
    def __init__(self, parent=None, position=None, directionFrom = 0):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.directionFrom = directionFrom

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, direction=0):

    start_node = Node(None, start, direction)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end, 3)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        #, (-1, -1), (-1, 1), (1, -1), (1, 1)
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != ' ':
                continue

            new_node = Node(current_node, node_position)
            if new_position == (0, -1):
                new_node = Node(current_node, node_position, 1)
            elif new_position == (0, 1):
                new_node = Node(current_node, node_position, 3)
            elif new_position == (1, 0):
                new_node = Node(current_node, node_position, 0)
            elif new_position == (-1, 0):
                new_node = Node(current_node, node_position, 2)

            children.append(new_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            if current_node.directionFrom != child.directionFrom:
                child.h = child.h + 8000
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)


class PathFinding:
    #TABLE_WIDTH = 111
    #TABLE_LENGTH = 231
    #ROBOT_WIDTH = 22
    #ROBOT_LENGHT = 22
    #OBSTACLE_WIDTH = 13
    #RATIO = 0.2

    #yCells = int(TABLE_WIDTH * RATIO)  # 101 208
    #xCells = int(TABLE_LENGTH * RATIO)  # 303 625
    actual_path = None

    def __init__(self, world, robot_width = 22, robot_lenght =22, obstacle_width = 13, ratio = 0.2, path_box = []):
        self.pixelRatio = world._ratioPixelCm
        self.axisX = world._axisX
        self.axisY = world._axisY
        self.TABLE_WIDTH = 111#world._width
        self.TABLE_LENGTH = 231#world._height
        self.ROBOT_WIDTH = robot_width
        self.ROBOT_LENGHT = robot_lenght
        self.OBSTACLE = world._obstacles
        self.OBSTACLE_WIDTH = obstacle_width #self.obstacle._radius
        self.RATIO = ratio
        self.yCells = int(self.TABLE_WIDTH * self.RATIO)
        self.xCells = int(self.TABLE_LENGTH * self.RATIO)
        self.path_websocket = path_box#est le array des tracé qui seront utiliser par les websocket
        self.tableLayout = []

    def centimetersToCoords(self, meters):
        return int(round(meters * self.RATIO))

    def coordToCentimeters(self, coord):
        return int(round(coord / self.RATIO))

    def createTable(self, x, y):
        table = []
        for i in range(y):
            array = []
            for j in range(x):
                array.insert(0, ' ')

            table.insert(0, array)
        self.tableLayout = table

    def addWallsToTable(self):
        y = len(self.tableLayout)
        x = len(self.tableLayout[0])
        for i in range(x):
            self.tableLayout[0][i] = 'W'
            self.tableLayout[y-1][i] = 'W'

        for j in range(y):
            self.tableLayout[j][0] = 'W'
            self.tableLayout[j][x-1] = 'W'

    def addObstacle(self, y, x):
        initialX = int(x*self.RATIO)
        initialY = int(y*self.RATIO)
        obstacleRay = self.OBSTACLE_WIDTH / 2

        self.tableLayout[initialY][initialX] = 'W'

        for i in range(len(self.tableLayout)):
            for j in range(len(self.tableLayout[0])):
                if self.tableLayout[i][j] == 'W':
                    continue
                deltaX = (x-j/self.RATIO)
                deltaY = (y-i/self.RATIO)
                if deltaX**2+deltaY**2 < obstacleRay**2 :
                    self.tableLayout[i][j]= 'W'

    def addSpacing(self):
        robotRay = self.ROBOT_LENGHT/2
        for i in range(len(self.tableLayout)):
            for j in range(len(self.tableLayout[0])):
                if self.tableLayout[i][j] is 'W':

                    for k in range(len(self.tableLayout)):
                        for l in range(len(self.tableLayout[0])):
                            if self.tableLayout[k][l] is 'W' or self.tableLayout[k][l] is 'o':
                                continue
                            if self.tableLayout[k][l] is not 'W' and self.tableLayout[k][l] is not 'o':
                                deltaX = (l/self.RATIO - j / self.RATIO)
                                deltaY = (k/self.RATIO - i / self.RATIO)
                                if deltaX**2+deltaY**2 < robotRay**2:
                                    self.tableLayout[k][l] = 'o'

    def movementsInCm(self, cellMovements):
        cmMovements = []
        for i in cellMovements:
            #cmMovements.append((self.coordToCentimeters(i[0]) + (self.axisX / self.pixelRatio), self.coordToCentimeters(i[1]) + (self.axisY / self.pixelRatio)))
            cmMovements.append((self.coordToCentimeters(i[0]), self.coordToCentimeters(i[1])))
        return cmMovements

    def getTestTablePath(self):
        self.createTable(self.xCells, self.yCells)

        self.addWallsToTable()
        self.addObstacle(40, 50)
        self.addObstacle(109, 229)

        self.addSpacing()

        cellMovements = astar(self.tableLayout, (self.centimetersToCoords(30), self.centimetersToCoords(30)),(self.centimetersToCoords(75), self.centimetersToCoords(185)))

        #cellMovements = self.smoothPathCompare()

        self.actual_path = self.movementsInCm(cellMovements)
        test = self.Array_to_str_path(self.actual_path)
        self.path_websocket.append(test)
        return self.actual_path

    def getPath(self, robot, destination):
        self.createTable(self.xCells, self.yCells)

        self.addWallsToTable()

        for i in self.OBSTACLE:
            self.addObstacle(i._coordinate[1]/self.pixelRatio, i._coordinate[0]/self.pixelRatio)

        self.addSpacing()

        cellMovements = astar(self.tableLayout, (self.centimetersToCoords(robot[1]/self.pixelRatio), self.centimetersToCoords(robot[0]/self.pixelRatio)), (self.centimetersToCoords(destination[1]/self.pixelRatio), self.centimetersToCoords(destination[0]/self.pixelRatio)))


        self.actual_path = self.movementsInCm(cellMovements)
        self.getJointPath(self.actual_path)

    def getUnsafeLocations(self):

        unsafeLocations = []

        for i in range(len(self.tableLayout)):
            for j in range(len(self.tableLayout[0])):
                if self.tableLayout[i][j] != ' ':
                    unsafeLocations.append((self.coordToCentimeters(i), self.coordToCentimeters(j)))

        return unsafeLocations

    def thread_start_pathfinding(self, robot, destination):
        t = threading.Thread(target=self.getPath, args=(robot, destination))
        t.start()

    def Array_to_str_path(self, path_array):
        return_value = str()
        for i in range(1, len(path_array)):
            start = path_array[i-1]
            diffX = path_array[i][0]-start[0]
            diffY = path_array[i][1]-start[1]
            if diffY > 0:
                return_value = return_value + "r"
            if diffY < 0:
                return_value = return_value + "l"
            if diffX > 0:
                return_value = return_value + "d"
            if diffX < 0:
                return_value = return_value + "u"
        return return_value

    def getJointPath(self, path):
        bufferPath = []
        for i in path:
            if i != path[-1]:
                bufferPath.append((path[path.index(i)+1][0]-i[0], path[path.index(i)+1][1]-i[1]))
        while(bufferPath):
            jointLenght = 1

            for k in range(0, len(bufferPath)-1):
                if bufferPath[k][0] == bufferPath[k+1][0] and bufferPath[k][1] == bufferPath[k+1][1]:
                #if k == bufferPath[bufferPath.index(k)+1] and k != bufferPath[-1]:
                        jointLenght = jointLenght + 1
                else :
                    diffY = bufferPath[k][1]
                    diffX = bufferPath[k][0]
                    side = None
                    if diffY > 0:
                        side = "O"
                    if diffY < 0:
                        side = "E"
                    if diffX > 0:
                        side = "N"
                    if diffX < 0:
                        side = "S"
                    movement = bufferPath[k][0]*jointLenght
                    if movement == 0:
                        movement = bufferPath[k][1]*jointLenght

                    movementString = []
                    if abs(movement) < 10:
                        self.path_websocket.append('D' + side + "00" + str(abs(int(movement))))

                    elif 9 < abs(movement) < 100:
                        self.path_websocket.append('D' + side + "0" + str(abs(int(movement))))
                    else:
                        self.path_websocket.append('D' + side + "0" + str(abs(int(movement/2))))
                        self.path_websocket.append('D' + side + "0" + str(abs(int(movement/2))))
                    for i in range(0, jointLenght):
                        bufferPath.remove(bufferPath[0])
                    break


    def smoothPathCompare(self):
        smoothestPath = []
        straightMovesCount = 0
        for i in range(0, 4):
            consecutiveMovements = 0
            path = astar(self.tableLayout, (self.centimetersToCoords(70), self.centimetersToCoords(180)),(self.centimetersToCoords(30), self.centimetersToCoords(30)), i)
            for j in path:
                if j is not path[-1] and j is not path[-2]:
                    yMovement = abs(j[0] - path[path.index(j)+1][0]) +  abs(path[path.index(j)+1][0] - path[path.index(j)+2][0])
                    xMovement = abs(j[1] - path[path.index(j) + 1][1]) + abs(path[path.index(j) + 1][1] - path[path.index(j) + 2][1])
                    if yMovement == 2 or xMovement == 2:
                        consecutiveMovements = consecutiveMovements + 1
            if consecutiveMovements > straightMovesCount:
                smoothestPath = path
                straightMovesCount = consecutiveMovements

        print(smoothestPath)
        return smoothestPath

'''
def main():

    getTestTable()

    tableMap = createTable(xCells, yCells)

    startingX = float(input("Entrez la coordonne en X du centre du robot: (cm) : "))
    startingY = float(input("Entrez la coordonne en Y du centre du robot: (cm) : "))

    targetX = float(input("Entrez la coordonne en X de la cible: (cm) : "))
    targetY = float(input("Entrez la coordonne en Y de la cible: (cm) : "))


    addWallsToTable(tableMap)
    ob1x = float(input("Entrez la coordonne en X du premier obstacle: (cm) : "))
    ob1y = float(input("Entrez la coordonne en Y du premier obstacle: (cm) : "))

    ob2x = float(input("Entrez la coordonne en X du deuxieme obstacle: (cm) : "))
    ob2y = float(input("Entrez la coordonne en Y du deuxieme obstacle: (cm) : "))

    addObstacle(ob1y, ob1x, tableMap)
    addObstacle(ob2y, ob2x, tableMap)

    for i in tableMap:
        print(i)

    print("------------------------------------------------------------------------")

    input()

    addSpacing(tableMap)

    for i in tableMap:
        print(i)
    print("------------------------------------------------------------------------")

    input()
    directions = astar(tableMap, (int(startingY*RATIO), int(startingX*RATIO)), (int(targetY*RATIO), int(targetX*RATIO)))

    for i in directions:
        tableResult = tableMap
        tableResult[i[0]][i[1]] = '*'

    for i in tableMap:
        print(i)

    print("------------------------------------------------------------------------")

    input()
    for coords in directions:
        if directions[directions.index(coords)] is not directions[len(directions)-1]:
            print('('+str((directions[directions.index(coords)+1][0]-coords[0])/RATIO) + ', ' + str((directions[directions.index(coords)+1][1]- coords[1])/RATIO) + ')')


if __name__ == '__main__':
    main()
'''
