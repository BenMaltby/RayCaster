import math
import pygame
import colorsys
import MapProcessing
import GEWY
from RayCastDefinition import CastRays
from EdgeDetectionAlgorithm import primitiveEdges, calculatedEdges, edgeChunk
from TurretDefinition import Turret
from GenerateChunkMapFromImage import GenerateChunks
# from LineSegmentDefinition import lineSeg

WIDTH = MapProcessing.WIDTH
HEIGHT = MapProcessing.HEIGHT
FPS = 30
SPEED = 3
TORQUE = 2
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
RayCastView = True

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

def playerMovement(sp, rot, Map):
	keysPressed = pygame.key.get_pressed()
	if keysPressed[pygame.K_a]:
		Player.Move_LEFT(sp)
		if Player.Check_Collision(Map):
			Player.Move_RIGHT(sp)
	if keysPressed[pygame.K_d]:
		Player.Move_RIGHT(sp)
		if Player.Check_Collision(Map):
			Player.Move_LEFT(sp)
	if keysPressed[pygame.K_w]:
		Player.Move_UP(sp)
		if Player.Check_Collision(Map):
			Player.Move_DOWN(sp)
	if keysPressed[pygame.K_s]:
		Player.Move_DOWN(sp)
		if Player.Check_Collision(Map):
			Player.Move_UP(sp)
	if keysPressed[pygame.K_j]:
		Player.facing -= rot * RADIAN
	if keysPressed[pygame.K_l]:
		Player.facing += rot * RADIAN
	if keysPressed[pygame.K_k]:
		Player.shooting = True


Player = Turret(100, 100, 270, 80, 0.5, (0, 255, 0))
RayCol = (0, 255, 0)


def main():
	Map = GenerateChunks("GameBoard.png")

	primEdgeSystem = primitiveEdges(Map)
	edgeSystem = calculatedEdges(primEdgeSystem)
	# print(edgeSystem)
	# exit()
	# LevelWalls.append(lineSeg(400, 450, 500, 367, 'H'))

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

		Player.MapCell = [Player.pos.x // MapProcessing.CELLSIZE, Player.pos.y // MapProcessing.CELLSIZE]

		playerMovement(SPEED*deltaTime, TORQUE*deltaTime, Map)

		if RayCastView:
			Player.fireRays(screen, 1200, 1800)
			DSD = CastRays(screen, Player, edgeSystem, 1, RayCastView)
			MapProcessing.renderMap3D(screen, DSD, 1100)
			# MapProcessing.MiniMap2D(screen, 400, Player, (10, 10), Map)

		elif not RayCastView:
			screen.fill((50, 50, 50))
			MapProcessing.renderMap2D(screen)
			Player.fireRays(screen, 1200, 1800)
			DSD = CastRays(screen, Player, edgeSystem, 1, RayCastView)

		# for y in range(8):
		# 	for x in range(8):
		# 		LevelWalls = edgeSystem.Query(edgeChunk(x, y), 0)
		# 		for i in range(len(LevelWalls)):
		# 			pygame.draw.line(screen, LevelWalls[i].edgeData.col, (LevelWalls[i].edgeData.x1, LevelWalls[i].edgeData.y1), (LevelWalls[i].edgeData.x2, LevelWalls[i].edgeData.y2), 3)

		pygame.draw.circle(screen, (0, 0, 0), (WIDTH/2, HEIGHT/2), 7, 2)
		Player.showWeapon(screen)
		Player.shooting = False

		GEWY.display(screen)
		pygame.display.flip()

		#Player.facing = ((ColIDX*1) * math.pi/180)

		ColIDX += 1

	pygame.quit()


if __name__ == "__main__":
	main()