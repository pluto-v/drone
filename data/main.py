import pygame
import sys
import random
import time
import math

'''
TO DO LIST:
- add rare boss
- music
- sound effects

CONTROLS:
w to fly up
Click to shoot (may not work with mousepad - try a mouse)
Spacebar to speed boost (might not be kept in final version of game, has a cooldown)
'''

# initiate pygame
pygame.init()
pygame.font.init()

# initialize random stuff()
disLength = 800
disHeight = 400
screen = pygame.display.set_mode((disLength,disHeight))

pygame.display.set_caption("drone")
clock = pygame.time.Clock()

# score and colours
score = 0
scoreTimer = 0
scoreMaxTimer = 20  # delay between giving score, in game ticks (60 = 1sec)
scoreFont = pygame.font.SysFont('Courier New', 20)

sky = (100,150,250)

# initialize plane
crashed = False
planeImg = pygame.image.load("data/drone.png")
pX = 25
pY = 50
acc = 0
forwardSpeed = 5  # def 5

# SPEEDDDD BOOOSSTT
boosted = False
superSpeed = 10
fuel = 200  # max 200
delay = 10

# initialize bullets
expImg = pygame.image.load("data/explode.png")
bulImg = pygame.image.load("data/bullet.png")
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
landImg = pygame.image.load("data/land.png")
landX = 0

# intialize enemies
enemyImg = pygame.image.load("data/enemy.png")
enemyDmgImg = pygame.image.load("data/enemyDmg.png")
enemyDeadImg = pygame.image.load("data/enemyDead.png")
enemyBulImg = pygame.image.load("data/enemyBullet.png")
maxHP = 2  # def 2
enemyX = [-100]
enemyY = [100]
eBulX = [-100]
eBulY = [100]
eBulTarX = [-50]
eBulTarY = [-50]
eBulOrgX = [-50]
eBulOrgY = [-50]
eNextBul = 0
enemyHP = [maxHP]
eCD = 0
bossMode = False
bossAcc = 0
for i in range (4):  # max 4 enemies at once
    enemyX.append(-100)
    enemyY.append(100)
    enemyHP.append(maxHP)
for i in range(10):  # max 10 enemy bullets at once
    eBulX.append(-50)
    eBulY.append(-50)
    eBulTarX.append(-50)
    eBulTarY.append(-50)
    eBulOrgX.append(-50)
    eBulOrgY.append(-50)

enemyTimer = random.randint(10,50)
nextEnemy = 0

