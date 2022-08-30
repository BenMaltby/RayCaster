from VOBJ import createVector
from Chunk_Struct import ChunkSystem
from GenerateChunkMapFromImage import MapTile, CHUNKSIZE, DIMENSIONS
import pygame
import math

RADIAN = math.pi/180
GUNMODEL = [(500,800), (500,700), (560,590), (640,590), (700,700), (700,800)]

class Turret:
	def __init__(self, x, y, dir, deg, step, col):
		self.pos = createVector(x, y)
		self.mouseRef = (400, 200)
		self.facing = dir * RADIAN
		self.angleOfVision = deg
		self.step = step
		self.col = col
		self.distance = 5000
		self.rayData = []
		self.shooting = False
		self.MapCell = []

	def Check_Collision(self, GridChunkMap: ChunkSystem):
		PlayerChunkData = GridChunkMap.Query(MapTile(self.MapCell[0], self.MapCell[1]), 0)
		PlayerCellIndex = (self.MapCell[1]//(DIMENSIONS/CHUNKSIZE)) * CHUNKSIZE + (self.MapCell[0]//(DIMENSIONS/CHUNKSIZE))
		if PlayerChunkData[PlayerCellIndex] == 2:
			return True
		return False

	def Move_LEFT(self, amount):
		self.pos.x += amount * math.cos(self.facing - math.pi / 2)
		self.pos.y += amount * math.sin(self.facing - math.pi / 2)

	def Move_RIGHT(self, amount):
		self.pos.x += amount * math.cos(self.facing + math.pi / 2)
		self.pos.y += amount * math.sin(self.facing + math.pi / 2)

	def Move_UP(self, amount):
		self.pos.x += amount * math.cos(self.facing)
		self.pos.y += amount * math.sin(self.facing)

	def Move_DOWN(self, amount):
		self.pos.x += amount * math.cos(self.facing - math.pi)
		self.pos.y += amount * math.sin(self.facing - math.pi)

	def update(self):
		self.pos.x = self.mouseRef[0]
		self.pos.y = self.mouseRef[1]

	def showWeapon(self, screen):
		if self.shooting:
			pygame.draw.rect(screen, (255, 158, 13), pygame.Rect(475, 475, 250, 250))
			# pygame.draw.circle(screen, (255, 138, 18), (600, 600), 100)
			pygame.draw.polygon(screen, (150,150,150), GUNMODEL)
		else:
			pygame.draw.polygon(screen, (150,150,150), GUNMODEL)

	def fireRays(self, screen, distFromPlane, widthOfPlane):
		# # pygame.draw.circle(screen, self.col, (self.pos.x, self.pos.y), 5)
		# self.rayData.clear()
		# for i in range(int(self.angleOfVision//self.step)):
		# 	x = self.distance*math.cos(self.facing + (((i * self.step) - (self.angleOfVision)//2) * RADIAN)) + self.pos.x
		# 	y = self.distance*math.sin(self.facing + (((i * self.step) - (self.angleOfVision)//2) * RADIAN)) + self.pos.y
		# 	# pygame.draw.line(screen, self.col, (self.pos.x, self.pos.y), (x, y))
		# 	self.rayData.append((x, y))


		pygame.draw.circle(screen, self.col, (self.pos.x, self.pos.y), 5)
		self.rayData.clear()
		numOfRays = int(self.angleOfVision//self.step)
		raySpacing = widthOfPlane / numOfRays
		halfWidth = widthOfPlane / 2

		# angle1 = math.atan2(halfWidth - (raySpacing * 0), distFromPlane)
		# angle2 = math.atan2(halfWidth - (raySpacing * 159), distFromPlane)
		# pygame.draw.line(screen, (255, 0, 0), ((distFromPlane / math.cos(angle1))*math.cos(self.facing-angle1)+self.pos.x, (distFromPlane / math.cos(angle1))*math.sin(self.facing-angle1)+self.pos.y),
		# 				 (((distFromPlane / math.cos(angle2))*math.cos(self.facing-angle2)+self.pos.x, (distFromPlane / math.cos(angle2))*math.sin(self.facing-angle2)+self.pos.y)))

		for idx in range(numOfRays):
			theta = math.atan2(halfWidth - (raySpacing * idx), distFromPlane)
			x = (distFromPlane / math.cos(theta)) * math.cos(self.facing - theta) + self.pos.x
			y = (distFromPlane / math.cos(theta)) * math.sin(self.facing - theta) + self.pos.y
			# pygame.draw.line(screen, self.col, (self.pos.x, self.pos.y), (x, y))
			self.rayData.append((x, y))
