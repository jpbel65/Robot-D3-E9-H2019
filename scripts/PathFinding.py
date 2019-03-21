
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
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

            children.append(new_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)


class PathFinding:
    TABLE_WIDTH = 111

    TABLE_LENGTH = 231

    ROBOT_WIDTH = 22
    ROBOT_LENGHT = 22

    OBSTACLE_WIDTH = 13

    RATIO = 0.2

    yCells = int(TABLE_WIDTH * RATIO)  # 101 208
    xCells = int(TABLE_LENGTH * RATIO)  # 303 625

    def centimetersToCoords(self, meters):
        return int(meters * self.RATIO)

    def coordToCentimeters(self, coord):
        return int(coord / self.RATIO)

    def createTable(self, x, y):
        table = []
        for i in range(y):
            array = []
            for j in range(x):
                array.insert(0,' ')

            table.insert(0,array)
        return table

    def addWallsToTable(self, table):
        y = len(table)
        x = len(table[0])
        for i in range(x):
            table[0][i] = 'W'
            table[y-1][i] ='W'

        for j in range(y):
            table[j][0] = 'W'
            table[j][x-1] = 'W'

    def addObstacle(self, y, x, table):
        initialX = int(x*self.RATIO)
        initialY = int(y*self.RATIO)
        obstacleRay = self.OBSTACLE_WIDTH / 2

        table[initialY][initialX] = 'W'

        for i in range(len(table)):
            for j in range(len(table[0])):
                deltaX = (x-j/self.RATIO)
                deltaY = (y-i/self.RATIO)
                if deltaX**2+deltaY**2 < obstacleRay**2 :
                    table[i][j]= 'W'

    def addSpacing(self, table):
        robotRay = self.ROBOT_LENGHT/2
        for i in range(len(table)):
            for j in range(len(table[0])):
                if table[i][j] is 'W':

                    for k in range(len(table)):
                        for l in range(len(table[0])):
                            if table[k][l] is not 'W' and table[k][l] is not 'o':
                                deltaX = (l/self.RATIO - j / self.RATIO)
                                deltaY = (k/self.RATIO - i / self.RATIO)
                                if deltaX**2+deltaY**2 < robotRay**2 :
                                    table[k][l] = 'o'

    def movementsInCm(self, cellMovements):
        cmMovements = []
        for i in cellMovements:
            cmMovements.append((self.coordToCentimeters(i[0]), self.coordToCentimeters(i[1])))
        return cmMovements

    def getTestTable(self):
        testTable = self.createTable(self.xCells, self.yCells)

        self.addWallsToTable(testTable)
        self.addObstacle(50, 50, testTable)
        self.addObstacle(50, 130, testTable)

        self.addSpacing(testTable)

        cellMovements = astar(testTable, (self.centimetersToCoords(30), self.centimetersToCoords(30)),
                                         (self.centimetersToCoords(70), self.centimetersToCoords(180)))

        return self.movementsInCm(cellMovements)


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
