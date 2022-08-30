import pygame
import math
import VOBJ
from VOBJ import createVector
from GenerateChunkMapFromImage import MapTile
from MapProcessing import WIDTH, HEIGHT
from spriteDefinitions import ammoBox_img, med_kit_img, base_zombie_img, \
							  flashlight_off, Star_powerup, machine_gun_item, \
							  level_portal, Spawn_portal, Number1, base_zombie_dead, \
							  base_zombie_hit, gatling_gun_item, mp5_item

class GameSpriteOBJ:
	def __init__(self, x, y, img, value):
		self.x = x
		self.y = y
		self.img = img
		self.value = value

	def __repr__(self):
		return f'({self.x}, {self.y})'

class GameSpriteSystem:
	"""Handles the rendering of all sprites in engine"""
	def __init__(self, spriteArray: list[GameSpriteOBJ]):
		self.spriteArray = spriteArray

	def coord_to_screen(self, planeV, dirV, spriteV, scale) -> float:
		invDet = 1 / (planeV.x * dirV.y - dirV.x * planeV.y)
		transformX = invDet * (dirV.y * spriteV.x - dirV.x * spriteV.y)
		transformY = invDet * (-planeV.y * spriteV.x + planeV.x * spriteV.y)
		if transformY != 0: 
			spriteScreenX = int((WIDTH / 2) * (1 + transformX / transformY))
			spriteHeight = abs(int(2 / (transformY)))/2 * scale
		else:
			spriteScreenX, spriteHeight = 0, 0
		return spriteScreenX, spriteHeight

	def draw_sprites(self, screen, player, wallDistanceData, columnWidth, z_system, *args):
		# Sprite positioning
		# *args: (dstFromPlane, widthOfPlane)
		lp = createVector(args[1] / 2 * math.cos(player.facing - math.pi / 2), args[1] / 2 * math.sin(player.facing - math.pi / 2))  # left of plane vector
		rp = createVector(args[1] / 2 * math.cos(player.facing + math.pi / 2), args[1] / 2 * math.sin(player.facing + math.pi / 2))  # right of plane vector
		planeV = createVector(rp.x - lp.x, rp.y - lp.y)  # vector of left of plane to right of plane
		dirV = createVector(args[0] * math.cos(player.facing), args[0] * math.sin(player.facing))  # vector in direction of view and length of dist of plane from player

		# sprites must be sorted based on distance to player, so they're drawn in the correct order
		self.spriteArray.sort(key=lambda entity: createVector(entity.x - player.pos.x, entity.y - player.pos.y).mag(), reverse=True)

		for idx, entity in enumerate(self.spriteArray):
			spriteV = createVector(entity.x - player.pos.x, entity.y - player.pos.y)
			sMag = spriteV.mag()

			if VOBJ.dotProduct(dirV, spriteV) > 0 and 3 < sMag < 120 and entity.img is not base_zombie_dead:
				scale = 1
				if entity.value == 7: scale = 2.5
				spriteScreenX, spriteHeight = self.coord_to_screen(planeV, dirV, spriteV, scale)  # returns the screenX and dimensions of sprite/2

				if 0 < spriteScreenX < WIDTH:  # if sprite is actually on screen
					segmentDist = wallDistanceData[int(spriteScreenX // columnWidth)][0]  # calculate which wall the sprite

					# if sprite is in front of player and is in front of walls and is more than 3 pixels away
					if segmentDist > sMag:

						if entity.img is base_zombie_img or entity.img is base_zombie_hit:
							# zombie = [z if z.pos.x == entity.x and z.pos.y == entity.y else 0 for z in z_system]  # getting zombie
							zombie = list(filter(lambda val: val !=  0, [z if z.pos.x == entity.x and z.pos.y == entity.y else 0 for z in z_system]))
							zombie[0].canSeePlayer = True 

						xOffset, yOffset, wStretch, hStretch = 1, 1, 1, 1  # offset is used to make things appear on the floor or in front of the player
						if entity.value == 4: yOffset = 0.3  # 1.5 makes ammo box appear on floor
						if entity.value == 6: yOffset, hStretch = 0.3, 0.8  # med kit
						if entity.value == 10: yOffset, wStretch, xOffset = 0.3, 1.5, 2  # torch
						if entity.value == 7: yOffset, hStretch, wStretch, xOffset = -0.7, 1.1, 1, 1  # base zombie
						if entity.value == 11: yOffset = 0.3  # star
						if entity.value == 12: wStretch, hStretch, yOffset, xOffset = 2, 0.5, 0.3, 1.5  # Machine Gun Item
						if entity.value == 14: wStretch, hStretch, xOffset, yOffset = 3, 4, 3, -3
						if entity.value == 17: wStretch, hStretch, xOffset, yOffset = 1.5, 0.75, 1, 0.2
						if entity.value == 18: wStretch, hStretch, yOffset = 1.5, 0.5, 0.3

						img_copy = pygame.transform.scale(entity.img, (spriteHeight * 2 * wStretch, spriteHeight * 2 * hStretch))  # scale sprite based on calculation
						screen.blit(img_copy, (spriteScreenX - spriteHeight * xOffset, (HEIGHT/2) + spriteHeight * yOffset))
						# pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(spriteScreenX-10 - spriteHeight, 440 - spriteHeight, spriteHeight*2, spriteHeight*2))

def generateSpriteOBJS(spriteCoords: MapTile):
	objs = []

	for idx, sprite in enumerate(spriteCoords):

		if sprite.tile == 4:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, ammoBox_img, 4))

		if sprite.tile == 5:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, Spawn_portal, 5))

		if sprite.tile == 6:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, med_kit_img, 6))

		if sprite.tile == 7:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, base_zombie_img, 7))

		if sprite.tile == 10:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, flashlight_off, 10))

		if sprite.tile == 11:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, Star_powerup, 11))

		if sprite.tile == 12:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, machine_gun_item, 12))

		if sprite.tile == 13:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, Spawn_portal, 13))  # Spawn Portal img is invisible

		if sprite.tile == 14:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, level_portal, 14))

		if sprite.tile == 16:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, Number1, 16))

		if sprite.tile == 17:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, gatling_gun_item, 17))

		if sprite.tile == 18:
			objs.append(GameSpriteOBJ(sprite.pos.x, sprite.pos.y, mp5_item, 18))

	return objs
