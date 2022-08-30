import pygame
from Chunk_Struct import ChunkSystem
from GenerateChunkMapFromImage import DIMENSIONS, CHUNKSIZE, MapTile, coordToIDX
import math

# Sprite Casting Guides:
# https://lodev.org/cgtutor/raycasting3.html
# https://wynnliam.github.io/raycaster/news/tutorial/2019/04/03/raycaster-part-02.html
# https://www.youtube.com/watch?v=eBFOjriHMc8
# https://www.youtube.com/watch?v=w0Bm4IA-Ii8

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
	3: Tile('Slime', (0, 255, 0)),
	4: Tile('Ammo', (0, 255, 0)),
	5: Tile('Spawn', (234, 255, 0)),
	6: Tile('Med', (255,0,0)),
	7: Tile('Zombie Basic', (170,0,255)),
	10: Tile('Flashlight', (0,255,255)),
	11: Tile('star Tab', (0,0,255)),
	12: Tile('M_Gun_Item', (100,100,100)),
	13: Tile('Activate Zombies', (255, 100, 0)),
	14: Tile('End Level', (140, 70, 0)),
	17: Tile('Gatling Gun', (10, 70, 75)),
	18: Tile('mp5', (0, 96, 64))
}

CELLSIZE = HEIGHT // DIMENSIONS  # width and height of cell in pixels
CHUNKWIDTH = CHUNKSIZE * CELLSIZE  # Width of chunk in pixels
SECTORANGLE = math.tau / 16  # used in frustum culling to split view
RADIAN = math.pi / 180  # used for degree to radian conversion

