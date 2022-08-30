import math
import pygame
import colorsys
import MapProcessing
from RayCastDefinition import CastRays
from EdgeDetectionAlgorithm import primitiveEdges, calculatedEdges
from TurretDefinition import Turret
import GEWY

WIDTH = MapProcessing.WIDTH
HEIGHT = MapProcessing.HEIGHT
FPS = 60
SPEED = 4
TORQUE = 3
RADIAN = math.pi/180

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlickyMachine")
clock = pygame.time.Clock()  # For syncing the FPS

# GUI BOILERPLATE CODE
# testButton = GEWY.Button(10, 5, 15, 15, "Test")
# testButtonWrapper = GEWY.Wrapper(800, 50, 35, 25, [testButton], "Test")
# GEWY.GUI_OBJECTS.append(testButtonWrapper)
#
# tabs = GEWY.TabSystem(x=800)
# tabs.addTab(testButtonWrapper)
# GEWY.GUI_OBJECTS.append(tabs)


def hsv2rgb(h, s, v):
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

def playerMovement():
	keysPressed = pygame.key.get_pressed()
	if keysPressed[pygame.K_a]:
		Player.Move_LEFT(SPEED)
		if Player.Check_Collision(MapProcessing.Map, MapProcessing.CELLSIZE):
			Player.Move_RIGHT(SPEED)
	if keysPressed[pygame.K_d]:
		Player.Move_RIGHT(SPEED)
		if Player.Check_Collision(MapProcessing.Map, MapProcessing.CELLSIZE):
			Player.Move_LEFT(SPEED)
	if keysPressed[pygame.K_w]:
		Player.Move_UP(SPEED)
		if Player.Check_Collision(MapProcessing.Map, MapProcessing.CELLSIZE):
			Player.Move_DOWN(SPEED)
	if keysPressed[pygame.K_s]:
		Player.Move_DOWN(SPEED)
		if Player.Check_Collision(MapProcessing.Map, MapProcessing.CELLSIZE):
			Player.Move_UP(SPEED)
	if keysPressed[pygame.K_j]:
		Player.facing -= TORQUE * RADIAN
	if keysPressed[pygame.K_l]:
		Player.facing += TORQUE * RADIAN


Player = Turret(400, 400, 270, 80, 0.5, (0, 255, 0))
RayCol = (0, 255, 0)


def main():
	LevelWalls = primitiveEdges()
	LevelWalls = calculatedEdges(LevelWalls)

	getTicksLastFrame = 0
	ColIDX = 0  # keep for rainbow
	running = True
	while running:

		r, g, b = hsv2rgb(((ColIDX + 0.3) / 100) % 3, 1, 1)

		t = pygame.time.get_ticks()
		deltaTime = (t - getTicksLastFrame) / 15.0
		getTicksLastFrame = t

		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			mVec = pygame.mouse.get_pos()
			GEWY.handleEvents(event, mVec, screen)

		playerMovement()

		screen.fill((50, 50, 50))
		#MapProcessing.renderMap2D(screen)
		DSD = CastRays(screen, Player, LevelWalls)
		Player.fireRays(screen, 1200, 1800)
		MapProcessing.renderMap3D(screen, DSD, 1100)
		MapProcessing.MiniMap2D(screen, 200, Player, (10, 10))

		# for i in range(len(LevelWalls)):
		# 	pygame.draw.line(screen, LevelWalls[i].col, (LevelWalls[i].x1, LevelWalls[i].y1), (LevelWalls[i].x2, LevelWalls[i].y2), 3)

		pygame.draw.circle(screen, (0, 0, 0), (WIDTH/2, HEIGHT/2), 7, 2)

		GEWY.display(screen)
		pygame.display.flip()

		#Player.facing = ((ColIDX*1) * math.pi/180)

		ColIDX += 1

	pygame.quit()


if __name__ == "__main__":
	main()