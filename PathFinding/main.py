# NOT PART OF FINAL PROJECT JUST DEMO OF A* FOR LEARNING

import pygame
import math

WIDTH = 580
HEIGHT = 400
FPS = 30
CELLSIZE = 20
GRIDWIDTH = WIDTH // CELLSIZE
GRIDHEIGHT = HEIGHT // CELLSIZE
INFINITY = float("inf")

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("a* Pathfinding")
clock = pygame.time.Clock()


class sNode:
    def __init__(self, pos, type, isObst, hasVis, GG, GL, parent):
        self.bObstacle = isObst
        self.bVisited = hasVis
        self.fGlobalGoal = GG
        self.fLocalGoal = GL
        self.x = pos[0]
        self.y = pos[1]
        self.Neighbours = []
        self.parent = parent
        self.type = type

    def __repr__(self):
        return f'({self.x}, {self.y})'


nodeStart = None
nodeEnd = None


def createGrid(w, h) -> list:
    nodeGrid = []

    for y in range(GRIDHEIGHT):
        temp = []
        for x in range(GRIDWIDTH):
            temp.append(sNode((x, y), 0, False, False, 0.0, 0.0, None))

        nodeGrid.append(temp)

    return nodeGrid


def displayGrid(screen, grid):
    b = 0.5
    screen.fill(BLACK)
    for y in range(len(grid)):
        for x in range(len(grid[y])):

            # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE), 1)

            if grid[y][x].bVisited == True and grid[y][x].type != 1 and grid[y][x].type != 2:
                pygame.draw.rect(screen, (0, 255, 255),
                                 pygame.Rect((x * CELLSIZE) + b, (y * CELLSIZE) + b, CELLSIZE - b / 2,
                                             CELLSIZE - b / 2))

            if grid[y][x].type == 0:
                pygame.draw.rect(screen, (255, 255, 255),
                                 pygame.Rect((x * CELLSIZE) + b, (y * CELLSIZE) + b, CELLSIZE - b / 2,
                                             CELLSIZE - b / 2))

            if grid[y][x].type == 1:
                pygame.draw.rect(screen, (0, 255, 0),
                                 pygame.Rect((x * CELLSIZE) + b, (y * CELLSIZE) + b, CELLSIZE - b / 2,
                                             CELLSIZE - b / 2))

            if grid[y][x].type == 2:
                pygame.draw.rect(screen, (255, 0, 0),
                                 pygame.Rect((x * CELLSIZE) + b, (y * CELLSIZE) + b, CELLSIZE - b / 2,
                                             CELLSIZE - b / 2))

            if grid[y][x].type == 3:
                pygame.draw.rect(screen, (50, 50, 50),
                                 pygame.Rect((x * CELLSIZE) + b, (y * CELLSIZE) + b, CELLSIZE - b / 2,
                                             CELLSIZE - b / 2))

            if grid[y][x].type == 4:
                pygame.draw.rect(screen, (160, 0, 255),
                                 pygame.Rect((x * CELLSIZE) + b, (y * CELLSIZE) + b, CELLSIZE - b / 2,
                                             CELLSIZE - b / 2))


