import math
from VOBJ import createVector

INFINITY = float("inf")


class sNode:
    def __init__(self, pos, nType, isObst, hasVis, GG, GL, parent):
        self.bObstacle = isObst
        self.bVisited = hasVis
        self.fGlobalGoal = GG
        self.fLocalGoal = GL
        self.x = pos[0]
        self.y = pos[1]
        self.Neighbours = []
        self.parent = parent
        self.nType = nType

    def __repr__(self):
        return f'({self.x}, {self.y})'


class PathfindingBoard:
    def __init__(self, gw: int):
        self.nodeStart = None
        self.nodeEnd = None
        self.grid_size = gw
        self.nodeGrid = []
        self.distance = lambda a, b: math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
        self.heuristic = lambda a, b: self.distance(a, b)

    def __find_node_by_coord(self, x, y):  # arr: nodeGrid, param: set(x, y)
        for idx, node in enumerate(self.nodeGrid):
            if {node.x, node.y} == {x, y}:
                return idx
        return False

    def createGrid(self, cellMap: list, cellSize) -> None:
        """
        Converts all cells in map to nodes for pathfinding
        :param cellMap: List of all cells in map
        """
        for idx, cell in enumerate(cellMap):

            x, y = (idx % self.grid_size) * cellSize, (idx // self.grid_size) * cellSize

            if cell != 2:
                self.nodeGrid.append(sNode((x + cellSize/2, y + cellSize/2), 0, False, False, 0.0, 0.0, None))

    def connect_nodes(self, cellSize):
        """
        Loops over all nodes and adds neighbours to walkable nodes
        """
        for _, node in enumerate(self.nodeGrid):
            cell = createVector(node.x // cellSize, node.y // cellSize)

            if cell.y > 0:  # if, can check up
                aboveIDX = self.__find_node_by_coord(cell.y - 1, cell.x)
                if aboveIDX: node.Neighbours.append(self.nodeGrid[aboveIDX])
            if cell.y < self.grid_size - 1:  # if, can check down
                belowIDX = self.__find_node_by_coord(cell.y - 1, cell.x)
                if belowIDX: node.Neighbours.append(self.nodeGrid[belowIDX])
            if cell.x < self.grid_size - 1:  # if, can check right
                rightIDX = self.__find_node_by_coord(cell.y - 1, cell.x)
                if rightIDX: node.Neighbours.append(self.nodeGrid[rightIDX])
            if cell.x > 0:  # if, can check left
                leftIDX = self.__find_node_by_coord(cell.y - 1, cell.x)
                if leftIDX: node.Neighbours.append(self.nodeGrid[leftIDX])

    def Solve_AStar(self):
        """
        calculates the shortest path between two sNode objects and stores in parent node from endNode
        """
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.nodeGrid[y][x].bVisited = False
                self.nodeGrid[y][x].fGlobalGoal = INFINITY
                self.nodeGrid[y][x].fLocalGoal = INFINITY
                self.nodeGrid[y][x].parent = None

        nodeCurrent = self.nodeStart
        self.nodeStart.fLocalGoal = 0.0
        self.nodeStart.fGlobalGoal = self.heuristic(self.nodeStart, self.nodeEnd)

        listNotTestedNodes = [self.nodeStart]

        while len(listNotTestedNodes) > 0:
            listNotTestedNodes.sort(key=lambda x: x.fGlobalGoal, reverse=True)  # sort based on global goal attribute

            while len(listNotTestedNodes) > 0 and listNotTestedNodes[0].bVisited:
                listNotTestedNodes.pop(0)

            if len(listNotTestedNodes) == 0: break

            nodeCurrent = listNotTestedNodes[0]
            nodeCurrent.bVisited = True

            for _, nodeNeighbour in enumerate(nodeCurrent.Neighbours):
                if not nodeNeighbour.bVisited and not nodeNeighbour.bObstacle:
                    listNotTestedNodes.append(nodeNeighbour)

                currentHeuristicDist = self.distance(nodeCurrent, nodeNeighbour)
                fPossiblyLowerGoal = nodeCurrent.fLocalGoal + currentHeuristicDist

                if fPossiblyLowerGoal < nodeNeighbour.fLocalGoal:
                    nodeNeighbour.parent = nodeCurrent
                    nodeNeighbour.fLocalGoal = fPossiblyLowerGoal

                    currentHeuristicDist = self.heuristic(nodeNeighbour, self.nodeEnd)
                    nodeNeighbour.fLocalGoal = currentHeuristicDist

    def getPath(self) -> list:
        """
        returns a list of coordinates for the enemy to travel to.
        """
        path = []

        if self.nodeEnd is not None:
            p = self.nodeEnd
            while p.parent is not None:
                path.append((p.x, p.y))
                p = p.parent
                if p.parent: p.type = 4

        return path
