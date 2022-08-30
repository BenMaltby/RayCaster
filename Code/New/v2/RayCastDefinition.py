import pygame
from LineSegmentDefinition import lineSeg
from IntersectionDefinition import intersects
from Chunk_Struct import ChunkSystem
from GenerateChunkMapFromImage import MapTile, CHUNKSIZE
from MapProcessing import CELLSIZE
import math

RADIAN = math.pi / 180  # used for degree to radian conversion
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


def CastRays(screen, turret, edgeSystem: ChunkSystem, tConstants, threeDview=True) -> list:
	"""Compares all the players fired rays to wall data in Map

	Parameters:
		screen: screen used in 2D View
		turret: reference of player for ray data and coordinates
		edgeSystem: holds chunk system of wall data to be Queried
		tConstants: constants from pre-calculated angles to remove fish-eye affect (distance * cos(angle))
		threeDview: draw 2D lines if False

	Returns:
		List of lengths of rays from player to the nearest walls
	"""

	distanceSegmentData = []  # all ray distances to be returned at the end
	WallData = []  # holds array of wall information to loop over
	culledChunks = cullFrustum(turret)  # returns which chunks to get wall data from

	# loops over culled coordinates
	for idx, coord in enumerate(culledChunks):
		wallsInChunk = edgeSystem.Query(MapTile(coord[0], coord[1]),
										0)  # Goes into chunk system and returns all wall data from culled chunk coordinates
		if wallsInChunk: WallData.append(wallsInChunk[0])  # only looks at chunk if it contains walls

	# loops over all rays fired by player
	for rayIDX in range(len(turret.rayData)):
		# everything works in line segments, so line segment between player and ray tip is created for calculation
		playerLignSeg = lineSeg(turret.pos.x, turret.pos.y, turret.rayData[rayIDX][0], turret.rayData[rayIDX][1], 'H')
		currentIntersections = []  # stores all ray-wall collisions to be sorted for closest distance

		for i, edge in enumerate(WallData):  # Goes over every chunk being checked
			for k in range(len(edge.edgeData)):  # looping over every wall in chunk
				Line = edge.edgeData[k]  # Line is the wall being checked
				pointOfIntersection = intersects(playerLignSeg, Line)  # passes line segments into line-line intersection equation

				if pointOfIntersection:
					currentIntersections.append((pointOfIntersection, Line.orientation))  # Add the point of intersection to be ordered
				else:  # if there is no wall in our view
					currentIntersections.append(((playerLignSeg.x2, playerLignSeg.y2), 'H'))  # add an intersection further away than view plane(raw ray)

		if currentIntersections:  # if we are seeing anything
			bestIntersection = []  # use for 2D View
			bestDist = 10_000_000  # set bestDist much further than any possible ray could be

			for xdx, intersection in enumerate(currentIntersections):  # loop over all wall intersection for that ray

				# find length of ray relative to (0, 0)
				px = intersection[0][0] - turret.pos.x
				py = intersection[0][1] - turret.pos.y
				dist = math.sqrt(px * px + py * py)  # calculate length of intersection

				if dist < bestDist:  # if we have found a closer wall,
					bestDist = dist  # set as new bestDist
					distanceSegmentData.append((dist * math.cos(tConstants[rayIDX][0]), intersection[1]))  # add the distance
					bestIntersection.append(intersection[0])  # put as best intersection for use in 2D View

			# remove any of the distances added to distanceSegmentData that weren't the best distances
			del distanceSegmentData[rayIDX: len(distanceSegmentData) - 1]

			if not threeDview:  # if 2D View, then use the best intersection to draw ray from player to wall
				pygame.draw.line(screen, (255, 255, 255), (turret.pos.x, turret.pos.y),
								 (bestIntersection[-1][0], bestIntersection[-1][1]))

	return distanceSegmentData
