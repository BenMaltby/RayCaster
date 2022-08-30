import pygame
import colorsys
import MapProcessing

WIDTH = 800
HEIGHT = 800
FPS = 30

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


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


getTicksLastFrame = 0
ColIDX = 0  # keep for rainbow
running = True
while running:

    r, g, b = hsv2rgb(((ColIDX+0.3)/100) % 3, 1, 1)

    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 15.0
    getTicksLastFrame = t

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    MapProcessing.renderMap2D(screen)

    pygame.display.flip()

    ColIDX += 1

pygame.quit()
