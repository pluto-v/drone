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
bulX = [-50, -50, -50]
bulY = [-50, -50, -50]
bulTarX = [-50, -50, -50]
bulTarY = [-50, -50, -50]
bulOrgX = [-50, -50, -50]
bulOrgY = [-50, -50, -50]
bulMaxSpeed = 20  # not sure exact thing
maxReload = 30  # two shots per sec
reload = 0
curBul = 0

# initialize land
landImg = pygame.image.load("land.png")
landX = -50


while True:
    screen.fill(sky)

    # counting down timers
    reload += -1

    # moving plane, accelerates instead of instant movement for more smoothness
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] == 1 and acc > -3 and 10 < pY:
        acc += - 0.25
    elif pY >= disHeight - 75:
        # CRASH
        # pY = disHeight - 75
        # acc = 0
        screen.fill((200,0,0))
        pygame.display.update()
        print ("YOU CRASHED")
        time.sleep(1)
        sys.exit()

    elif acc < 3:
        acc += 0.25
    pY += acc

    # updates plane image
    screen.blit(planeImg, (pX, pY))

    # shooting
    mouse = pygame.mouse.get_pressed()
    if mouse[0] == 1 and reload <= 0:
        # get mouse position
        curBul += 1
        if curBul > 2:
            curBul = 0
        mousePos = pygame.mouse.get_pos()
        bulTarX[curBul] = mousePos[0]
        bulTarY[curBul] = mousePos[1]
        bulX[curBul] = pX + 60
        bulY[curBul] = pY + 30
        bulOrgX[curBul] = bulX[curBul]
        bulOrgY[curBul] = bulY[curBul]
        # test if it works
        # pygame.draw.rect(screen, (255,255,255), (mouseX - 10, mouseY - 10, 20, 20), 0)
        reload = maxReload

    # if bullet is in air
    for i in range(3):
        if bulTarX[i] > -25 and bulTarY[i] > -25 and bulX[i] < disLength + 100 and bulY[i] < disHeight + 100:
            bulSpeed = math.sqrt(((bulTarX[i] - bulOrgX[i]) ** 2) + ((bulTarY[i] - bulOrgY[i]) ** 2))
            ratio = bulMaxSpeed / bulSpeed
            travelX = (bulTarX[i] - bulOrgX[i]) * ratio
            travelY = (bulTarY[i] - bulOrgY[i]) * ratio
            bulX[i] += travelX
            bulY[i] += travelY

            screen.blit(bulImg, (bulX[i], bulY[i]))

    screen.blit(landImg, (landX, disHeight - 125))

    pygame.display.update()  # updates display

    clock.tick(60)  # should make it 60FPS max
    # exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

pygame.quit()
quit()