def cullFrustum(player):
	"""Calculates Which chunks are in view of the player, so chunks outside of players vision(Frustum) aren't rendered"""

	pCoords = (int(player.pos.x // CHUNKWIDTH), int(player.pos.y // CHUNKWIDTH))  # Players chunk position
	finalCoords = [pCoords]  # stores all chunk coordinates in players view

	section = int((player.facing % math.tau) // SECTORANGLE)  # calculates which direction player is looking to know which chunks to render

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


def draw_wall_line(screen, columnWidth, heightBuffer, columnHeight, next_columnHeight, idx, col, check_next_column):

	line_width = int(abs((columnHeight-next_columnHeight)/2))

	if check_next_column and columnHeight - heightBuffer < next_columnHeight < columnHeight: 
		pygame.draw.line(screen, col, ((idx+1) * columnWidth, (HEIGHT / 2 - columnHeight / 2) + line_width/2),  # top line
										((idx+2) * columnWidth, (HEIGHT / 2 - next_columnHeight / 2) + line_width/2), line_width)

		pygame.draw.line(screen, col, ((idx+1) * columnWidth, (HEIGHT / 2 + columnHeight / 2) - line_width/2),  # bottom line
										((idx+2) * columnWidth, (HEIGHT / 2 + next_columnHeight / 2) - line_width/2), line_width)

	elif check_next_column and columnHeight + heightBuffer > next_columnHeight > columnHeight: 
		pygame.draw.line(screen, col, (idx * columnWidth, (HEIGHT / 2 - columnHeight / 2) + line_width/2),  # top line
										((idx+1) * columnWidth, (HEIGHT / 2 - next_columnHeight / 2) + line_width/2), line_width)

		pygame.draw.line(screen, col, (idx * columnWidth, (HEIGHT / 2 + columnHeight / 2) - line_width/2),  # bottom line
										((idx+1) * columnWidth, (HEIGHT / 2 + next_columnHeight / 2) - line_width/2), line_width)


def renderMap2D(screen, Map, Player):
	"""Used to render the players view from a birds eye perspective"""
	vwo2 = (1.5 * CHUNKSIZE) / 2  # 1.5 chunks either side of the player in 2D view  |  vwo2(view width over 2)
	playerCell = (Player.pos.x / CELLSIZE, Player.pos.y / CELLSIZE)  # floating point of cell coordinate
	spriteCoords = []

	for y in range(int(playerCell[1]) - int(vwo2), int(playerCell[1]) + int(vwo2)):  # loop from 1.5 chunks to the left and right
		for x in range(int(playerCell[0]) - int(vwo2), int(playerCell[0]) + int(vwo2)):

			idx = int(coordToIDX(x, y))  # calculate 1 dimensional index
			if 0 <= idx < 10_000 and 0 <= x < DIMENSIONS and 0 <= y < DIMENSIONS:  # if index and coordinates are within map
				tile = Map[idx]  # get stored tile type
				col = MapMaterials[tile].colour  # colour based on colour map

				scale = HEIGHT/CHUNKSIZE  # scale for resizing
				cx, cy = (HEIGHT/2) - ((playerCell[0] - x) * scale), (HEIGHT/2) - ((playerCell[1] - y) * scale)
				if tile != 4:  # if not AmmoBox
					pygame.draw.rect(screen, col, pygame.Rect(cx, cy, scale, scale))

				elif tile == 4:  # draw ammo crate box
					pygame.draw.rect(screen, MapMaterials[1].colour, pygame.Rect(cx, cy, scale, scale))  # draw floor tile and then ammo box on top
					spriteCoords.append((cx + scale/2, cy + scale/2, 4))
					# screen.blit(ammoBox_img, ((cx + scale/2) - int(ammoBox_img.get_width() / 2), (cy + scale/2) - int(ammoBox_img.get_height() / 2)))

				elif tile == 6:
					pygame.draw.rect(screen, MapMaterials[1].colour, pygame.Rect(cx, cy, scale, scale))  # draw floor tile and then ammo box on top
					spriteCoords.append((cx + scale/2, cy + scale/2, 6))

	return spriteCoords

rotate = lambda p, a: (p[0]*math.cos(a)+p[1]*math.sin(a), p[0]*(-math.sin(a))+p[1]*math.cos(a))

def renderMap3D(screen, player, z_system, distanceSegmentData, maxDistance, GSS, wb=0.05, sb=1, flash=15, *args) -> None:
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
		# pygame.draw.rect(screen, (135 * sb, 206 * sb, 235 * sb), pygame.Rect(0, 0, WIDTH, HEIGHT / 2))  # draw sky
		# pygame.draw.rect(screen, (120 * sb, 120 * sb, 120 * sb), pygame.Rect(0, HEIGHT / 2, WIDTH, HEIGHT / 2))  # draw floor

		columnWidth = WIDTH / len(distanceSegmentData)  # calculate width of each column that makes up the walls

		for idx, Data in enumerate(distanceSegmentData):  # loop over each distance from wall

			# perc is a calculation for a percentage of distance as a percentage (long - small)distance maps to (dark - light)brightness
			# choose how much flash to use if gun is shooting (flash) or (flash/3)
			if not player.shooting and not player.flashlight: perc = 1 - ((Data[0] / maxDistance) * flash)
			else: perc = 1 - ((Data[0] / maxDistance) * (flash / 2.5))

			perc = 0 if perc < 0 else perc  # make sure perc can't go below 0

			check_next_column, heightBuffer = idx < len(distanceSegmentData)-1, 30
			columnHeight = (CELLSIZE*2 * HEIGHT) / Data[0] if Data[0] > 0 else 1200  # calculate how tall the wall column should be
			if check_next_column: 
				next_columnHeight = (CELLSIZE*2 * HEIGHT) / distanceSegmentData[idx+1][0] if distanceSegmentData[idx+1][0] > 0 else 1200

			if columnHeight > 0 and Data[0] <= maxDistance:  # if the column is tall enough and the wall is within viewing distance

				# Vertical walls are drawn darker than Horizontal walls to make them more distinguishable
				if Data[1] == 'V':
					col = (46 * perc * wb, 46 * perc * wb, 46 * perc * wb)  # calculate colour with brightness and shadows
					if player.on_star: col = (args[2][0] * perc * wb, args[2][1] * perc * wb, args[2][2] * perc * wb)

					# draw the column
					pygame.draw.rect(screen, col, pygame.Rect(idx * columnWidth, (HEIGHT / 2 - columnHeight / 2), columnWidth + 1, columnHeight))

					# draw_wall_line(screen, columnWidth, heightBuffer, columnHeight, next_columnHeight, idx, col, check_next_column)

				# Horizontal walls are drawn lighter than Vertical walls to make them more distinguishable
				elif Data[1] == 'H':
					col = (112 * perc * wb, 112 * perc * wb, 112 * perc * wb)
					if player.on_star: col = (args[2][0] * perc * wb, args[2][1] * perc * wb, args[2][2] * perc * wb)

					# draw the column
					pygame.draw.rect(screen, col, pygame.Rect(idx * columnWidth, (HEIGHT / 2 - columnHeight / 2), columnWidth + 1, columnHeight))

					# draw_wall_line(screen, columnWidth, heightBuffer, columnHeight, next_columnHeight, idx, col, check_next_column)

				else:  # this should never happen but was included for precaution
					raise Exception("SOME HOW THE WALL HAS NO ORIENTATION")

		GSS.draw_sprites(screen, player, distanceSegmentData, columnWidth, z_system, *args)


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
	# pCell = (Player.pos.x//CELLSIZE, Player.pos.y//CELLSIZE)

	# loops over culled coordinates
	for idx, coord in enumerate(culledChunks):
		pygame.draw.rect(screen, (255,255,255), pygame.Rect(coord[0] * CHUNKWIDTH, coord[1] * CHUNKWIDTH, CHUNKWIDTH, CHUNKWIDTH), 1)


def renderMapAsImage(screen, img_of_map, Player):
	img_copy = pygame.transform.scale(img_of_map, (HEIGHT, HEIGHT))  # scale sprite based on calculation
	screen.blit(img_copy, (0,0))

	r = 4
	pygame.draw.circle(screen, (0,255,0), (Player.pos.x, Player.pos.y), r)
	pygame.draw.line(screen, (255,0,0), (Player.pos.x, Player.pos.y), (r*2*math.cos(Player.facing)+Player.pos.x, r*2*math.sin(Player.facing)+Player.pos.y))


def render2DRawChunkedGridData(screen, Map: ChunkSystem, cs):

	for cy in range(DIMENSIONS//CHUNKSIZE):
		for cx in range(DIMENSIONS//CHUNKSIZE):

			cellData = Map.Query(MapTile(cx, cy), 0)

			for i, cell in enumerate(cellData):

				x, y = i % CHUNKSIZE, i // CHUNKSIZE
				xoffset = (cx * CHUNKSIZE + x) * cs
				yoffset = (cy * CHUNKSIZE + y) * cs

				col = MapMaterials[cell.tile].colour
				pygame.draw.rect(screen, col, pygame.Rect(xoffset, yoffset, cs, cs))



def render2DRawGridData(screen, cellArray):

	for idx, cell in enumerate(cellArray):

		x, y = idx % DIMENSIONS, idx // DIMENSIONS

		col = MapMaterials[cell].colour
		pygame.draw.rect(screen, col, pygame.Rect(x*CELLSIZE,y*CELLSIZE, CELLSIZE, CELLSIZE))
