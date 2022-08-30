import math
from VOBJ import createVector

class Projectile:
	def __init__(self, x, y, dir, vel):
		self.pos = createVector(x, y)
		self.facing = dir
		self.vel = createVector(vel * math.cos(dir), vel * math.sin(dir))

	def update(self):
		self.pos.add(self.vel)

	def show(self): pass