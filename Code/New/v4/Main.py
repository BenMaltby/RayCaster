import math
import pygame
import colorsys
import MapProcessing
import GEWY
import VOBJ
import game_state_functions

from RayCastDefinition import CastRays
from EdgeDetectionAlgorithm import primitiveEdges, calculatedEdges
from TurretDefinition import Turret, thetaOffsetConstants, HEALTH_MAX
from GenerateChunkMapFromImage import GenerateChunks, CHUNKSIZE, DIMENSIONS
from SpriteSystem import GameSpriteSystem, generateSpriteOBJS
from VOBJ import createVector
from aStar import PathfindingBoard
from Zombie_Definition import Zombie, Generate_Zombie_map, cast_zombie
from Level_Presets import Level_Defaults

# CONSTANTS
WIDTH = MapProcessing.WIDTH  # Width of window in pixels
HEIGHT = MapProcessing.HEIGHT  # Height of window in pixels
FPS = 60  # 30 runs smooth and is more efficient
RADIAN = math.pi / 180  # used for degree to radian conversion
CurrentGameState = 1
MAP_IMG_PATH = "MapFiles/Level_0.png"

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()  # For syncing the FPS

pygame.font.init()
myfont = pygame.font.SysFont('Century Gothic', 20)
pauseMenuText = pygame.font.SysFont('Century Gothic', 100)
ENDMenuText = pygame.font.SysFont('Century Gothic', 100)

# GUI BOILERPLATE CODE
# View Mode Button Instances
RayCastViewButton = GEWY.Button(5, 10, 20, 20, "3D View", True)
BirdsEyeViewButton = GEWY.Button(5, 40, 20, 20, "2D View", True)
RenderWallLinesButton = GEWY.Button(5, 70, 20, 20, "2D WireFrame", True)
RenderMapImageButton = GEWY.Button(5, 100, 20, 20, "2D Map Image", True)
ViewButtonWrapper = GEWY.Wrapper(10, 35, 200, 100, [RayCastViewButton, BirdsEyeViewButton, RenderWallLinesButton, RenderMapImageButton], "Change View")
# GEWY.GUI_OBJECTS.append(ViewButtonWrapper)

brightnessSettings = False  # True when debugging
# Brightness Setting slider instances
sceneBrightnessSlider = GEWY.VariableSlider(5, 30, 100, 0, 1, "Scene", True, 1)
wallBrightnessSlider = GEWY.VariableSlider(5, 70, 100, 0, 2, "Walls", True, 2)
flashBrightnessSlider = GEWY.VariableSlider(5, 110, 100, 3, 15, "Gun Flash", True, 3)
BrightnessSlidersWrapper = GEWY.Wrapper(170, 35, 150, 130, [sceneBrightnessSlider, wallBrightnessSlider, flashBrightnessSlider], "Brightness Options")
# GEWY.GUI_OBJECTS.append(BrightnessSlidersWrapper)

Resume_Button  = GEWY.Button (0, 0, 300, 60, "Resume", False, (-215, -15), textSize=50, tp_back=True)
Resume_Wrapper = GEWY.Wrapper(450, 300, 300, 60, [Resume_Button], show_window=False)
GEWY.GUI_OBJECTS.append(Resume_Wrapper)
Exit_Button  = GEWY.Button (0, 0, 300, 60, "Exit", False, (-185, -15), textSize=50, tp_back=True)
Exit_Wrapper = GEWY.Wrapper(450, 460, 300, 60, [Exit_Button], show_window=False)
GEWY.GUI_OBJECTS.append(Exit_Wrapper)

Restart_Button  = GEWY.Button (0, 0, 300, 60, "Restart", False, (-215, -15), textSize=50, tp_back=True)
Restart_Wrapper = GEWY.Wrapper(450, 300, 300, 60, [Restart_Button], show_window=False)
GEWY.GUI_OBJECTS.append(Restart_Wrapper)

# settings_button  = GEWY.Button (0, 0, 300, 60, "Settings", False, (-220, -15), textSize=50, tp_back=True)
res_slider = GEWY.VariableSlider(125, 50, 300, 0.3, 1.5, "Resolution:  HIGH  ------>  LOW  (1.0 Recommended)", True, 0.7, 30, (-80, -45))
settings_wrapper = GEWY.Wrapper(330, 410, 550, 80, [res_slider], show_window=False)
GEWY.GUI_OBJECTS.append(settings_wrapper)

Tabs = GEWY.TabSystem(0, -50)
Tabs.addTab(Resume_Wrapper)
Tabs.addTab(Exit_Wrapper)
Tabs.addTab(Restart_Wrapper)
Tabs.addTab(settings_wrapper)
GEWY.GUI_OBJECTS.append(Tabs)

