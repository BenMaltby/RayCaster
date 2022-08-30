import math
import pygame
import colorsys
import MapProcessing
import GEWY
from RayCastDefinition import CastRays
from EdgeDetectionAlgorithm import primitiveEdges, calculatedEdges
from TurretDefinition import Turret, thetaOffsetConstants
from GenerateChunkMapFromImage import GenerateChunks

# CONSTANTS
WIDTH = MapProcessing.WIDTH  # Width of window in pixels
HEIGHT = MapProcessing.HEIGHT  # Height of window in pixels
FPS = 30  # 30 runs smooth and is more efficient
SPEED = 1  # Pixels
TORQUE = 2  # Pixels
RADIAN = math.pi / 180  # used for degree to radian conversion

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
# View Mode Button Instances
RayCastViewButton = GEWY.Button(5, 10, 20, 20, "3D View", True)
BirdsEyeViewButton = GEWY.Button(5, 40, 20, 20, "2D View")
RenderWallLinesButton = GEWY.Button(5, 70, 20, 20, "2D WireFrame", True)
testButtonWrapper = GEWY.Wrapper(10, 35, 150, 100, [RayCastViewButton, BirdsEyeViewButton, RenderWallLinesButton], "Change View")
GEWY.GUI_OBJECTS.append(testButtonWrapper)

brightnessSettings = False  # True when debugging
# Brightness Setting slider instances
sceneBrightnessSlider = GEWY.VariableSlider(5, 30, 100, 0, 1, "Scene", True, 1)
wallBrightnessSlider  = GEWY.VariableSlider(5, 70, 100, 0, 2, "Walls", True, 2)
flashBrightnessSlider = GEWY.VariableSlider(5, 110, 100, 3, 15, "Gun Flash", True, 3)
BrightnessSlidersWrapper = GEWY.Wrapper(170, 35, 150, 130, [sceneBrightnessSlider, wallBrightnessSlider, flashBrightnessSlider], "Brightness Options")
GEWY.GUI_OBJECTS.append(BrightnessSlidersWrapper)

# GUI Tab system setup
tabs = GEWY.TabSystem()
tabs.addTab(testButtonWrapper)
if brightnessSettings: tabs.addTab(BrightnessSlidersWrapper)
GEWY.GUI_OBJECTS.append(tabs)


def hsv2rgb(h, s, v):  # Colour conversion function
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def playerMovement(sp, rot, Map) -> None:
	"""
	Handles Player input and Collision response.
	Moves player in direction of travel and then checks collision in new position.
	If there is a collision the movement is reverted as response to collision.

	Parameters:
		sp: speed of player movement
		rot: rotational speed of player
		Map: Array of map cells
	"""

	keysPressed = pygame.key.get_pressed()  # inputs

	if keysPressed[pygame.K_a]:  # a = STRAFE LEFT
		Player.Move_LEFT(sp)
		if Player.Check_Collision(Map):
			Player.Move_RIGHT(sp)

	if keysPressed[pygame.K_d]:  # d = STRAFE RIGHT
		Player.Move_RIGHT(sp)
		if Player.Check_Collision(Map):
			Player.Move_LEFT(sp)

	if keysPressed[pygame.K_w]:  # w = FORWARD
		Player.Move_UP(sp)
		if Player.Check_Collision(Map):
			Player.Move_DOWN(sp)

	if keysPressed[pygame.K_s]:  # s = BACKWARDS
		Player.Move_DOWN(sp)
		if Player.Check_Collision(Map):
			Player.Move_UP(sp)

	if keysPressed[pygame.K_j]:  # j = TURN LEFT
		Player.facing -= rot * RADIAN

	if keysPressed[pygame.K_l]:  # l = TURN RIGHT
		Player.facing += rot * RADIAN

	if keysPressed[pygame.K_k]:  # k = SHOOT GUN
		Player.shooting = True


