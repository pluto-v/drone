import pygame
import sys
import random
import pyganim
import time
import math


# initiate pygame
pygame.init()

# initialize random stuff (e.g. colours)
disLength = 800
disHeight = 400
screen = pygame.display.set_mode((disLength,disHeight))

pygame.display.set_caption("drone")
clock = pygame.time.Clock()

# colours
sky = (70,110,220)

# initialize plane
crashed = False
planeImg = pygame.image.load("drone.png")
pX = 50
pY = 50
acc = 0

# initialize bullets
bulImg = pygame.image.load("bullet.png")
bulX = -50
bulY = -50
bulTarX = 0
bulTarY = 0
bulSpeed = 20  # not sure exact thing
reload = 30  # two shots per sec

while True:
    screen.fill(sky)

    # counting down timers
    reload += -1

    # moving plane, accelerates instead of instant movement for more smoothness
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] == 1 and acc > -3:
        acc += - 0.25
    elif acc < 3:
        acc += 0.25
    pY += acc

    # updates plane image
    screen.blit(planeImg, (pX, pY))

    # shooting
    mouse = pygame.mouse.get_pressed()
    if mouse[0] == 1 and reload <= 0:
        # get mouse position
        mousePos = pygame.mouse.get_pos()
        bulTarX = mousePos[0] * 10
        bulTarY = mousePos[1] * 10
        # set bullet to gun position on plane sprite
        bulX = pX + 60
        bulY = pY + 30

        # test if it works
        # pygame.draw.rect(screen, (255,255,255), (mouseX - 10, mouseY - 10, 20, 20), 0)

        reload = 30

    # if bullet is in air
    if bulTarX > 25 and bulTarY > 25:
        # eBulSpeed = math.sqrt(abs(yDiff) ** 2 + abs(xDiff) ** 2)
        # ratio = 350 / eBulSpeed
        # # set bullet to certain speed
        # yDiff *= ratio
        # xDiff *= ratio
        #
        # eShotY[i] += yDiff / 100
        # eShotX[i] += xDiff / 100

        xDiff = (bulTarX - bulX)
        yDiff = (bulTarY - bulY)
        ratio = bulSpeed / (math.sqrt(abs(xDiff) ** 2 + abs(yDiff) ** 2))
        xDiff *= ratio
        yDiff *= ratio
        bulX += xDiff
        bulY += yDiff

        screen.blit(bulImg, (bulX, bulY))

    pygame.display.update()  # updates display
    clock.tick(60)  # should make it 60FPS max

    # exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

pygame.quit()
quit()

