import pygame
import sys
import random
import pyganim
import time
import math

'''
TO DO LIST:
- add enemies
- moving landscape
- maybe high score stuff

'''

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
pX = 25
pY = 50
acc = 0

# initialize bullets
bulImg = pygame.image.load("bullet.png")
bulX = [-50, -50, -50, -50]
bulY = [-50, -50, -50, -50]
bulTarX = [-50, -50, -50, -50]
bulTarY = [-50, -50, -50, -50]
bulOrgX = [-50, -50, -50, -50]
bulOrgY = [-50, -50, -50, -50]
bulMaxSpeed = 20  # num of units per game tick that bullet moves, def 20
maxReload = 30  # num ticks before u can shoot again, def 30 (2 shots /sec)
reload = 0
curBul = 0

# initialize land/obstacles
landImg = pygame.image.load("land.png")
landX = -50

# intialize


while True:
    screen.fill(sky)

    # counting down timers
    reload += -1

    # moving plane, accelerates instead of instant movement for more smoothness
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] == 1 and acc > -3 and 10 < pY:
        acc += - 0.25
        planeImg = pygame.image.load("droneUp.png")
    elif 10 > pY or pressed[pygame.K_w] == 0 and acc < 3:
        acc += 0.25
        planeImg = pygame.image.load("drone.png")

    # checking for ground collision
    if pY >= disHeight - 75:
        # CRASH
        # pY = disHeight - 75
        # acc = 0
        screen.fill((200,0,0))
        pygame.display.update()
        print ("YOU CRASHED")
        time.sleep(1)
        sys.exit()

    pY += acc

    # updates plane image
    screen.blit(planeImg, (pX, pY))

    # shooting
    mouse = pygame.mouse.get_pressed()
    if mouse[0] == 1 and reload <= 0:
        # get mouse position
        curBul += 1
        if curBul > 3:
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
    for i in range(4):
        if bulTarX[i] > -25 and bulTarY[i] > -25 and bulX[i] < disLength + 100 and bulY[i] < disHeight + 100:
            bulSpeed = math.sqrt(((bulTarX[i] - bulOrgX[i]) ** 2) + ((bulTarY[i] - bulOrgY[i]) ** 2))
            ratio = bulMaxSpeed / bulSpeed
            travelX = (bulTarX[i] - bulOrgX[i]) * ratio
            travelY = (bulTarY[i] - bulOrgY[i]) * ratio
            bulX[i] += travelX
            bulY[i] += travelY

            screen.blit(bulImg, (bulX[i], bulY[i]))

    screen.blit(landImg, (landX, disHeight - 125))

    # updates display
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)

    # moving the land
    landX -= 10 # Also use this to adjust plane speed
    if landX < -2300:
        landX = 800

    # exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

pygame.quit()
quit()

