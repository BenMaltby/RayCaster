import pygame
from GenerateChunkMapFromImage import GenerateChunks, DIMENSIONS, coordToIDX
from aStar import PathfindingBoard, sNode
from VOBJ import createVector

WIDTH = 800
HEIGHT = 800
FPS = 30
CELLSIZE = 8

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Entity:
	def __init__(self, x, y, col):
		self.pos = createVector(x, y)
		self.col = col

	def UP(self, speed): self.pos.y -= speed
	def RIGHT(self, speed): self.pos.x += speed
	def DOWN(self, speed): self.pos.y += speed
	def LEFT(self, speed): self.pos.x -= speed
	def Check_Collision(self, Map):
		self.MapCell = [self.pos.x // CELLSIZE, self.pos.y // CELLSIZE]  # calculates map cell of new player position

		if 0 < self.pos.x < DIMENSIONS*CELLSIZE:  # if player is withing bounds of map
			if 0 < self.pos.y < DIMENSIONS*CELLSIZE:

				if Map[int(coordToIDX(self.MapCell[0], self.MapCell[1]))] == 2:  # if players new position is withing wall tile
					return True

				return False  # if not in wall tile, then not in collision

		return True  # if player not in wall tile but leaves bounds of map then return in collision

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PathFinding Test")
clock = pygame.time.Clock()  # For syncing the FPS

# Map data
ChunkedMap, Map, PlayerSpawn, sp = GenerateChunks("MapFiles/Level_1_v5.png")  # Generates a ChunkSystem of GameBoard Image
ai_nodeGraph = PathfindingBoard(Map, DIMENSIONS, CELLSIZE)
ai_nodeGraph.nodeStarts.append(ai_nodeGraph.nodeArray[0])
ai_nodeGraph.nodeEnd = ai_nodeGraph.nodeArray[-1]
ai_nodeGraph.Solve_AStar(ai_nodeGraph.nodeStarts[0])
shortest_path = ai_nodeGraph.getPath()


def display_nodes(screen, nGraph: PathfindingBoard):
	if nGraph.nodeArray:
		for idx, node in enumerate(nGraph.nodeArray):
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(node.x - 4, node.y - 4, nGraph.cellSize, nGraph.cellSize))
			for jdx, neighbor in enumerate(node.Neighbours):
				pygame.draw.line(screen, (0,255,0), (node.x, node.y), (neighbor.x, neighbor.y))


def display_path(screen, path: list):
	for i in range(len(path)-1):
		pygame.draw.line(screen, (160, 0, 255), (path[i][0], path[i][1]), (path[i+1][0], path[i+1][1]), 5)



def player1Movement(keys, sp, Map, ent: Entity):
	if keys[pygame.K_a]:  # a = STRAFE LEFT
		ent.LEFT(sp)
		if ent.Check_Collision(Map):
			ent.RIGHT(sp)
	if keys[pygame.K_d]:  # d = STRAFE RIGHT
		ent.RIGHT(sp)
		if ent.Check_Collision(Map):
			ent.LEFT(sp)
	if keys[pygame.K_w]:  # w = FORWARD
		ent.UP(sp)
		if ent.Check_Collision(Map):
			ent.DOWN(sp)
	if keys[pygame.K_s]:  # s = BACKWARDS
		ent.DOWN(sp)
		if ent.Check_Collision(Map):
			ent.UP(sp)
	if not keys:
		return False
	else:
		return True

def player2Movement(keys, sp, Map, ent: Entity) -> None:
	if keys[pygame.K_LEFT]:  # a = STRAFE LEFT
		ent.LEFT(sp)
		if ent.Check_Collision(Map):
			ent.RIGHT(sp)
	if keys[pygame.K_RIGHT]:  # d = STRAFE RIGHT
		ent.RIGHT(sp)
		if ent.Check_Collision(Map):
			ent.LEFT(sp)
	if keys[pygame.K_UP]:  # w = FORWARD
		ent.UP(sp)
		if ent.Check_Collision(Map):
			ent.DOWN(sp)
	if keys[pygame.K_DOWN]:  # s = BACKWARDS
		ent.DOWN(sp)
		if ent.Check_Collision(Map):
			ent.UP(sp)


Player = Entity(PlayerSpawn[0] * CELLSIZE + (CELLSIZE / 2), PlayerSpawn[1] * CELLSIZE + (CELLSIZE / 2), (160,97,0))
Enemy  = Entity(PlayerSpawn[0] * CELLSIZE + (CELLSIZE / 2), PlayerSpawn[1] * CELLSIZE + (CELLSIZE / 2), (255,0,0))
Enemy2 = Entity(PlayerSpawn[0] * CELLSIZE + (CELLSIZE / 2), PlayerSpawn[1] * CELLSIZE + (CELLSIZE / 2), (255,0,255))

enemies = [Enemy, Enemy2]
paths = []

def display_entity(screen, ent: Entity):
	pygame.draw.circle(screen, ent.col, (ent.pos.x, ent.pos.y), CELLSIZE)

# Game loop
running = True
time = 0
pPos, ePos = createVector(Player.pos.x, Player.pos.y), createVector(Enemy.pos.x, Enemy.pos.y)
while running:
	clock.tick(FPS)     # will make the loop run at the same speed all the time
	for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
		# listening for the X button at the top
		if event.type == pygame.QUIT:
			running = False

	if time % 100 == 0:  # and (pPos != Player.pos or ePos != Enemy.pos):
		paths = []
		ai_nodeGraph.nodeStarts = []
		for jdx, enemy in enumerate(enemies):
			ai_nodeGraph.nodeStarts.append(ai_nodeGraph.nodeGrid.chunkMap[f'{int(enemy.pos.x//CELLSIZE)} {int(enemy.pos.y//CELLSIZE)}'][0])
		ai_nodeGraph.nodeEnd = ai_nodeGraph.nodeGrid.chunkMap[f'{int(Player.pos.x//CELLSIZE)} {int(Player.pos.y//CELLSIZE)}'][0]
		for idx, node in enumerate(ai_nodeGraph.nodeStarts):
			ai_nodeGraph.Solve_AStar(node)
			paths.append(ai_nodeGraph.getPath())

	pPos, ePos = createVector(Player.pos.x, Player.pos.y), createVector(Enemy.pos.x, Enemy.pos.y)

	keysPressed = pygame.key.get_pressed()  # inputs
	player1Movement(keysPressed, 5, Map, Player)
	player2Movement(keysPressed, 4, Map, Enemy)
	player2Movement(keysPressed, 8, Map, Enemy2)

	screen.fill(BLACK)

	display_nodes(screen, ai_nodeGraph)
	# if len(shortest_path) < 15:
	for path in paths:
		display_path(screen, path)

	display_entity(screen, Player)
	display_entity(screen, Enemy)
	display_entity(screen, Enemy2)

	# Done after drawing everything to the screen
	pygame.display.flip()
	time += 1

pygame.quit()