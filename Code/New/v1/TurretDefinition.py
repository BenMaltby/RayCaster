from VOBJ import createVector
import pygame
import math

RADIAN = math.pi/180

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

	def Check_Collision(self, mapData, cellSize):
		cell = createVector(int(self.pos.x//cellSize), int(self.pos.y//cellSize))
		if mapData[cell.y][cell.x] == 2:
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

	def fireRays(self, screen, distFromPlane, widthOfPlane):
		# # pygame.draw.circle(screen, self.col, (self.pos.x, self.pos.y), 5)
		# self.rayData.clear()
		# for i in range(int(self.angleOfVision//self.step)):
		# 	x = self.distance*math.cos(self.facing + (((i * self.step) - (self.angleOfVision)//2) * RADIAN)) + self.pos.x
		# 	y = self.distance*math.sin(self.facing + (((i * self.step) - (self.angleOfVision)//2) * RADIAN)) + self.pos.y
		# 	# pygame.draw.line(screen, self.col, (self.pos.x, self.pos.y), (x, y))
		# 	self.rayData.append((x, y))


		# pygame.draw.circle(screen, self.col, (self.pos.x, self.pos.y), 5)
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
