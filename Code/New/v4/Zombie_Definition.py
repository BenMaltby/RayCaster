from TurretDefinition import Turret
from VOBJ import createVector
from spriteDefinitions import base_zombie_img, base_zombie_hit, base_zombie_dead
from SpriteSystem import GameSpriteOBJ
from GenerateChunkMapFromImage import DIMENSIONS, coordToIDX
from MapProcessing import CELLSIZE
from aStar import sNode
from random import random
import VOBJ
import math
from pygame import time as pgTime

ZOMBIE_TYPES = {  # health, damage per second, sprite, speed, reach
	7: (100, 30, base_zombie_hit, 0.8, 18)  # regular Zombie
}


class Zombie:
	def __init__(self, x, y, args):
		self.pos = createVector(x, y)
		self.health = args[0]
		self.damage = args[1]
		self.sprite: GameSpriteOBJ = args[2]
		self.targets = []
		self.speed = args[3]
		self.reach = args[4]
		self.vel = createVector()
		self.nodeStart: sNode = None
		self.nodeEnd: sNode = None
		self.radius = 2  # zombie hitbox
		self.canSeePlayer = False

		self.vDistToPlayer = 0

		self.isHit = False
		self.hitUntil = 0

	def __eq__(self, other):
		if type(other) == createVector:
			return self.pos.x == other.x and self.pos.y == other.y
		else: return False

	def __repr__(self):
		return f'({self.pos.x}, {self.pos.y})'

	def update(self, player: Turret, Map):
		
		# Animation timing
		if not self.isHit and self.health > 0: self.sprite.img = base_zombie_img
		elif self.isHit and self.health > 0: 
			if pgTime.get_ticks() >= self.hitUntil: self.isHit = False
		else: self.sprite.img = base_zombie_dead

		if self.targets and self.health > 0:  # if the zombie has places to go and is alive
			if not self.canSeePlayer: vDir = VOBJ.sub2Vec(createVector(self.targets[0][0], self.targets[0][1]), self.pos)  # vector between zombie and next position
			else: vDir = VOBJ.sub2Vec(player.pos, self.pos)
			if vDir.mag() > self.speed:  # make sure Zombie can't jump over target
				vDir.normalize()
				vDir.mult(self.speed + (random() / 10 - 0.05))

				self.vel.add(vDir)
				next_position = VOBJ.add2Vec(self.vel, self.pos)

				if Map[int(coordToIDX(next_position.x//CELLSIZE, next_position.y//CELLSIZE))] != 2:  # make sure zombie is only walking on floor tiles
					if random() > 0.20 and self.vDistToPlayer > self.reach/2: self.pos = next_position  # move

				self.vel.mult(0)
			elif not self.canSeePlayer:

				# if zombie is going past target, just teleport to place.
				self.pos = createVector(self.targets[0][0], self.targets[0][1])
				del self.targets[0]  # advance zombie position

		if self.health > 0:
			# distance from player to zombie		
			if self.vDistToPlayer < self.reach: player.health -= self.damage / 30  # 30 is the frameRate
			if player.health <= 0: player.score -= 300
		
		self.canSeePlayer = False  # used for direct line of sight

	def set_node_start(self):
		self.nodeStart = sNode((self.pos.x + CELLSIZE/2, self.pos.y + CELLSIZE/2), 0, False, False, 0.0, 0.0, None)


def Generate_Zombie_map(Map):
	z_system = []  # ChunkSystem(CHUNKSIZE)

	for i, cell in enumerate(Map):
		x, y = i % DIMENSIONS, i // DIMENSIONS

		if cell in [7]:
			# z_system.insert(Zombie(x, y, ZOMBIE_TYPES[cell]))
			z_system.append(Zombie(x * CELLSIZE, y * CELLSIZE, ZOMBIE_TYPES[cell]))

	return z_system


def cast_zombie(z_system: list[Zombie], player: Turret) -> list:

	for idx, zombie in enumerate(z_system):
		# distance from player to zombie
		vDistToZombie = zombie.vDistToPlayer

		# coordinate of tip of ray cast
		playerRayCoord = createVector(vDistToZombie * math.cos(player.facing) + player.pos.x,
									  vDistToZombie * math.sin(player.facing) + player.pos.y)

		# distance from ray cast point to centre of zombie hitbox
		dPointHitbox = math.sqrt((playerRayCoord.x - zombie.sprite.x)**2 + (playerRayCoord.y - zombie.sprite.y)**2)

		if dPointHitbox <= zombie.radius and zombie.health > 0 and player.ZOMBIES_ARE_COMING:  # in collision
	
			zombie.health -= player.weapon.damage  # Coldest line in the whole code base

			if zombie.health <= 0: player.score += 100  # zombies are 100 points

			zombie.sprite.img = base_zombie_hit
			zombie.isHit = True
			zombie.hitUntil = pgTime.get_ticks() + 500  # milliseconds
