import pygame
from VOBJ import createVector

WIDTH = 800


class Tile:
    def __init__(self, name, col):
        self.name = name
        self.colour = col


MapMaterials = {
    0: Tile('Empty', (0, 0, 0)),
    1: Tile('Floor', (255, 255, 255)),
    2: Tile('Wall', (163, 65, 47)),
    3: Tile('Water', (0, 0, 255))
}

Map = [[2, 2, 2, 2, 2, 2, 2, 2],
       [2, 1, 1, 1, 1, 1, 1, 2],
       [2, 1, 1, 1, 1, 1, 1, 2],
       [2, 1, 1, 1, 1, 1, 1, 2],
       [2, 1, 1, 1, 1, 1, 1, 2],
       [2, 2, 2, 1, 1, 1, 1, 2],
       [0, 0, 2, 1, 1, 1, 1, 2],
       [0, 0, 2, 2, 2, 2, 2, 2]]

CELLSIZE = WIDTH / len(Map)


def renderMap2D(screen):
    b = 1
    for y, row in enumerate(Map):
        for x, col in enumerate(row):
            pos = createVector(x * CELLSIZE, y * CELLSIZE)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pos.x, pos.y, CELLSIZE, CELLSIZE))
            pygame.draw.rect(screen, MapMaterials[col].colour, pygame.Rect(pos.x+b, pos.y+b, CELLSIZE-b*2, CELLSIZE-b*2))
