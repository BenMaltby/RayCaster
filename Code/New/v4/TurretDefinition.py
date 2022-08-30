from VOBJ import createVector
import VOBJ
from GenerateChunkMapFromImage import DIMENSIONS, coordToIDX
from spriteDefinitions import ammo_icon, gun_idle, gun_shooting, machine_gun_idle, \
							  machine_gun_shooting, flashlight_on, flashlight_off, \
							  gatling_gun_idle, gatling_gun_shooting, mp5_idle, mp5_shooting
from MapProcessing import CELLSIZE, WIDTH, HEIGHT
import pygame
import math

RADIAN = math.pi/180  # used for degree to radian conversion
HEALTH_MAX = 100
MAX_ANGLE = 90
STARTING_WEAPON = "Machine_Gun"
AMMO_CAP = 15
GUNMODEL = [(WIDTH*0.416, HEIGHT), (WIDTH*0.416, HEIGHT*0.875), (WIDTH*0.46, HEIGHT*0.7375), (WIDTH*0.53, HEIGHT*0.7375), (WIDTH*0.583, HEIGHT*0.875), (WIDTH*0.583, HEIGHT)]  # coordinates of gun model
pygame.font.init()  # used for font... duh
GLOBAL_FONT = "Century Gothic"


# Definition of all weapons in the game
class gun:
	def __init__(self, dmg, amcap, fRte, sprites: list, name, szs):  # fire rate is measured in milliseconds	
		self.damage, self.ammo_cap, self.fire_rate, self.wSprite, self.name, self.sprite_sizes = dmg, amcap, fRte, sprites, name, szs