while True:
    screen.fill(sky)

    # counting down timers
    reload += -1
    if bossMode == False:
        enemyTimer += -1
    eCD += -1
    scoreTimer += -1
    if scoreTimer <= 0:

        scoreTimer = scoreMaxTimer
        score += 1

    # moving plane, accelerates instead of instant movement for more smoothness
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE] == 1 and fuel > 1:
        boosted = True
        fuel += -2
        delay = 45
    # fly up and down
    elif pressed[pygame.K_w] == 1 and acc > -3 and 10 < pY:
        acc += - 0.25
        planeImg = pygame.image.load("data/droneUp.png")
        boosted = False
        # refuel
        if fuel < 200 and delay <= 0:
            fuel += 1
        else:
            delay += - 1
    elif 10 > pY or pressed[pygame.K_w] == 0 and acc < 3:
        acc += 0.25
        planeImg = pygame.image.load("data/drone.png")
        boosted = False
        # refuel
        if fuel < 200 and delay <= 0:
            fuel += 1
        else:
            delay += - 1

    # SPEED BOOOST
    if not boosted:
        forwardSpeed = 5
    else:
        forwardSpeed = superSpeed
        acc = 0
        planeImg = pygame.image.load("data/DroneSuperSpeed.png")

    pY += acc

    # updates plane image
    screen.blit(planeImg, (pX, pY))

    # shooting
    mouse = pygame.mouse.get_pressed()
    if mouse[0] == 1 and reload <= 0 and forwardSpeed != superSpeed:
        # get mouse position
        curBul += 1
        if curBul > 3:
            curBul = 0
        mousePos = pygame.mouse.get_pos()
        bulTarX[curBul] = mousePos[0]
        bulTarY[curBul] = mousePos[1]
        bulX[curBul] = pX + 80
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

            screen.blit(bulImg,(bulX[i], bulY[i]))


    # moving the land
    landX -= forwardSpeed # Also use this to adjust plane speed

    if landX < -2550:
        landX = -10

    screen.blit(landImg, (landX, disHeight - 170))


    # SPAWN ENEMIES
    if enemyTimer <= 0:
        enemyTimer = random.randint(80,160)  # def 80 - 160
        nextEnemy += 1
        if nextEnemy > 3:
            nextEnemy = 0

        for i in range(6):
            colour = screen.get_at((disLength - 5, disHeight - 110 + i * 10))
            if colour == (167,223,100,255):
                enemyY[nextEnemy] = disHeight - 170 + i * 10
                break
            else:
                enemyY[nextEnemy] = disHeight - 100

        if random.randint(0,5) == 1:  # 1/30 chance of a boss
            bossMode = True
            enemyHP[nextEnemy] = 15
            enemyY[nextEnemy] = disHeight - 140
        else:
            bossMode = False
            enemyHP[nextEnemy] = maxHP
        enemyX[nextEnemy] = disLength

    # move enemies forward
    for i in range(4):
        # YES BOSS
        if bossMode:
            if enemyX[i] > 550:
                enemyX[i] += -2
            elif enemyX[i] < 520:
                enemyX[i] += - forwardSpeed
            else:
                if enemyY[i] >= disHeight - 150:
                    bossAcc = -1
                elif enemyY[i] <= 50:
                    bossAcc = 1
            enemyY[i] += bossAcc

            screen.blit(enemyImg, (enemyX[i], enemyY[i]))

            # SHOOTING FOR ENEMY
            if eCD <= 0 and random.randint(1, 10) == 1 and enemyHP[i] > 0 and enemyX[i] > 75:
                eCD = 150
                for j in range(3):
                    eNextBul += 1
                    if eNextBul > 10:
                        eNextBul = 0
                    eBulX[eNextBul] = enemyX[i] + 15
                    eBulY[eNextBul] = enemyY[i] + 5

                    eBulTarY[eNextBul] = pY - 85 + (j*100)
                    eBulTarX[eNextBul] = pX + 300 - pY
                    eBulOrgX[eNextBul] = enemyX[i] + 15
                    eBulOrgY[eNextBul] = enemyY[i] + 5

        # NO BOSS
        elif enemyX[i] > -70:
            enemyX[i] -= forwardSpeed
            if enemyHP[i] <= 0:
                screen.blit(enemyDeadImg, (enemyX[i], enemyY[i]))
            elif enemyHP[i] <= maxHP / 2:
                screen.blit(enemyDmgImg, (enemyX[i], enemyY[i]))
            else:
                screen.blit(enemyImg, (enemyX[i], enemyY[i]))

            # SHOOTING FOR ENEMY
            if eCD <= 0 and random.randint(1,30) == 1 and enemyHP[i] > 0 and enemyX[i] > 75:
                eCD = 100
                eNextBul += 1
                if eNextBul > 10:
                    eNextBul = 0
                eBulX[eNextBul] = enemyX[i] + 15
                eBulY[eNextBul] = enemyY[i] + 5

                eBulTarY[eNextBul] = pY + 15
                eBulTarX[eNextBul] = pX + 300 - pY
                eBulOrgX[eNextBul] = enemyX[i] + 15
                eBulOrgY[eNextBul] = enemyY[i] + 5

    # checking for ground collision, has to be here due it checking colour, if we find a diff way move it back
    colour = screen.get_at((int(pX + 40), int(pY + 30)))
    # colour of most of ground (green part): (168, 224, 101, 255) RGBA
    if pY >= disHeight - 51 or colour == (167,223,100,255) or colour == (254,81,84,255):
        # CRASH
        # pY = disHeight - 75
        # acc = 0
        time.sleep(0.5)
        screen.fill((200,0,0))
        pygame.display.update()
        print ("YOU CRASHED")
        time.sleep(1)
        sys.exit()

    # checking for bullet collission
    for i in range(4):
        # ground
        if bulExploded[i]:
            bulX[i] -= forwardSpeed
            screen.blit(expImg, (bulX[i] - 10, bulY[i] - 10))
            if bulX[i] < bulTarX[i] - 60:
                bulX[i] = -50
                bulTarX[i] = -50
                bulExploded[i] = False

        # if bullet hits ground or enemy
        # 255,82,85,255 is colour of enemy
        elif disLength - 1 > bulX[i] > 6 and disHeight - 9 > bulY[i] > 9:
            colour = screen.get_at((int(bulX[i]), int(bulY[i])))
            colour2 = screen.get_at((int(bulX[i] - 2), int(bulY[i] + 8)))
            if colour == (167,223,100,255) or colour == (254,81,84,255) or\
                            colour2 == (167,223,100,255) or colour2 == (254,81,84,255):
                bulTarX[i] = bulX[i]
                bulExploded[i] = True

                # do dmg to enemies
                for j in range(4):
                    if bulX[i] - 45 < enemyX[j] + 25 < bulX[i] + 45 and bulY[i] - 60 < enemyY[j] + 10 < bulY[i] + 60:
                        enemyHP[j] -= 1
                        if enemyHP[j] == 0:
                            score += 20

    # moving and displaying enemy bullets that are in the air
    for i in range(10):
        if eBulX[i] < -20 or eBulY[i] < -20:
            eBulX[i] = - 50

        elif eBulX[i] > 0 and eBulY[i] > 0:
            bulSpeed = math.sqrt(((eBulTarX[i] - eBulOrgX[i]) ** 2) + ((eBulTarY[i] - eBulOrgY[i]) ** 2))
            ratio = 5 / bulSpeed
            travelX = (eBulTarX[i] - eBulOrgX[i]) * ratio
            travelY = (eBulTarY[i] - eBulOrgY[i]) * ratio
            eBulX[i] += travelX - 3  # - 3 cuz plane is flying for
            eBulY[i] += travelY

            # if speed boost is activated
            if boosted:
                eBulX[i] -= (forwardSpeed - 5)

            # hitting the player
            if pY + 5 < eBulY[i] < pY + 30 and pX + 25 < eBulX[i] < pX + 100:
                time.sleep(0.5)
                screen.fill((200, 0, 0))
                pygame.display.update()
                time.sleep(1)
                sys.exit()
            screen.blit(enemyBulImg, (eBulX[i], eBulY[i]))

    # SCORES
    scoreText = str(score)
    textSurface = scoreFont.render(("score:"+ scoreText), False, (0, 0, 0))
    screen.blit(textSurface, (disLength - 140, 10))

    # Draw fuel
    pygame.draw.rect(screen, (250, 100, 100), (disLength - 40, 40, 20, fuel / 2), 0)
    pygame.draw.rect(screen, (0,0,0), (disLength - 40, 40, 20, 100), 4)

    # updates display
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)

    # exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

pygame.quit()
quit()