def hsv2rgb(h, s, v):  # Colour conversion function
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


SPEED = 0.25  # if RayCastViewButton.returnState() else 0.5 # Pixels
TORQUE = 2  # Pixels


def playerMovement(keys, sp, rot, Map, dt) -> list:
	"""
	Handles Player input and Collision response.
	Moves player in direction of travel and then checks collision in new position.
	If there is a collision the movement is reverted as response to collision.

	Parameters:
		sp: speed of player movement
		rot: rotational speed of player
		Map: Array of map cells
		keys: keys that are down on that frame
	"""
	Player.vel.mult(0)

	if keys[pygame.K_a]:  # a = STRAFE LEFT
		Player.vel.add(createVector(math.cos(Player.facing - math.pi / 2), math.sin(Player.facing - math.pi / 2)))

	if keys[pygame.K_d]:  # d = STRAFE RIGHT
		Player.vel.add(createVector(math.cos(Player.facing + math.pi / 2), math.sin(Player.facing + math.pi / 2)))

	if keys[pygame.K_w]:  # w = FORWARD
		Player.vel.add(createVector(math.cos(Player.facing), math.sin(Player.facing)))

	if keys[pygame.K_s]:  # s = BACKWARDS
		Player.vel.add(createVector(math.cos(Player.facing - math.pi), math.sin(Player.facing - math.pi)))

	if Player.vel.mag() > 0:
		Player.vel.normalize()
		Player.vel.mult(sp)

	Player.vel.mult(dt)
	Player.pos = VOBJ.add2Vec(Player.pos, Player.vel)

	cellCoords = Player.calc_viewing_cells()
	points = Player.calc_clamped_points(cellCoords, Map)
	for d in points:
		Player.PlayerCollision(d.x, d.y)

	Player.facing += (rot * RADIAN) % math.tau

	if keys[pygame.K_k]:  # k = SHOOT GUN
		Player.shooting = True

	return points


def HandleMouse(dt):
	if pygame.mouse.get_focused() != 0:
		if BirdsEyeViewButton.returnState() or RenderWallLinesButton.returnState():
			rotate = ((pygame.mouse.get_pos()[0] - WIDTH / 2) / (WIDTH / 1.5)) / RADIAN * (dt)
		else:
			rotate = ((pygame.mouse.get_pos()[0] - WIDTH / 2) / (WIDTH / 1.5)) / RADIAN * (dt)
		return rotate
	else:
		return 0


# Instantiation of Payer Object known as "Turret"
Player = Turret(780, 780, 0, 80, 0.5, (3, 132, 70))
RayCol = (0, 255, 0)  # used for 2D diagram


