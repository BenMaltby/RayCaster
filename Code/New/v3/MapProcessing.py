import pygame
from Chunk_Struct import ChunkSystem
from GenerateChunkMapFromImage import DIMENSIONS, CHUNKSIZE, MapTile, coordToIDX
import math

WIDTH = 1200  # Width in pixels
HEIGHT = 800  # Height in pixels

class Tile:
	def __init__(self, name, col):
		self.name = name
		self.colour = col

# stores map tile object and the associated colour
MapMaterials = {
	0: Tile('Empty', (0, 0, 0)),
	1: Tile('Floor', (20, 20, 20)),
	2: Tile('Wall', (50, 50, 50)),  # (163, 65, 47)
	3: Tile('Slime', (0, 255, 0))
}

CELLSIZE = HEIGHT // DIMENSIONS  # width and height of cell in pixels
CHUNKWIDTH = CHUNKSIZE * CELLSIZE  # Width of chunk in pixels
SECTORANGLE = math.tau / 16  # used in frustum culling to split view

def cullFrustum(player):
	"""Calculates Which chunks are in view of the player, so chunks outside of players vision(Frustum) aren't rendered"""

	pCoords = (int(player.pos.x // CHUNKWIDTH), int(player.pos.y // CHUNKWIDTH))  # Players chunk position
	finalCoords = [pCoords]  # stores all chunk coordinates in players view

	section = int((
							  player.facing % math.tau) // SECTORANGLE)  # calculates which direction player is looking to know which chunks to render

	# Ugly Check to generate chunk offsets
	# Diagram in Data folder for example: "Frustum_Culling_Diagram.png"
	if section in [0, 15]:
		offsets = [(0, -1), (1, -1), (1, 0), (0, 1), (1, 1)]
	elif section in [1, 2]:
		offsets = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
	elif section in [3, 4]:
		offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
	elif section in [5, 6]:
		offsets = [(1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
	elif section in [7, 8]:
		offsets = [(-1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
	elif section in [9, 10]:
		offsets = [(1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
	elif section in [11, 12]:
		offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0)]
	else:
		offsets = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]

	# finds new chunk coordinates from offset array
	for idx, offset in enumerate(offsets):
		finalCoords.append((pCoords[0] + offset[0], pCoords[1] + offset[1]))

	return finalCoords


def renderMap2D(screen, Map, Player):
	"""Used to render the players view from a birds eye perspective"""
	vwo2 = (3 * CHUNKSIZE) / 2  # 1.5 chunks either side of the player in 2D view  |  vwo2(view width over 2)
	playerCell = (Player.pos.x / CELLSIZE, Player.pos.y / CELLSIZE)  # floating point of cell coordinate

	for y in range(int(playerCell[1]) - int(vwo2), int(playerCell[1]) + int(vwo2)):  # loop from 1.5 chunks to the left and right
		for x in range(int(playerCell[0]) - int(vwo2), int(playerCell[0]) + int(vwo2)):

			idx = int(coordToIDX(x, y))  # calculate 1 dimensional index
			if 0 <= idx < 10_000 and 0 <= x < DIMENSIONS and 0 <= y < DIMENSIONS:  # if index and coordinates are within map
				tile = Map[idx]  # get stored tile type
				col = MapMaterials[tile].colour  # colour based on colour map

				scale = HEIGHT/CHUNKSIZE  # scale for resizing
				pygame.draw.rect(screen, col, pygame.Rect((HEIGHT/2) - ((playerCell[0] - x) * scale), (HEIGHT/2) - ((playerCell[1] - y) * scale), scale, scale))


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


def renderMap3D(screen, distanceSegmentData, maxDistance, wb=0.05, sb=1, flash=15, isShooting=False) -> None:
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
			else: perc = 1 - ((Data[0] / maxDistance) * (flash / 2.5))

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

	culledChunks = cullFrustum(Player)  # returns which chunks to get wall data from
	pCell = (Player.pos.x//CELLSIZE, Player.pos.y//CELLSIZE)

	# loops over culled coordinates
	for idx, coord in enumerate(culledChunks):
		pygame.draw.rect(screen, (255,255,255), pygame.Rect(coord[0] * CHUNKWIDTH, coord[1] * CHUNKWIDTH, CHUNKWIDTH, CHUNKWIDTH), 1)


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