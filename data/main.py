import pygame
import sys
import random
import time
import math

'''
TO DO LIST:
- music
- sound effects

CONTROLS:
w to fly up
Click to shoot (may not work with mousepad - try a mouse)
Spacebar to speed boost (might not be kept in final version of game, has a cooldown)

KNOWN BUGS:

'''

# initiate pygame
pygame.init()
pygame.font.init()

while True:
    pygame.mixer.music.stop()

    # initialize random stuff()
    dead = False
    disLength = 800
    disHeight = 400
    screen = pygame.display.set_mode((disLength,disHeight))

    pygame.display.set_caption("drone")
    clock = pygame.time.Clock()

    # = = = START THE GAME - SPLASH SCREEN = = = #
    while True:
        splashScreen = pygame.image.load("data/splash.png")
        screen.blit(splashScreen, (0, 0))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            dead = False
            break
        elif pressed[pygame.K_ESCAPE]:
            sys.exit()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        pygame.display.update()

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
    bossImg = pygame.image.load("data/bossImage.png")
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

    enemyBoss = [False]
    bossAcc = 0
    bossSpawn = 0  # makes boss spawning more common if it doesnt spawn, or vice versa
    for i in range (4):  # max 4 enemies at once
        enemyX.append(-100)
        enemyY.append(100)
        enemyHP.append(maxHP)
        enemyBoss.append(False)

    for i in range(10):  # max 10 enemy bullets at once
        eBulX.append(-50)
        eBulY.append(-50)
        eBulTarX.append(-50)
        eBulTarY.append(-50)
        eBulOrgX.append(-50)
        eBulOrgY.append(-50)

    enemyTimer = random.randint(10,50)
    nextEnemy = 0

    # =========== MAIN PROGRAM ============= #

    while not dead:
        screen.fill(sky)

        # counting down timers
        reload += -1
        if True not in enemyBoss:
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
            delay = 60
        # fly up and down
        elif pressed[pygame.K_w] == 1 and acc > -3 and 10 < pY:
            acc += - 0.25
            planeImg = pygame.image.load("data/droneUp.png")
            boosted = False
        elif 10 > pY or pressed[pygame.K_w] == 0 and acc < 3:
            acc += 0.25
            planeImg = pygame.image.load("data/drone.png")
            boosted = False

        # refuel
        if fuel < 200 and delay <= 0:
            fuel += 0.5
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
            mousePos = pygame.mouse.get_pos()
            reload = maxReload

            curBul += 1
            if curBul > 3:
                curBul = 0
            bulX[curBul] = pX + 80
            bulY[curBul] = pY + 30
            bulOrgX[curBul] = bulX[curBul]
            bulOrgY[curBul] = bulY[curBul]
            bulExploded[curBul] = False
            bulTarX[curBul] = mousePos[0]
            bulTarY[curBul] = mousePos[1]

            reload = maxReload

        # if bullet is in air
        for i in range(4):
            if bulTarX[i] > -25 and bulTarY[i] > -25 and bulX[i] < disLength + 100 and bulY[i] < disHeight + 100\
                    and bulExploded[i] == False:
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
        if True not in enemyBoss and enemyTimer <= 0:
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

            # spawning boss
            if random.randint(0,25) + bossSpawn >= 30:
                bossSpawn = 0
                enemyBoss[nextEnemy] = True
                enemyHP[nextEnemy] = 20
                enemyX[nextEnemy] = disLength + 25
                enemyY[nextEnemy] = disHeight - 169
                # boss music!
                pygame.mixer.music.load('data/backgroundMusic.mp3')
                pygame.mixer.music.play(-1)
            # spawn normal enemy
            else:
                enemyBoss[nextEnemy] = False
                enemyHP[nextEnemy] = maxHP
                bossSpawn += 1  # boss gets more common
                enemyX[nextEnemy] = disLength

        # Boss logic
        for i in range(4):

            # YES BOSS
            if enemyBoss[i]:
                # moving boss up and down
                if enemyX[i] > disLength - 200:
                    enemyX[i] += -2
                else:
                    if enemyY[i] >= disHeight - 170:
                        bossAcc = -1
                    elif enemyY[i] <= 50:
                        bossAcc = 1
                    enemyY[i] += bossAcc

                    # enemy death
                    if enemyHP[i] <= 0:
                        if enemyY[i] < disHeight - 100:
                            enemyY[i] += 3
                        enemyX[i] += - 5
                        if enemyX[i] <= -60:
                            pygame.mixer.music.stop()
                            enemyBoss[i] = False

                screen.blit(bossImg, (enemyX[i], enemyY[i]))

                # SHOOTING FOR BOSS
                if eCD <= 0 and random.randint(1, 10) == 1 and enemyHP[i] > 0 and enemyX > disLength - 240:
                    eCD = 120
                    for j in range(3):
                        eNextBul += 1
                        if eNextBul > 10:
                            eNextBul = 0
                        eBulX[eNextBul] = enemyX[i] + 15
                        eBulY[eNextBul] = enemyY[i] + 40

                        eBulTarY[eNextBul] = pY - 115 + (j*130)
                        eBulTarX[eNextBul] = pX + 150
                        eBulOrgX[eNextBul] = eBulX[eNextBul]
                        eBulOrgY[eNextBul] = eBulY[eNextBul]

            # NO BOSS, MOVE ENEMIES FORWARD
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
                    eCD = 80
                    eNextBul += 1
                    if eNextBul > 10:
                        eNextBul = 0
                    eBulX[eNextBul] = enemyX[i] + 15
                    eBulY[eNextBul] = enemyY[i] + 5

                    eBulTarY[eNextBul] = pY + 15
                    eBulTarX[eNextBul] = pX + 450 - (pY * 2) + (enemyX[i] / 8)
                    eBulOrgX[eNextBul] = enemyX[i] + eBulX[eNextBul]
                    eBulOrgY[eNextBul] = enemyY[i] + eBulY[eNextBul]

        # checking for ground collision, has to be here due it checking colour, if we find a diff way move it back
        colour = screen.get_at((int(pX + 40), int(pY + 30)))
        # colour of most of ground (green part): (168, 224, 101, 255) RGBA
        if pY >= disHeight - 51 or colour == (167,223,100,255) or colour == (254,81,84,255):
            time.sleep(0.5)
            dead = True
            pygame.display.update()
            time.sleep(0.5)

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
                                # bonus score in boss mode
                                if enemyBoss[j] == True:
                                    score += 130

        # moving and displaying enemy bullets that are in the air
        for i in range(10):
            if eBulX[i] < -40 or eBulY[i] < -40:
                eBulX[i] = - 50

            elif eBulX[i] > -20 and eBulY[i] > -20:
                bulSpeed = math.sqrt(((eBulTarX[i] - eBulOrgX[i]) ** 2) + ((eBulTarY[i] - eBulOrgY[i]) ** 2))
                ratio = 5 / bulSpeed
                travelX = (eBulTarX[i] - eBulOrgX[i]) * ratio
                travelY = (eBulTarY[i] - eBulOrgY[i]) * ratio
                eBulX[i] += travelX - 3  # - 3 cuz plane is flying for
                eBulY[i] += travelY

                # if speed boost is activated
                if boosted:
                    eBulX[i] -= (forwardSpeed - 5)

                screen.blit(enemyBulImg, (eBulX[i], eBulY[i]))

                # hitting the player
                if pY + 5 < eBulY[i] < pY + 30 and pX + 25 < eBulX[i] < pX + 100:
                    time.sleep(0.5)
                    dead = True
                    pygame.display.update()
                    time.sleep(0.5)

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