def GameState1(has_game_started):
	"""Main running state, which handles game loop"""
	global MAP_IMG_PATH

	return_command = "end"

	if MAP_IMG_PATH[-5:-4] in Level_Defaults: is_game_over = False
	else:
		is_game_over = True
		MAP_IMG_PATH = MAP_IMG_PATH[:-5] + str(int(MAP_IMG_PATH[-5:-4]) - 1) + ".png"

	Player.set_defaults(Level_Defaults[MAP_IMG_PATH[-5:-4]])  # Allows levels to start with different parameters

	pygame.mouse.set_visible(False)
	pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)

	# Load image of map for use of viewing 
	img_of_map = pygame.image.load(MAP_IMG_PATH)
	img_of_map.set_colorkey((0, 0, 0, 0))

	# Make sure "DIMENSIONS" is changed in "GenerateChunkMapFromImage.py" to match width of map
	ChunkedMap, Map, PlayerSpawn, sprite_coords = GenerateChunks(MAP_IMG_PATH)  # Generates a ChunkSystem of GameBoard Image

	# Zombie init
	z_system: list[Zombie] = Generate_Zombie_map(Map)
	# instance of board grid defined as graph for use in pathfinding
	ai_nodeGraph = PathfindingBoard(Map, DIMENSIONS, MapProcessing.CELLSIZE)

	# sprite stuff
	zombie_coords: list[createVector] = []
	for idx, zombie in enumerate(z_system):
		zombie_coords.append(zombie.pos)

	indexes = []
	for idx, obj in enumerate(sprite_coords):
		if (obj.pos * MapProcessing.CELLSIZE) in zombie_coords:
			indexes.append((z_system.index(obj.pos * MapProcessing.CELLSIZE), idx))

		obj.pos.x = obj.pos.x * MapProcessing.CELLSIZE + (MapProcessing.CELLSIZE / 2)
		obj.pos.y = obj.pos.y * MapProcessing.CELLSIZE + (MapProcessing.CELLSIZE / 2)
	gObjects = generateSpriteOBJS(sprite_coords)
	for idx in indexes: z_system[idx[0]].sprite = gObjects[idx[1]]
	GSS = GameSpriteSystem(gObjects)

	# Player spawn point
	if PlayerSpawn:
		Player.pos.x = PlayerSpawn[0] * MapProcessing.CELLSIZE + (MapProcessing.CELLSIZE / 2)
		Player.pos.y = PlayerSpawn[1] * MapProcessing.CELLSIZE + (MapProcessing.CELLSIZE / 2)
	else:
		raise Exception("No Spawn Point, Map requires spawn point.")

	# Two functions responsible for generating coordinate Line data
	primEdgeSystem = primitiveEdges(ChunkedMap)
	edgeChunkSystem = calculatedEdges(primEdgeSystem)

	tConstants, numOfRays = thetaOffsetConstants(Player.angleOfVision // Player.step, 227, 340.5)  # 227, 340.5

	# Used for formatting chunk data in to images to help with debugging
	# MapProcessing.render2DRawChunkedGridData(screen, ChunkedMap, int(HEIGHT//DIMENSIONS))
	# MapProcessing.render2DRawGridData(screen, Map)


	# pre-defined stuff
	getTicksLastFrame = 0  # used in delta time
	ColIDX = 0  # keep for rainbow
	time_since_torch, time_since_pause = 0, 0
	Old_ammo_count, Old_health_amount = Player.weapon.ammo_cap, HEALTH_MAX
	mouseDown = False
	star_screen, pause_screen, Start_screen, end_screen = pygame.Surface((WIDTH, HEIGHT)), pygame.Surface((WIDTH, HEIGHT)), pygame.Surface((WIDTH, HEIGHT)), pygame.Surface((WIDTH, HEIGHT))
	star_screen.set_alpha(30)
	pause_screen.set_alpha(200)
	game_paused = False
	running = True
	while running:  # main game loop

		if RayCastViewButton.returnState():  # fps control
			fps = 30
		else:
			fps = 60

		if not game_paused:
			pygame.mouse.set_visible(False)
			pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
		else:
			pygame.mouse.set_visible(True)

		keysPressed = pygame.key.get_pressed()  # inputs

		r, g, b = hsv2rgb(((ColIDX + 0.3) / 100) % 3, 1, 1)  # rainbow r, g, b

		# Allows for speed of game to be independent of frame rate
		ticks = pygame.time.get_ticks()
		deltaTime = (ticks - getTicksLastFrame) / 15.0

		clock.tick(fps)  # window title
		pygame.display.set_caption(f'Blicky Machine: {clock.get_fps() :.1f}')

		for event in pygame.event.get():  # pygame event handling
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseDown = True
			if event.type == pygame.MOUSEBUTTONUP:
				mouseDown = False
			if keysPressed[pygame.K_1]:
				RayCastViewButton.state = False
				BirdsEyeViewButton.state = False
				RenderWallLinesButton.state = True
				RenderMapImageButton.state = False
			if keysPressed[pygame.K_2]:
				RayCastViewButton.state = False
				BirdsEyeViewButton.state = True
				RenderWallLinesButton.state = False
				RenderMapImageButton.state = False
			if keysPressed[pygame.K_3]:
				RayCastViewButton.state = True
				BirdsEyeViewButton.state = False
				RenderWallLinesButton.state = False
				RenderMapImageButton.state = False
			if keysPressed[pygame.K_4]:
				RayCastViewButton.state = False
				BirdsEyeViewButton.state = False
				RenderWallLinesButton.state = False
				RenderMapImageButton.state = True
			if keysPressed[pygame.K_f] and ticks >= time_since_torch:
				if Player.hasFlashlight: 
					Player.flashlight = True if not Player.flashlight else False
					time_since_torch = ticks + 150  # 200 milliseconds or 0.2 seconds
			if keysPressed[pygame.K_h]:
				Player.on_star = True if Player.on_star == False else False
				Player.starUntil = ticks + 10_000
				ColIDX = 0
			if keysPressed[pygame.K_ESCAPE] and ticks >= time_since_pause:
				game_paused = True if not game_paused else False
				Player.canMove = True if not Player.canMove else False
				pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
				time_since_pause = ticks + 300

			# Handles all input for my GUI
			mVec = pygame.mouse.get_pos()
			GEWY.handleEvents(event, mVec, screen)

		# Keeps track of Player cell coordinate
		Player.MapCell = [int(Player.pos.x // MapProcessing.CELLSIZE), int(Player.pos.y // MapProcessing.CELLSIZE)]



		# Zombie Path Finding Logic
		if ColIDX % 100 == 0:  # delays zombie path calculation
			ai_nodeGraph.nodeStarts = []
			for jdx, enemy in enumerate(z_system):
				# find enemies starting node position and add them to a list of starting positions to calc each zombies path
				if not enemy.canSeePlayer and enemy.vDistToPlayer < 120:  # Only calculate path if enemie is in sight
					ai_nodeGraph.nodeStarts.append(ai_nodeGraph.nodeGrid.chunkMap[f'{int(enemy.pos.x // MapProcessing.CELLSIZE)} {int(enemy.pos.y // MapProcessing.CELLSIZE)}'][0])
			# find players current node (target for enemies)
			ai_nodeGraph.nodeEnd = ai_nodeGraph.nodeGrid.chunkMap[f'{int(Player.pos.x // MapProcessing.CELLSIZE)} {int(Player.pos.y // MapProcessing.CELLSIZE)}'][0]
			# solve path for every enemy
			for idx, node in enumerate(ai_nodeGraph.nodeStarts):
				ai_nodeGraph.Solve_AStar(node)
				z_system[idx].targets = ai_nodeGraph.getPath()  # sets list of movement instructions for enemy

		# moves each zombie based on movement instructions
		for idx, zombie in enumerate(z_system):
			zombie.vDistToPlayer = math.sqrt((Player.pos.x - zombie.sprite.x)**2 + (Player.pos.y - zombie.sprite.y)**2)
			if Player.ZOMBIES_ARE_COMING and zombie.vDistToPlayer < 120 and not game_paused: 
				zombie.update(Player, Map)
			zombie.sprite.x = zombie.pos.x
			zombie.sprite.y = zombie.pos.y



		# gun shot timing and logic
		if not game_paused:
			if mouseDown:
				if not Player.isShootAnim and Player.ammo_count > 0:
					Player.isShootAnim = True
					Player.AnimUntil = ticks + Player.weapon.fire_rate
					Player.shooting = True
					if not Player.on_star: Player.ammo_count -= 1
					cast_zombie(z_system, Player)  # handle detecting zombie hits and deal damage
				else: 
					if ticks >= Player.AnimUntil and Player.ammo_count > 0:
						Player.isShootAnim = True
						Player.AnimUntil = ticks + Player.weapon.fire_rate
						Player.shooting = True
						if not Player.on_star: Player.ammo_count -= 1
						cast_zombie(z_system, Player)  # handle detecting zombie hits and deal damage

			elif not mouseDown:
				if ticks >= Player.AnimUntil: Player.isShootAnim = False


		# Handles Player collision with walls and movement
		rot = HandleMouse(deltaTime)
		screen.fill(BLACK)  # Colour screen Black


		# if Rendering 3D View
		if RayCastViewButton.returnState():
			curr_speed = SPEED/2 if not Player.on_star else SPEED
			if Player.canMove: points = playerMovement(keysPressed, curr_speed * deltaTime, rot * 0.6 * deltaTime, Map, deltaTime)
			Player.fireRays(screen, tConstants, numOfRays, RayCastViewButton.returnState())  # generates ray coordinates
			DSD = CastRays(screen, Player, edgeChunkSystem, Map, tConstants, RayCastViewButton.returnState())  # compares ray's against walls

			# Brightness Values from GUI objects
			wallB = wallBrightnessSlider.returnValue() if brightnessSettings else 1  # 1
			sceneB = sceneBrightnessSlider.returnValue() if brightnessSettings else 0.02  # 0.02
			flashB = flashBrightnessSlider.returnValue() if brightnessSettings else 15  # 15k

			# responsible for drawing scene
			MapProcessing.renderMap3D(screen, Player, z_system, DSD, WIDTH, GSS, wallB, sceneB, flashB, 1800, 1200, (r,g,b), ColIDX/100)

			# MapProcessing.MiniMap2D(screen, 400, Player, (10, 10), Map)  # Mini Map for 3D scene
			pygame.draw.circle(screen, (255, 255, 255), (WIDTH / 2, HEIGHT / 2), 5, 1)  # crosshair
			Player.showWeapon(screen, 1 - (flashB / 20))  # displays weapon models


		# if Rendering 2D View
		elif BirdsEyeViewButton.returnState():
			curr_speed = SPEED/2 if not Player.on_star else SPEED
			points = playerMovement(keysPressed, curr_speed * deltaTime, rot * deltaTime, Map, deltaTime)  # points are used for debugging
			spriteCoords = MapProcessing.renderMap2D(screen, Map, Player)  # responsible for drawing scene
			Player.fireRays(screen, tConstants, numOfRays, RayCastViewButton.returnState())  # generates ray coordinates
			DSD = CastRays(screen, Player, edgeChunkSystem, Map, tConstants, RayCastViewButton.returnState(), spriteCoords)  # compares ray's against walls

			for d in points:  # show the clamped wall collision points
				playerCell = (Player.pos.x / MapProcessing.CELLSIZE, Player.pos.y / MapProcessing.CELLSIZE)  # floating point of cell coordinate
				scale = MapProcessing.HEIGHT / CHUNKSIZE  # scale for resizing
				cx, cy = (HEIGHT / 2) - ((playerCell[0] - d.x / MapProcessing.CELLSIZE) * scale), (HEIGHT / 2) - ((playerCell[1] - d.y / MapProcessing.CELLSIZE) * scale)
				pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 5)


		elif RenderWallLinesButton.returnState():
			points = playerMovement(keysPressed, SPEED / 2 * deltaTime, rot * 1.2 * deltaTime, Map, deltaTime)
			MapProcessing.render2DWallLines(screen, edgeChunkSystem, Player)  # Renders 2D Map WireFrame


		elif RenderMapImageButton.returnState():
			points = playerMovement(keysPressed, SPEED / 2 * deltaTime, rot * 1.2 * deltaTime, Map, deltaTime)
			MapProcessing.renderMapAsImage(screen, img_of_map, Player)  # Renders 2D Map WireFrame


		if RayCastViewButton.returnState() or BirdsEyeViewButton.returnState():
			Player.display_hud(screen)  # heads up display (health, ammo, torch, compass)
			GSS.spriteArray, return_command = Player.Check_for_pickup(Map, gObjects)  # adds functionality to sprites
			if return_command == "next":  # handles portal pickup
				running, return_command = False, "next"
				break

		getTicksLastFrame = ticks
		# GEWY.display(screen)  # handles rendering of GEWY objects

		if Player.on_star:  # timing for the star powerup
			star_screen.fill((r, g, b))
			screen.blit(star_screen, (0,0))
			Player.health = HEALTH_MAX
			if ticks >= Player.starUntil:
				Player.health = Old_health_amount
				Player.on_star = False

		if not Player.on_star:
			Old_health_amount = Player.health


		# Pause screen code
		if game_paused and Player.health > 0 and has_game_started and not is_game_over:
			cmd = game_state_functions.Pause_Screen(screen, pause_screen, Player, Tabs, Resume_Wrapper, Resume_Button,
										  Restart_Wrapper, Restart_Button, Exit_Wrapper, Exit_Button, 
										  pauseMenuText)
			if cmd == "play": game_paused = False
			elif cmd == "restart": return "run"
			elif cmd == "exit": return "end"


		# Death screen code
		if Player.health <= 0:
			game_paused = True
			cmd = game_state_functions.Death_Screen(screen, pause_screen, Player, Tabs, Restart_Wrapper, 
										  Restart_Button, Exit_Wrapper, Exit_Button, pauseMenuText)
			if cmd == "restart": return "run"
			elif cmd == "exit": return "end"

		
		# Start screen code (before game has started)
		if not has_game_started:
			game_paused = True
			cmd = game_state_functions.Start_Screen(screen, Start_screen, Player, Tabs, Resume_Wrapper, 
										  Resume_Button, settings_wrapper, res_slider, Exit_Wrapper, Exit_Button,
										  pauseMenuText)
			if cmd == "play": return "run"
			elif cmd == "exit": return "end"

		
		# End screen code (after finishing the final level)
		if is_game_over:
			game_paused = True
			cmd = game_state_functions.End_Screen(screen, end_screen, Player, Tabs, Exit_Wrapper, Exit_Button,
										  pauseMenuText, ENDMenuText)
			if cmd == "exit": return "end"


		pygame.display.flip()

		# Player.facing = ((ColIDX*1) * math.pi/180)  # used to give player constant rotation
		Player.shooting = False  # Players shooting is set to False at end of Frame to stop shooting
		ColIDX += 1  # used for rainbow

	return return_command



# 1. PyCharm recognises it as a run-able file
if __name__ == "__main__":

	command = "run"
	has_game_started = False
	while command != "end":

		if CurrentGameState == 1:  # Game State
			command = GameState1(has_game_started)
			has_game_started = True

		if command[:2] == "gm":
			CurrentGameState = int(command[-1])

		if command == "next": 
			MAP_IMG_PATH = MAP_IMG_PATH[:-5] + str(int(MAP_IMG_PATH[-5:-4]) + 1) + ".png"

	pygame.quit()