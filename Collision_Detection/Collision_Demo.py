# NOT PART OF FINAL PROJECT JUST DEMO OF COLLISON DETECTION
import math
import pygame
import GEWY
import numpy as np
from VOBJ import createVector
import VOBJ

WIDTH = 700
HEIGHT = 600
FPS = 30
RA = math.pi / 2
RADIAN = math.pi / 180
SCALE_MAT = np.matrix('0.5 0; 0 0.5')
OFFSET_SPEED = 20

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Demo")
clock = pygame.time.Clock()

PlayerViewLockButton = GEWY.Button(5, 5, 20, 20, "View Player", False, (5, 0))
PlayerViewLockWrapper = GEWY.Wrapper(10, 40, 130, 30, [PlayerViewLockButton], "View")
GEWY.GUI_OBJECTS.append(PlayerViewLockWrapper)

tabs = GEWY.TabSystem()
tabs.addTab(PlayerViewLockWrapper)
GEWY.GUI_OBJECTS.append(tabs)


class CircOBJ:
    def __init__(self, x, y, sp):
        self.pos = createVector(x, y)
        self.vel = createVector()
        self.facing = 0
        self.radius = 25
        self.speed = sp
        self.torque = 8 * RADIAN

    def show(self, screen, velMag, viewWin):
        screenPoints = (viewWin[0] * np.matrix(f'{self.pos.x}; {self.pos.y}')).tolist()
        px, py = screenPoints[0][0] + viewWin[1].x, screenPoints[1][0] + viewWin[1].y
        pygame.draw.circle(screen, (0, 0, 0), (px, py), self.radius)
        pygame.draw.circle(screen, (120,120,120), (px, py), self.radius*0.92)
        pygame.draw.line(screen, (255, 255, 255), (self.pos.x, self.pos.y),
                         (self.radius * math.cos(self.facing) + self.pos.x,
                          self.radius * math.sin(self.facing) + self.pos.y))

        pygame.draw.line(screen, (0, 255, 0), (self.pos.x, self.pos.y),
                         (velMag.mag() * math.cos(math.atan2(velMag.y, velMag.x)) + self.pos.x,
                          velMag.mag() * math.sin(math.atan2(velMag.y, velMag.x)) + self.pos.y))

    def actorMovement(self, keys):
        if keys[pygame.K_j]:
            self.facing -= self.torque
        if keys[pygame.K_l]:
            self.facing += self.torque
        self.facing %= math.tau
        if keys[pygame.K_a]:  # a = STRAFE LEFT
            self.vel.add(createVector(math.cos(self.facing - RA), math.sin(self.facing - RA)))
        if keys[pygame.K_d]:  # d = STRAFE RIGHT
            self.vel.add(createVector(math.cos(self.facing + RA), math.sin(self.facing + RA)))
        if keys[pygame.K_w]:  # w = FORWARD
            self.vel.add(createVector(math.cos(self.facing), math.sin(self.facing)))
        if keys[pygame.K_s]:  # s = BACKWARDS
            self.vel.add(createVector(math.cos(self.facing + RA * 2), math.sin(self.facing + RA * 2)))

        currVel = createVector()
        if self.vel != createVector():
            self.vel.normalize()
            currVel = createVector(self.vel.x, self.vel.y)
            currVel.mult(15)
            self.vel.setMag(self.speed)
            self.pos.add(self.vel)
            self.vel.setMag(0)

        return currVel

def main():
    Actor = CircOBJ(WIDTH / 2, HEIGHT / 2, 5)

    scale = np.matrix('1.0 0.0; 0.0 1.0')

    running = True
    while running:

        # 1 Process input/events
        clock.tick(FPS)
        for event in pygame.event.get():
            mVec = pygame.mouse.get_pos()
            GEWY.handleEvents(event, mVec, screen)

            keysPressed = pygame.key.get_pressed()  # inputs
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    scale += SCALE_MAT
                if event.y < 0:
                    scale -= SCALE_MAT

        screen.fill((50, 50, 50))
        viewBox = [scale, createVector(WIDTH/2, HEIGHT/2)]

        pygame.draw.rect(screen, (0,0,0), pygame.Rect(250, 250, 100, 100))

        velMag = Actor.actorMovement(pygame.key.get_pressed())
        Actor.show(screen, velMag, viewBox)

        GEWY.display(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
