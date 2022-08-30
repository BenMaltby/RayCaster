import pygame
import math

WIDTH = 800
HEIGHT = 800
FPS = 30
PATH = "Player2Dsprite.png"
RADIAN = math.pi / 180

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

## initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sprite testing")
clock = pygame.time.Clock()


# class Player(pygame.sprite.Sprite):
# 	def __init__(self, imagePath) -> None:
# 		super().__init__()
# 		self.pos = [0, 0]
# 		self.facing = 0
# 		self.image = pygame.image.load(imagePath)
# 		self.rect = self.image.get_rect()

# 	def update(self):
# 		self.rect.center = [self.pos[0], self.pos[1]]


# player = Player(PATH)
# player_group = pygame.sprite.Group()
# player_group.add(player)
img = pygame.image.load(PATH)
img.set_colorkey((0,0,0))

angle = 0
## Game loop
running = True
while running:
	angle += 2

	clock.tick(FPS)
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT:
			running = False

	#3 Draw/render
	screen.fill(BLACK)

	x, y = 400, 400
	img_copy = pygame.transform.rotate(img, angle)
	screen.blit(img_copy, (x - int(img_copy.get_width() / 2), y - int(img_copy.get_height() / 2)))


	## Done after drawing everything to the screen
	pygame.display.flip()       

pygame.quit()