def changeGrid(x, y, type, grid):
    global nodeStart, nodeEnd
    coord = (x // CELLSIZE, y // CELLSIZE)

    if type == 1 and nodeStart == None:
        grid[coord[1]][coord[0]].type = type
        nodeStart = grid[coord[1]][coord[0]]

    elif type == 2 and nodeEnd == None:
        grid[coord[1]][coord[0]].type = type
        nodeEnd = grid[coord[1]][coord[0]]

    elif type == 0:
        if grid[coord[1]][coord[0]].type == 1:
            nodeStart = None
        elif grid[coord[1]][coord[0]].type == 2:
            nodeEnd = None
        elif grid[coord[1]][coord[0]].type == 3:
            grid[coord[1]][coord[0]].bObstacle = False

        grid[coord[1]][coord[0]].type = type

    elif type == 3:
        grid[coord[1]][coord[0]].type = type
        grid[coord[1]][coord[0]].bObstacle = True


def connect_nodes(nodeGrid):
    for y in range(GRIDHEIGHT):
        for x in range(GRIDWIDTH):

            if y > 0:
                nodeGrid[y][x].Neighbours.append(nodeGrid[y - 1][x])
            # if y > 0 and x < GRIDWIDTH - 1:
            #     nodeGrid[y][x].Neighbours.append(nodeGrid[y - 1][x + 1])
            if y < GRIDHEIGHT - 1:
                nodeGrid[y][x].Neighbours.append(nodeGrid[y + 1][x])
            # if y < y < GRIDHEIGHT - 1 and x < GRIDWIDTH - 1:
            #     nodeGrid[y][x].Neighbours.append(nodeGrid[y + 1][x + 1])
            if x < GRIDWIDTH - 1:
                nodeGrid[y][x].Neighbours.append(nodeGrid[y][x + 1])
            # if x > 0 and y < GRIDHEIGHT - 1:
            #     nodeGrid[y][x].Neighbours.append(nodeGrid[y + 1][x - 1])
            if x > 0:
                nodeGrid[y][x].Neighbours.append(nodeGrid[y][x - 1])
            # if x > 0 and y > 0:
            #     nodeGrid[y][x].Neighbours.append(nodeGrid[y - 1][x - 1])

    return nodeGrid


distance = lambda a, b: math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
heuristic = lambda a, b: distance(a, b)


def Solve_AStar(nodeGrid: list[list[sNode]]):
    global nodeStart, nodeEnd

    for y in range(GRIDHEIGHT):
        for x in range(GRIDWIDTH):
            nodeGrid[y][x].bVisited = False
            nodeGrid[y][x].fGlobalGoal = INFINITY
            nodeGrid[y][x].fLocalGoal = INFINITY
            nodeGrid[y][x].parent = None

    nodeCurrent = nodeStart
    nodeStart.fLocalGoal = 0.0
    nodeStart.fGlobalGoal = heuristic(nodeStart, nodeEnd)

    listNotTestedNodes = []
    listNotTestedNodes.append(nodeStart)

    while len(listNotTestedNodes) > 0:
        listNotTestedNodes.sort(key=lambda x: x.fGlobalGoal, reverse=True)

        while len(listNotTestedNodes) > 0 and listNotTestedNodes[0].bVisited:
            listNotTestedNodes.pop(0)

        if len(listNotTestedNodes) == 0: break

        nodeCurrent = listNotTestedNodes[0]
        nodeCurrent.bVisited = True

        for idx, nodeNeighbour in enumerate(nodeCurrent.Neighbours):
            if not nodeNeighbour.bVisited and not nodeNeighbour.bObstacle:
                listNotTestedNodes.append(nodeNeighbour)

            fPossiblyLowerGoal = nodeCurrent.fLocalGoal + distance(nodeCurrent, nodeNeighbour)

            if fPossiblyLowerGoal < nodeNeighbour.fLocalGoal:
                nodeNeighbour.parent = nodeCurrent
                nodeNeighbour.fLocalGoal = fPossiblyLowerGoal

                nodeNeighbour.fLocalGoal = nodeNeighbour.fLocalGoal = heuristic(nodeNeighbour, nodeEnd)


def showPath(nodeGrid: list[list[sNode]]):
    global nodeEnd

    for y in range(GRIDHEIGHT):
        for x in range(GRIDWIDTH):
            if nodeGrid[y][x].type == 4:
                nodeGrid[y][x].type = 0

    if nodeEnd != None:
        p = nodeEnd
        while p.parent != None:
            # pygame.draw.rect(screen, (160, 0, 255), pygame.Rect(p.x * CELLSIZE, p.y * CELLSIZE, CELLSIZE, CELLSIZE))
            p = p.parent
            if p.parent: p.type = 4


def main():
    global nodeStart, nodeEnd

    grid_of_nodes = createGrid(GRIDWIDTH, GRIDHEIGHT)
    grid_of_nodes = connect_nodes(grid_of_nodes)

    running = True
    while running:

        # 1 Process input/events
        clock.tick(FPS)
        for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
            keysPressed = pygame.key.get_pressed()  # inputs
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and keysPressed[pygame.K_q]:
                mVec = pygame.mouse.get_pos()
                changeGrid(mVec[0], mVec[1], 0, grid_of_nodes)

            if event.type == pygame.MOUSEBUTTONDOWN and keysPressed[pygame.K_s]:
                mVec = pygame.mouse.get_pos()
                changeGrid(mVec[0], mVec[1], 1, grid_of_nodes)

            if event.type == pygame.MOUSEBUTTONDOWN and keysPressed[pygame.K_e]:
                mVec = pygame.mouse.get_pos()
                changeGrid(mVec[0], mVec[1], 2, grid_of_nodes)

            if event.type == pygame.MOUSEBUTTONDOWN and keysPressed[pygame.K_w]:
                mVec = pygame.mouse.get_pos()
                changeGrid(mVec[0], mVec[1], 3, grid_of_nodes)

            if keysPressed[pygame.K_p]:
                if nodeStart and nodeEnd: Solve_AStar(grid_of_nodes)
                showPath(grid_of_nodes)

        displayGrid(screen, grid_of_nodes)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