# Instantiation of Payer Object known as "Turret"
Player = Turret(780, 780, 270, 80, 0.5, (0, 255, 0))
RayCol = (0, 255, 0)  # used for 2D diagram


def main():
	"""Main running file, which handles main loop"""

	ChunkedMap, Map = GenerateChunks("BigBoardTest.png")  # Generates a ChunkSystem of GameBoard Image

	# Two functions responsible for generating coordinate Line data
	primEdgeSystem = primitiveEdges(ChunkedMap)
	edgeChunkSystem = calculatedEdges(primEdgeSystem)

	tConstants, numOfRays = thetaOffsetConstants(Player.angleOfVision//Player.step, 1200, 1800)

	# Used for formatting chunk data in to images to help with debugging
	# MapProcessing.render2DRawChunkedGridData(screen, ChunkedMap, 8)
	# MapProcessing.render2DRawGridData(screen, Map)

	getTicksLastFrame = 0  # used in delta time
	ColIDX = 0  # keep for rainbow
	running = True
	while running:  # main game loop

		r, g, b = hsv2rgb(((ColIDX + 0.3) / 100) % 3, 1, 1)  # rainbow r, g, b

		# Allows for speed of game to be independent of frame rate
		t = pygame.time.get_ticks()
		deltaTime = (t - getTicksLastFrame) / 15.0
		getTicksLastFrame = t

		clock.tick(FPS)
		for event in pygame.event.get():  # pygame event handling
			if event.type == pygame.QUIT:
				running = False

			# Handles all input for my GUI
			mVec = pygame.mouse.get_pos()
			GEWY.handleEvents(event, mVec, screen)

		# Keeps track of Player cell coordinate
		Player.MapCell = [Player.pos.x // MapProcessing.CELLSIZE, Player.pos.y // MapProcessing.CELLSIZE]

		# Handles Player collision with walls and movement
		playerMovement(SPEED * deltaTime, TORQUE * deltaTime, Map)
		screen.fill(BLACK)  # Colour screen Black

		# if Rendering 3D View
		if RayCastViewButton.returnState():
			Player.fireRays(screen, tConstants, numOfRays)  # generates ray coordinates
			DSD = CastRays(screen, Player, edgeChunkSystem, tConstants, RayCastViewButton.returnState())  # compares ray's against walls

			# Brightness Values from GUI objects
			wallB = wallBrightnessSlider.returnValue() if brightnessSettings else 1
			sceneB = sceneBrightnessSlider.returnValue() if brightnessSettings else 0.05
			flashB = flashBrightnessSlider.returnValue() if brightnessSettings else 15

			MapProcessing.renderMap3D(screen, DSD, 1100, wallB, sceneB, flashB, Player.shooting)  # responsible for drawing scene
			# MapProcessing.MiniMap2D(screen, 400, Player, (10, 10), Map)  # Mini Map for 3D scene
			pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2, HEIGHT/2), 5, 1)  # crosshair
			Player.showWeapon(screen, 1-(flashB/20))  # displays weapon models

		# if Rendering 2D View
		elif BirdsEyeViewButton.returnState():
			MapProcessing.renderMap2D(screen)  # responsible for drawing scene
			Player.fireRays(screen, tConstants, numOfRays)  # generates ray coordinates
			DSD = CastRays(screen, Player, edgeChunkSystem, tConstants, RayCastViewButton.returnState())  # compares ray's against walls

		elif RenderWallLinesButton.returnState():
			MapProcessing.render2DWallLines(screen, edgeChunkSystem, Player)  # Renders 2D Map WireFrame

		Player.shooting = False  # Players shooting is set to False at end of Frame to stop shooting

		GEWY.display(screen)  # handles rendering of GEWY objects
		pygame.display.flip()

		# Player.facing = ((ColIDX*1) * math.pi/180)  # used to give player constant rotation

		ColIDX += 1  # used for rainbow

	pygame.quit()

# 1. a lot of imports could mess with namespace
# 2. PyCharm recognises it as a run-able file
if __name__ == "__main__":
	main()
