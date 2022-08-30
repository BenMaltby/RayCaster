import pygame
from Chunk_Struct import ChunkSystem
from GenerateChunkMapFromImage import DIMENSIONS, CHUNKSIZE, MapTile
import math

WIDTH = 1200  # Width in pixels
HEIGHT = 800  # Height in pixels

# class Tile:
#     def __init__(self, name, col):
#         self.name = name
#         self.colour = col
#
#
# MapMaterials = {
#     0: Tile('Empty', (0, 0, 0)),
#     1: Tile('Floor', (20, 20, 20)),
#     2: Tile('Wall', (50, 50, 50)),  # (163, 65, 47)
#     3: Tile('Slime', (0, 255, 0))
# }

CELLSIZE = HEIGHT // DIMENSIONS  # width and height of cell in pixels


def renderMap2D(screen):
    """Used to render the players view from a birds eye perspective"""
    pass
    # b = 0
    # for y, row in enumerate(Map):
    #     for x, col in enumerate(row):
    #         pos = createVector(x * CELLSIZE, y * CELLSIZE)
    #         pygame.draw.rect(screen, MapMaterials[col].colour,
    #                          pygame.Rect(pos.x + b, pos.y + b, CELLSIZE - b * 2, CELLSIZE - b * 2))


# def MiniMap2D(screen, mmWidth, Player, offset, MapChunks):
#     mmCellSize = mmWidth / DIMENSIONS
#
#     for i in range(DIMENSIONS*DIMENSIONS):
#         x = i % DIMENSIONS
#         y = i // DIMENSIONS
#         pos = createVector(x * mmCellSize, y * mmCellSize)
#         PlayerChunkData = MapChunks.Query(MapTile(x, y), 0)
#         PlayerCellIndex = (y // (DIMENSIONS / CHUNKSIZE)) * CHUNKSIZE + (
#                     x // (DIMENSIONS / CHUNKSIZE))
#         col = PlayerChunkData[int(PlayerCellIndex)].tile
#         pygame.draw.rect(screen, MapMaterials[col].colour,
#                          pygame.Rect(pos.x + offset[0], pos.y + offset[1], mmCellSize, mmCellSize))
#
#     px, py = (Player.pos.x/HEIGHT)*mmWidth + offset[0], (Player.pos.y/HEIGHT)*mmWidth + offset[1]
#     pygame.draw.line(screen, (255, 0, 0), (px, py), (mmWidth*0.05*math.cos(Player.facing)+px, mmWidth*0.05*math.sin(Player.facing)+py))
#     pygame.draw.circle(screen, (0, 255, 0), (px, py), mmWidth*0.01)


