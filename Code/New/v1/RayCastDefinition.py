import pygame
from LineSegmentDefinition import lineSeg
from IntersectionDefinition import intersects
import math

RADIAN = math.pi/180


def CastRays(screen, turret, LevelWalls):
	# turret.mouseRef = pygame.mouse.get_pos()
	# turret.update()

	distanceSegmentData = []

	for y in range(len(turret.rayData)):
		playerLignSeg = lineSeg(turret.pos.x, turret.pos.y, turret.rayData[y][0], turret.rayData[y][1], 'H')
		currentIntersections = []

		for i in range(len(LevelWalls)):
			pointOfIntersection = intersects(playerLignSeg, LevelWalls[i])
			if pointOfIntersection:
				currentIntersections.append((pointOfIntersection, LevelWalls[i].orientation))
			else:
				currentIntersections.append(((playerLignSeg.x2, playerLignSeg.y2), 'H'))

		if currentIntersections:
			bestIntersection = []
			bestDist = 10_000_000
			for x, j in enumerate(currentIntersections):
				px = j[0][0] - turret.pos.x
				py = j[0][1] - turret.pos.y
				dist = math.sqrt(px * px + py * py)
				if dist < bestDist:
					bestDist = dist
					#angle = (((y * turret.step) - (turret.angleOfVision)//2) * RADIAN)
					angle = math.atan2(900 - (11.25 * y), 1100)
					#print(dist, angle, math.cos(angle))
					distanceSegmentData.append((dist * math.cos(angle), j[1]))  # dist * math.cos(angle)
					bestIntersection.append(j[0])
			del distanceSegmentData[y : len(distanceSegmentData)-1]

			# pygame.draw.line(screen, (255, 255, 255), (turret.pos.x, turret.pos.y),
			# 				 (bestIntersection[-1][0], bestIntersection[-1][1]))

	return distanceSegmentData