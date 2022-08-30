from VOBJ import createVector
from GenerateChunkMapFromImage import DIMENSIONS, coordToIDX
from MapProcessing import CELLSIZE, WIDTH, HEIGHT
import pygame
import math

RADIAN = math.pi/180  # used for degree to radian conversion
GUNMODEL = [(WIDTH*0.416,HEIGHT), (WIDTH*0.416,HEIGHT*0.875), (WIDTH*0.46,HEIGHT*0.7375), (WIDTH*0.53,HEIGHT*0.7375), (WIDTH*0.583,HEIGHT*0.875), (WIDTH*0.583,HEIGHT)]  # coordinates of gun model


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

		if 0 < self.pos.x < DIMENSIONS*CELLSIZE:  # if player is withing bounds of map
			if 0 < self.pos.y < DIMENSIONS*CELLSIZE:

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
			pygame.draw.rect(screen, (255, 158, 13), pygame.Rect(WIDTH*0.39583, HEIGHT*0.59375, WIDTH*0.208, HEIGHT*0.3125))  # draw flash
			# pygame.draw.circle(screen, (255, 138, 18), (600, 600), 100)
			pygame.draw.polygon(screen, ((150*b*2.5)%255,(150*b*2.5)%255,(150*b*2.5)%255), GUNMODEL)  # draw brighter gun model

		else:  # draw dark gun model no flash
			pygame.draw.polygon(screen, (150*b,150*b,150*b), GUNMODEL)

	def fireRays(self, screen, tConstants: list, numOfRays, threeDview=True):
		"""Calculates Ray coordinates from player position and looking angle"""

		if not threeDview:
			r, ho2 = 15, HEIGHT/2
			pygame.draw.circle(screen, self.col, (ho2, ho2), r)  # draw player in 2D
			pygame.draw.line(screen, (255,0,0), (ho2, ho2), (r*2*math.cos(self.facing)+ho2, r*2*math.sin(self.facing)+ho2))

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