WeaponKit = {
	"Pistol"      : gun(34, 15, 500, [gun_idle, gun_shooting], "pistol", 
						[gun_idle.get_size(), gun_shooting.get_size()]),  # 3 stk

	"Machine_Gun" : gun(25, 15, 100, [machine_gun_idle, machine_gun_shooting], "M_Gun", 
						[machine_gun_idle.get_size(), machine_gun_shooting.get_size()]),  # 4 stk

	"Gatling"     : gun(16, 9999, 50, [gatling_gun_idle, gatling_gun_shooting], "Gat", 
						[gatling_gun_idle.get_size(), gatling_gun_shooting.get_size()]),  # 6 stk

	"MP5"         : gun(20, 20, 100, [mp5_idle, mp5_shooting], "MP5", 
						[mp5_idle.get_size(), mp5_shooting.get_size()])
}


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
		# Used in Ray Casting
		self.pos = createVector(x, y)
		self.vel = createVector()
		self.facing = dir * RADIAN
		self.angleOfVision = deg
		self.step = step
		self.col = col
		self.rayData = []  # Holds Ray coordinates
		self.MapCell = []  # Players map cell coordinate (x: 0 - 79, y: 0 - 79)

		# Item Tracking
		self.isShootAnim = False
		self.AnimUntil = 0
		self.shooting = False
		self.flashlight = False
		self.hasFlashlight = False
		self.on_star = False
		self.starUntil = 0
		self.__AMMO_CAP = WeaponKit[STARTING_WEAPON].ammo_cap
		self.ammo_count = WeaponKit[STARTING_WEAPON].ammo_cap
		self.weapon: gun = WeaponKit[STARTING_WEAPON]  # starting weapons for player
		self.ZOMBIES_ARE_COMING = True

		# Player Stats
		self.radius = 3
		self.health = HEALTH_MAX
		self.canMove = True
		self.score = 0

	def set_defaults(self, args):
		self.health = args[0]
		self.ZOMBIES_ARE_COMING = args[1]
		self.weapon = WeaponKit[args[2]]
		self.ammo_count = WeaponKit[args[2]].ammo_cap if args[3] == "max" else args[3]
		self.__AMMO_CAP = WeaponKit[args[2]].ammo_cap
		self.hasFlashlight = args[4]
		self.facing = args[5] * RADIAN
		self.on_star = False

	def calc_viewing_cells(self) -> list:
		pCell = createVector(int(self.pos.x // CELLSIZE), int(self.pos.y // CELLSIZE))
		cellCoords = []
		for y in range(pCell.y - 1, pCell.y + 2):
			for x in range(pCell.x - 1, pCell.x + 2):
				cell = createVector(VOBJ.clamp(0, DIMENSIONS, x), VOBJ.clamp(0, DIMENSIONS, y))
				cellCoords.append(cell)
		return cellCoords

	def calc_clamped_points(self, cellCoords: list[createVector], Map) -> list:
		points = []
		for idx, cell in enumerate(cellCoords):
			if Map[int(coordToIDX(cell.x, cell.y))] == 2:
				points.append(createVector(VOBJ.clamp(cell.x * CELLSIZE, CELLSIZE*(cell.x+1), self.pos.x), VOBJ.clamp(cell.y * CELLSIZE, CELLSIZE*(cell.y+1), self.pos.y)))
		return points

	def PlayerCollision(self, dx, dy):
		vDist = VOBJ.sub2Vec(self.pos, createVector(dx, dy))
		overlap = self.radius - vDist.mag()
		if overlap >= 0 and vDist.mag() != 0:
			vDist.normalize()
			self.pos.x += overlap * vDist.x
			self.pos.y += overlap * vDist.y

	def display_health_bar(self, screen):
		r = 50
		hb_pos = createVector(r * 2, HEIGHT - r * 2)
		pygame.draw.circle(screen, (20, 20, 20), (hb_pos.x, hb_pos.y), r)
		self.health = VOBJ.clamp(0, HEALTH_MAX, self.health)
		amount = -(MAX_ANGLE - ((self.health / HEALTH_MAX) * MAX_ANGLE))

		for i in range(-MAX_ANGLE, int(amount)+1, 5):
			pygame.draw.line(screen, (255,0,0), (hb_pos.x, hb_pos.y),
							 ((r - 5) * math.cos(i * (2 * RADIAN)) + hb_pos.x, (r - 5) * math.sin(i * (2 * RADIAN)) + hb_pos.y))

		healthTag = pygame.font.SysFont(GLOBAL_FONT, 40)
		textsurface = healthTag.render(str(round(self.health)), True, (255, 0, 0))
		screen.blit(textsurface, (hb_pos.x - 15 if len(str(self.health)) < 3 else hb_pos.x - 25, hb_pos.y + 10))

	def display_ammo_count(self, screen):
		ac_pos = createVector(WIDTH - 90, HEIGHT - 300)
		# pygame.draw.rect(screen, (20,20,20), pygame.Rect(ac_pos.x, ac_pos.y, 50, 250))
		self.ammo_count = VOBJ.clamp(0, self.__AMMO_CAP, self.ammo_count)
		for i in range(VOBJ.clamp(0, 30, self.ammo_count)):
			screen.blit(ammo_icon, (ac_pos.x + 5, (ac_pos.y + 230) - (5 * (5 * i))))

	def display_flashlight(self, screen):
		scale = 1/4
		if self.flashlight:
			img_copy = pygame.transform.flip(flashlight_on, True, False)
			img_copy = pygame.transform.scale(img_copy, (672 * scale, 372 * scale))
			screen.blit(img_copy, (25, 20))
		if not self.flashlight:
			img_copy = pygame.transform.flip(flashlight_off, True, False)
			img_copy = pygame.transform.scale(img_copy, (672 * scale, 372 * scale))
			screen.blit(img_copy, (25, 20))

	def display_compass(self, screen):
		radius, x, y = 30, 100, 165
		pygame.draw.circle(screen, (150,150,150), (x, y), radius + 5)
		pygame.draw.line(screen, (255, 0, 0), (x, y), (radius * math.cos(self.facing) + x, radius * math.sin(self.facing) + y), 2)
		pygame.draw.line(screen, (0, 34, 255), (x, y), (radius/2 * math.cos(self.facing + math.pi) + x, radius/2 * math.sin(self.facing + math.pi) + y), 2)

	def display_hud(self, screen):
		self.display_health_bar(screen)
		self.display_ammo_count(screen)
		if self.hasFlashlight: self.display_flashlight(screen)
		self.display_compass(screen)

	def Check_for_pickup(self, Map, gObjects):
		cell = Map[int(coordToIDX(self.MapCell[0], self.MapCell[1]))]
		index, pickup_used = -1, False
		return_command = "end"
		if cell in [4, 5, 6, 10, 11, 12, 13, 14, 17, 18]:  # item codes of all possible collectables
			for idx, obj in enumerate(gObjects):
				if obj.x // CELLSIZE == self.MapCell[0] and obj.y // CELLSIZE == self.MapCell[1]:
					index = idx
					break
				else: index = -1

			if cell == 4 and index >= 0 and self.ammo_count < self.__AMMO_CAP:
				self.ammo_count += 5
				self.score -= 20  # ammo pickups lose 20 points because makes game easier
				pickup_used = True
			if cell == 5 and index >= 0:
				self.canMove = True
				pickup_used = True
			if cell == 6 and index >= 0 and self.health < HEALTH_MAX:
				self.health += 15
				self.score -= 50  # health pickups lose 50 points because makes game easier
				pickup_used = True
			if cell == 10 and index >= 0 and not self.hasFlashlight:
				self.hasFlashlight = True
				pickup_used = True
			if cell == 11 and index >= 0:
				self.on_star = True
				self.starUntil = pygame.time.get_ticks() + 10_000
				pickup_used = True
			if cell == 12 and index >= 0 and self.weapon.name != "M_Gun":
				self.weapon = WeaponKit["Machine_Gun"]
				self.ammo_count = WeaponKit["Machine_Gun"].ammo_cap
				self.__AMMO_CAP = WeaponKit["Machine_Gun"].ammo_cap
				pickup_used = True
			if cell == 13 and index >= 0:
				self.ZOMBIES_ARE_COMING = True if not self.ZOMBIES_ARE_COMING else False
				pickup_used = True
			if cell == 14 and index >= 0:
				return_command = "next"
				self.score += self.health  # add health at end of each level to score
				self.pos = createVector(self.MapCell[0] + CELLSIZE/2, self.MapCell[1] + CELLSIZE/2)
				self.vel = createVector()
				pickup_used = True
				self.canMove = False
			if cell == 17 and index >= 0 and self.weapon.name != "Gat":
				self.weapon = WeaponKit["Gatling"]
				self.ammo_count = WeaponKit["Gatling"].ammo_cap
				self.__AMMO_CAP = WeaponKit["Gatling"].ammo_cap
				pickup_used = True
			if cell == 18 and index >= 0 and self.weapon.name != "MP5":
				self.weapon = WeaponKit["MP5"]
				self.ammo_count = WeaponKit["MP5"].ammo_cap
				self.__AMMO_CAP = WeaponKit["MP5"].ammo_cap
				pickup_used = True

		if index >= 0 and pickup_used: del gObjects[index]
		return gObjects, return_command


	def Check_Collision(self, Map, speed):
		"""Looks up cell type in Map to check if player is in collision with wall"""
		self.update(speed)

		self.MapCell = [self.pos.x // CELLSIZE, self.pos.y // CELLSIZE]  # calculates map cell of new player position

		if 0 < self.pos.x < DIMENSIONS*CELLSIZE:  # if player is withing bounds of map
			if 0 < self.pos.y < DIMENSIONS*CELLSIZE:

				if Map[int(coordToIDX(self.MapCell[0], self.MapCell[1]))] == 2:  # if players new position is withing wall tile
					return True

				return False  # if not in wall tile, then not in collision

		return True  # if player not in wall tile but leaves bounds of map then return in collision

	# amount = speed of player in pixels
	def Move_LEFT(self):  # moves player left based on facing direction
		self.vel.add(createVector(math.cos(self.facing - math.pi / 2), math.sin(self.facing - math.pi / 2)))

	def Move_RIGHT(self):  # moves player right based on facing direction
		self.vel.add(createVector(math.cos(self.facing + math.pi / 2), math.sin(self.facing + math.pi / 2)))

	def Move_UP(self):  # moves player forward based on facing direction
		self.vel.add(createVector(math.cos(self.facing), math.sin(self.facing)))

	def Move_DOWN(self):  # moves player backwards based on facing direction
		self.vel.add(createVector(math.cos(self.facing - math.pi), math.sin(self.facing - math.pi)))

	def update(self, amount):
		self.vel.normalize()
		self.vel.setMag(amount)
		self.vel.limit(amount)
		self.pos.add(self.vel)

	def showWeapon(self, screen, b):
		"""Displays weapon models in idle and shooting state"""
		if self.weapon.name == "Gat": model_scale = 3
		elif self.weapon.name == "M_Gun": model_scale = 1.6
		elif self.weapon.name == "MP5": model_scale = 3.5
		else: model_scale = 1.6

		if self.shooting:  # draw gun with flash if shooting
			# pygame.draw.rect(screen, (255, 158, 13), pygame.Rect(WIDTH*0.39583, HEIGHT*0.59375, WIDTH*0.208, HEIGHT*0.3125))  # draw flash
			# pygame.draw.polygon(screen, ((150*b*2.5)%255,(150*b*2.5)%255,(150*b*2.5)%255), GUNMODEL)  # draw brighter gun model
			img_copy = pygame.transform.scale(self.weapon.wSprite[1], (self.weapon.sprite_sizes[0][0] * model_scale, self.weapon.sprite_sizes[0][1] * model_scale))  # scale sprite based on calculation
			screen.blit(img_copy, ((WIDTH / 2) - (self.weapon.sprite_sizes[0][0] * model_scale) / 2, HEIGHT - self.weapon.sprite_sizes[0][1] * model_scale))

		else:  # draw dark gun model no flash
			# pygame.draw.polygon(screen, (150*b,150*b,150*b), GUNMODEL)
			img_copy = pygame.transform.scale(self.weapon.wSprite[0], (self.weapon.sprite_sizes[1][0] * model_scale, self.weapon.sprite_sizes[1][1] * model_scale))  # scale sprite based on calculation
			screen.blit(img_copy, ((WIDTH/2) - (self.weapon.sprite_sizes[1][0] * model_scale)/2, HEIGHT - self.weapon.sprite_sizes[1][1] * model_scale))

	def fireRays(self, screen, tConstants: list, numOfRays, threeDview=True):
		"""Calculates Ray coordinates from player position and looking angle"""

		# if not threeDview:
		# 	r, ho2 = 15, HEIGHT/2
		# 	pygame.draw.circle(screen, self.col, (ho2, ho2), r)  # draw player in 2D
		# 	pygame.draw.line(screen, (255,0,0), (ho2, ho2), (r*2*math.cos(self.facing)+ho2, r*2*math.sin(self.facing)+ho2))

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