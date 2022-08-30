# Only code that i didn't write is the actual Solve_AStar Method in the PathfindingBoard class and the essentials of the sNode object.

import math
from VOBJ import createVector
from Chunk_Struct import ChunkSystem

INFINITY = float("inf")


class sNode:
    def __init__(self, pos, nType, isObst, hasVis, GG, GL, parent):
        self.bObstacle = isObst
        self.bVisited = hasVis
        self.fGlobalGoal = GG
        self.fLocalGoal = GL
        self.x = pos[0]
        self.y = pos[1]
        self.pos = createVector(pos[0], pos[1])
        self.Neighbours = []
        self.parent = parent
        self.nType = nType

    def __repr__(self):
        return f'({self.x}, {self.y})'


class tempPoint:
    def __init__(self, x, y):
        self.pos = createVector(x, y)


class PathfindingBoard:
    def __init__(self, mapList: list, gw: int, cs: int):
        self.nodeStarts = []
        self.nodeEnd = None
        self.grid_size = gw
        self.cellSize = cs
        self.cellMap = mapList
        self.nodeGrid = ChunkSystem(cs)
        self.nodeArray = []
        self.enemyArray = []
        self.distance = lambda a, b: math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
        self.heuristic = lambda a, b: self.distance(a, b)
        self.createGrid()
        self.connect_nodes()

    def __find_node_by_coord(self, x, y):  # arr: nodeGrid, param: set(x, y)
        for idx, node in enumerate(self.nodeGrid):
            cell = createVector(node.x // self.cellSize, node.y // self.cellSize)
            if [cell.x, cell.y] == [x, y]:
                return idx
        return False

    def createGrid(self) -> None:
        """
        Converts all cells in map to nodes for pathfinding
        :param cellMap: List of all cells in map
        """
        for idx, cell in enumerate(self.cellMap):

            x, y = (idx % self.grid_size) * self.cellSize, (idx // self.grid_size) * self.cellSize

            if cell != 2:
                nodeOBJ = sNode((x + self.cellSize/2, y + self.cellSize/2), 0, False, False, 0.0, 0.0, None)
                self.nodeGrid.insert(nodeOBJ)
                self.nodeArray.append(nodeOBJ)

    def connect_nodes(self):
        """
        Loops over all nodes and adds neighbours to walkable nodes
        """
        for idx, node in enumerate(self.nodeArray):

            temp = []
            temp.extend(self.nodeGrid.Query(tempPoint(node.x, node.y - self.cellSize), 0))
            temp.extend(self.nodeGrid.Query(tempPoint(node.x + self.cellSize, node.y), 0))
            temp.extend(self.nodeGrid.Query(tempPoint(node.x, node.y + self.cellSize), 0))
            temp.extend(self.nodeGrid.Query(tempPoint(node.x - self.cellSize, node.y), 0))
            node.Neighbours.extend(temp)

    # A_Star Solver implementation in c++ translated into python from YouTube tutorial by Javidx9
    # YouTube video: https://www.youtube.com/watch?v=icZj67PTFhc
    # GitHub source code: https://github.com/OneLoneCoder/videos/blob/master/OneLoneCoder_PathFinding_AStar.cpp
    # lines 85 - 122
    def Solve_AStar(self, node_Start):
        """
        calculates the shortest path between two sNode objects and stores in parent node from endNode
        """
        for idx, node in enumerate(self.nodeArray):
            node.bVisited = False
            node.fGlobalGoal = INFINITY
            node.fLocalGoal = INFINITY
            node.parent = None

        nodeCurrent = node_Start
        node_Start.fLocalGoal = 0.0
        node_Start.fGlobalGoal = self.heuristic(node_Start, self.nodeEnd)

        listNotTestedNodes = [node_Start]

        while len(listNotTestedNodes) > 0:
            listNotTestedNodes.sort(key=lambda x: x.fGlobalGoal, reverse=True)  # sort based on global goal attribute

            while len(listNotTestedNodes) > 0 and listNotTestedNodes[0].bVisited:
                listNotTestedNodes.pop(0)

            if len(listNotTestedNodes) == 0: break

            nodeCurrent = listNotTestedNodes[0]
            nodeCurrent.bVisited = True

            for idx, nodeNeighbour in enumerate(nodeCurrent.Neighbours):
                if not nodeNeighbour.bVisited and not nodeNeighbour.bObstacle:
                    listNotTestedNodes.append(nodeNeighbour)

                fPossiblyLowerGoal = nodeCurrent.fLocalGoal + self.distance(nodeCurrent, nodeNeighbour)

                if fPossiblyLowerGoal < nodeNeighbour.fLocalGoal:
                    nodeNeighbour.parent = nodeCurrent
                    nodeNeighbour.fLocalGoal = fPossiblyLowerGoal

                    nodeNeighbour.fLocalGoal = nodeNeighbour.fLocalGoal = self.heuristic(nodeNeighbour, self.nodeEnd)

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

        return path[::-1][:-1]
