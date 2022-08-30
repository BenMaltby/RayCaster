from VOBJ import createVector
from GenerateChunkMapFromImage import CHUNKSIZE, DIMENSIONS, coordToIDX
from MapProcessing import CELLSIZE
import pygame
import math

RADIAN = math.pi/180  # used for degree to radian conversion
GUNMODEL = [(500,800), (500,700), (560,590), (640,590), (700,700), (700,800)]  # coordinates of gun model


class Turret:
	def __init__(self, x, y, dir, deg, step, col):
		"""Definition of player object

		Parameters:
			x: starting x coordinate of player
			y: starting y coordinate of player
			dir: angle that the player is looking in
			deg: the degree of vision of player
			step: angle(degrees) increment that each ray is shot
			col: Color of Ray if used in 2D perspective
		"""
		self.pos = createVector(x, y)
		self.facing = dir * RADIAN
		self.angleOfVision = deg
		self.step = step
		self.col = col
		self.rayData = []  # Holds Ray coordinates
		self.shooting = False
		self.MapCell = []  # Players map cell coordinate (x: 0 - 79, y: 0 - 79)

	def Check_Collision(self, Map):
		"""Looks up cell type in Map to check if player is in collision with wall"""

		self.MapCell = [self.pos.x // CELLSIZE, self.pos.y // CELLSIZE]  # calculates map cell of new player position

		if 0 < self.pos.x < DIMENSIONS*CHUNKSIZE:  # if player is withing bounds of map
			if 0 < self.pos.y < DIMENSIONS*CHUNKSIZE:

				if Map[int(coordToIDX(self.MapCell[0], self.MapCell[1]))] == 2:  # if players new position is withing wall tile
					return True

				return False  # if not in wall tile, then not in collision

		return True  # if player not in wall tile but leaves bounds of map then return in collision

	# amount = speed of player in pixels
	def Move_LEFT(self, amount):  # moves player left based on facing direction
		self.pos.x += amount * math.cos(self.facing - math.pi / 2)
		self.pos.y += amount * math.sin(self.facing - math.pi / 2)

	def Move_RIGHT(self, amount):  # moves player right based on facing direction
		self.pos.x += amount * math.cos(self.facing + math.pi / 2)
		self.pos.y += amount * math.sin(self.facing + math.pi / 2)

	def Move_UP(self, amount):  # moves player forward based on facing direction
		self.pos.x += amount * math.cos(self.facing)
		self.pos.y += amount * math.sin(self.facing)

	def Move_DOWN(self, amount):  # moves player backwards based on facing direction
		self.pos.x += amount * math.cos(self.facing - math.pi)
		self.pos.y += amount * math.sin(self.facing - math.pi)

	def showWeapon(self, screen, b):
		"""Displays weapon models in idle and shooting state"""

		if self.shooting:  # draw gun with flash if shooting
			pygame.draw.rect(screen, (255, 158, 13), pygame.Rect(475, 475, 250, 250))  # draw flash
			# pygame.draw.circle(screen, (255, 138, 18), (600, 600), 100)
			pygame.draw.polygon(screen, (150*b*3,150*b*3,150*b*3), GUNMODEL)  # draw brighter gun model

		else:  # draw dark gun model no flash
			pygame.draw.polygon(screen, (150*b,150*b,150*b), GUNMODEL)

	def fireRays(self, screen, tConstants: list, numOfRays):
		"""Calculates Ray coordinates from player position and looking angle"""

		# pygame.draw.circle(screen, self.col, (self.pos.x, self.pos.y), 5)  # draw player in 2D
		self.rayData.clear()  # remove old rays

		for idx in range(int(numOfRays)):
			x = tConstants[idx][1] * math.cos(self.facing - tConstants[idx][0]) + self.pos.x  # constants are used for efficiency
			y = tConstants[idx][1] * math.sin(self.facing - tConstants[idx][0]) + self.pos.y
			# pygame.draw.line(screen, self.col, (self.pos.x, self.pos.y), (x, y))
			self.rayData.append((x, y))  # store as coordinate tuple


def thetaOffsetConstants(numOfRays, distFromPlane, widthOfPlane):
	"""Calculates the offset angles from facing to save efficieny at run time"""

	raySpacing = widthOfPlane / numOfRays  # angle inbetween each ray
	halfWidth = widthOfPlane / 2  # Rays are fired at invisible plane, but half width of plane is required

	TOC = []  # Theta Offset Constants

	for idx in range(int(numOfRays)):  # do for each ray
		theta = math.atan2(halfWidth - (raySpacing * idx), distFromPlane)  # calculate angle based on ray being fired at invisible plane
		TOC.append((theta, distFromPlane / math.cos(theta)))

	return TOC, numOfRays  # num of rays doesn't change so calculated before