def renderMap3D(screen, distanceSegmentData, maxDistance, sb=1, wb=0.05, flash=15, isShooting=False) -> None:
    """Function that takes distance to wall data from rays and constructs a 3D scene

    Parameters:
        distanceSegmentData: list of all distances of all rays to all walls in view
        maxDistance: distance used for calculating shadows
        sb: (SceneBrightness) used for changing brightness of sky and floor
        wb: (WallBrightness) used for changing brightness of walls
        flash: changes brightness of each object when gun is shot
        isShooting: used to choose which amount of flash to use
    """
    if distanceSegmentData:  # if we are looking at any walls
        pygame.draw.rect(screen, (135 * sb, 206 * sb, 235 * sb), pygame.Rect(0, 0, WIDTH, HEIGHT / 2))  # draw sky
        pygame.draw.rect(screen, (120 * sb, 120 * sb, 120 * sb), pygame.Rect(0, HEIGHT / 2, WIDTH, HEIGHT / 2))  # draw floor

        columnWidth = WIDTH / len(distanceSegmentData)  # calculate width of each column that makes up the walls

        for idx, Data in enumerate(distanceSegmentData):  # loop over each distance from wall

            # perc is a calculation for a percentage of distance as a percentage (long - small)distance maps to (dark - light)brightness
            # choose how much flash to use if gun is shooting (flash) or (flash/3)
            if not isShooting: perc = 1 - ((Data[0] / maxDistance) * flash)
            else: perc = 1 - ((Data[0] / maxDistance) * (flash / 3))

            perc = 0 if perc < 0 else perc  # make sure perc can't go below 0

            columnHeight = (CELLSIZE*2 * 800) / Data[0] if Data[0] > 0 else 1200  # calculate how tall the wall column should be

            if columnHeight > 0 and Data[0] <= maxDistance:  # if the column is tall enough and the wall is within viewing distance

                # Vertical walls are drawn darker than Horizontal walls to make them more distinguishable
                if Data[1] == 'V':
                    col = (46 * perc * wb, 46 * perc * wb, 46 * perc * wb)  # calculate colour with brightness and shadows
                    # draw the column
                    pygame.draw.rect(screen, col, pygame.Rect(idx * columnWidth, HEIGHT/2 - columnHeight/2, columnWidth+1, columnHeight))

                # Horizontal walls are drawn lighter than Vertical walls to make them more distinguishable
                elif Data[1] == 'H':
                    col = (112 * perc * wb, 112 * perc * wb, 112 * perc * wb)
                    # draw the column
                    pygame.draw.rect(screen, col, pygame.Rect(idx * columnWidth, HEIGHT/2 - columnHeight/2, columnWidth+1, columnHeight))

                else:  # this should never happen but was included for precaution
                    raise Exception("SOME HOW THE WALL HAS NO ORIENTATION")


def render2DWallLines(screen, edgeChunkMap: ChunkSystem, Player, showChunks=True):

    r = 4
    pygame.draw.circle(screen, (0,255,0), (Player.pos.x, Player.pos.y), r)
    pygame.draw.line(screen, (255,0,0), (Player.pos.x, Player.pos.y), (r*2*math.cos(Player.facing)+Player.pos.x, r*2*math.sin(Player.facing)+Player.pos.y))

    for y in range(DIMENSIONS//CHUNKSIZE):
        for x in range(DIMENSIONS//CHUNKSIZE):

            lineData = edgeChunkMap.Query(MapTile(x, y), 0)

            if showChunks:
                temp = CELLSIZE*CHUNKSIZE
                pygame.draw.rect(screen, (10, 10, 10), pygame.Rect(x*temp, y*temp, temp, temp), 1)

            # for i, lineSegmentList in enumerate(lineData):
            #     lineSegment = lineSegmentList.edgeData
            #     pygame.draw.line(screen, lineSegment.col, (lineSegment.x1, lineSegment.y1), (lineSegment.x2, lineSegment.y2))

            if lineData:
                for i, lineSegment in enumerate(lineData[0].edgeData):
                    pygame.draw.line(screen, lineSegment.col, (lineSegment.x1, lineSegment.y1), (lineSegment.x2, lineSegment.y2))


def render2DRawChunkedGridData(screen, Map: ChunkSystem, cs):

    for cy in range(DIMENSIONS//CHUNKSIZE):
        for cx in range(DIMENSIONS//CHUNKSIZE):

            cellData = Map.Query(MapTile(cx, cy), 0)

            for i, cell in enumerate(cellData):

                x, y = i % CHUNKSIZE, i // CHUNKSIZE
                xoffset = (cx * CHUNKSIZE + x) * cs
                yoffset = (cy * CHUNKSIZE + y) * cs

                if cell.tile == 2:
                    pygame.draw.rect(screen, (120,120,120), pygame.Rect(xoffset, yoffset, cs, cs))

                elif cell.tile == 1:
                    pygame.draw.rect(screen, (255,255,255), pygame.Rect(xoffset, yoffset, cs, cs))



def render2DRawGridData(screen, cellArray):

    for idx, cell in enumerate(cellArray):

        x, y = idx % DIMENSIONS, idx // DIMENSIONS

        if cell == (0, 0, 0):
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x*CELLSIZE,y*CELLSIZE, CELLSIZE, CELLSIZE))

        elif cell == (255, 255, 255):
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(x*CELLSIZE,y*CELLSIZE, CELLSIZE, CELLSIZE))