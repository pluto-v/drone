import pygame
import sys
import random
import pyganim
import time
import math

'''
TO DO LIST:
- add enemies (done)
- moving landscape (done)
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
expImg = pygame.image.load("explode.png")
bulImg = pygame.image.load("bullet.png")
bulX = [-50, -50, -50, -50]
bulY = [-50, -50, -50, -50]
bulTarX = [-50, -50, -50, -50]
bulTarY = [-50, -50, -50, -50]
bulOrgX = [-50, -50, -50, -50]
bulOrgY = [-50, -50, -50, -50]
bulExploded = [False, False, False, False]
bulMaxSpeed = 20  # num of units per game tick that bullet moves, def 20
maxReload = 30  # num ticks before u can shoot again, def 30 (2 shots /sec)
reload = 0
curBul = 0

# initialize land/obstacles
landImg = pygame.image.load("land.png")
landX = 10

# intialize enemy bullet stuff


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
        bulExploded[curBul] = False
        # test if it works
        # pygame.draw.rect(screen, (255,255,255), (mouseX - 10, mouseY - 10, 20, 20), 0)
        reload = maxReload

    # if bullet is in air
    for i in range(4):
        if bulTarX[i] > -25 and bulTarY[i] > -25 and bulX[i] < disLength + 100 and bulY[i] < disHeight + 100 and bulExploded[i] == False:
            bulSpeed = math.sqrt(((bulTarX[i] - bulOrgX[i]) ** 2) + ((bulTarY[i] - bulOrgY[i]) ** 2))
            ratio = bulMaxSpeed / bulSpeed
            travelX = (bulTarX[i] - bulOrgX[i]) * ratio
            travelY = (bulTarY[i] - bulOrgY[i]) * ratio
            bulX[i] += travelX
            bulY[i] += travelY

            screen.blit(bulImg,(bulX[i] + 2, bulY[i] + 2))


    # moving the land
    landX -= 5 # Also use this to adjust plane speed

    if landX < -2550:
        landX = -10

    screen.blit(landImg, (landX, disHeight - 160))

    # checking for ground collision, has to be here due it checking colour, if we find a diff way move it back
    colour = screen.get_at((int(pX + 40), int(pY + 30)))
    # colour of most of ground (green part): (168, 224, 101, 255) RGBA
    if pY >= disHeight - 51 or colour == (168,224,101,255):
        # CRASH
        # pY = disHeight - 75
        # acc = 0
        screen.fill((200,0,0))
        pygame.display.update()
        print ("YOU CRASHED")
        time.sleep(1)
        sys.exit()

    # checking for bullet collission
    for i in range(4):
        # ground
        if bulExploded[i] == True:
            bulX[i] += -5
            screen.blit(expImg, (bulX[i] + 2, bulY[i] + 2))
            if bulX[i] < bulTarX[i] - 60:
                bulX[i] = -50
                bulTarX[i] = -50
                bulExploded[i] = False

        elif bulX[i] > 1 and bulY[i] > 1 and bulX[i] < disLength - 1 and bulY[i] < disHeight - 1:
            colour = screen.get_at((int(bulX[i]) + 2, int(bulY[i]) + 2))
            if colour == (168,224,101,255):
                bulTarX[i] = bulX[i]
                bulExploded[i] = True

    # updates display
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)

    # exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

pygame.quit()
quit()

