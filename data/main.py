import pygame
import sys
import random
import time
import math
import pickle

'''
TO-DO list:
- polish then add to play stores
CONTROLS:
w to fly up
Click to shoot (may not work with mousepad - try a mouse)
Spacebar to speed boost (might not be kept in final version of game, has a cooldown)
SECRET CONTROL - press E and W together on menu screen to do the boss training scenario (also good for debugging)
KNOWN BUGS:
- boss hitboxes may not work if hitting to the far right of it
- inf boost
- delayed sound
'''

# initiate pygame
pygame.mixer.pre_init(44100, 16, 4, 4096)
pygame.init()
pygame.font.init()
time.sleep(1)

while True:
    # initialize random stuff()
    dead = False
    disLength = 800
    disHeight = 400
    screen = pygame.display.set_mode((disLength,disHeight))

    # MUSIC NOTE (pun not intended): .wav files must be 16bit to work (.wav is also recommended, mp3 is buggy)
    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)
    atkSound = pygame.mixer.Sound('data/attackSound.wav')
    expSound = pygame.mixer.Sound('data/explodeSound.wav')

    try:
        with open('data/config.dat', 'rb') as file:
            hi_score = pickle.load(file)
    except:
        hi_score = 0

    pygame.display.set_caption("drone")
    clock = pygame.time.Clock()

    # = = = START THE GAME - SPLASH SCREEN = = = #
    pygame.mixer.music.load("data/titleMusic.mp3")
    pygame.mixer.music.play(-1)

    splashFont = pygame.font.SysFont("Courier New", 30)

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

        label = splashFont.render("Hi Score: %d" % hi_score, 1, (0, 0, 0))
        screen.blit(label, (20, 300))

        pygame.display.update()

    # =============================================
    # score and colours
    score = 0
    scoreTimer = 0
    scoreMaxTimer = 20  # delay between giving score, in game ticks (60 = 1sec)
    scoreFont = pygame.font.SysFont('Courier New', 20)
    levelFont = pygame.font.SysFont('Courier New', 15)

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
    dmgBossImg = pygame.image.load("data/damagedBoss.png")
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
    bossSpawn = 0 # makes boss spawning more common if it doesnt spawn, or vice versa
    bossLevel = 0  # increments by one every defeated boss, starts at 0 (displayed as level 1 though)
    bossMaxHp = 15 + (bossLevel * 5)
    bossTrain = False
    # boss training demo
    if pressed[pygame.K_e]:
        bossSpawn = 30
        bossLevel = 1  # level 2 starts
        bossMaxHp = 15 + (bossLevel * 5)
        bossTrain = True

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

    pygame.mixer.music.load("data/backgroundMusic.mp3")
    pygame.mixer.music.play(-1)
    while not dead:
        screen.fill(sky)

        # counting down timers
        reload += -1
        if True not in enemyBoss:
            enemyTimer += -(forwardSpeed / 5)
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
            # shooting sound
            atkSound.play()

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
                enemyHP[nextEnemy] = bossMaxHp
                enemyX[nextEnemy] = disLength + 25
                enemyY[nextEnemy] = disHeight - 169
                # boss music!
                pygame.mixer.music.load('data/bossMusic.mp3')
                pygame.mixer.music.play(-1)
            # spawn normal enemy
            else:
                enemyBoss[nextEnemy] = False
                enemyHP[nextEnemy] = maxHP
                bossSpawn += 2  # boss gets more common
                enemyX[nextEnemy] = disLength

        # Enemy logic
        for i in range(4):

            # YES BOSS
            if enemyBoss[i]:
                # moving boss up and down
                if enemyX[i] > disLength - 200:
                    enemyX[i] += -2

                    # Boss healthbar + level indication
                    pygame.draw.rect(screen, (250, 25, 25), (enemyX[i] + 15, enemyY[i] + 85, (enemyHP[i] * 80 / bossMaxHp), 15), 0)
                    pygame.draw.rect(screen, (0, 0, 0), (enemyX[i] + 15, enemyY[i] + 85, 80, 15), 2)
                    lvlSurface = levelFont.render(("lvl " + str(bossLevel + 1)), False, (240, 240, 100))
                    screen.blit(lvlSurface, (enemyX[i] - 40, enemyY[i] + 85))

                else:
                    if enemyY[i] >= disHeight - 170:
                        bossAcc = -1
                    elif enemyY[i] <= 50:
                        bossAcc = 1
                    enemyY[i] += bossAcc

                    # boss death
                    if enemyHP[i] <= 0:
                        if enemyY[i] < disHeight - 100:
                            enemyY[i] += 3
                        enemyX[i] += - 5
                        if enemyX[i] <= -90:
                            pygame.mixer.music.load("data/backgroundMusic.mp3")
                            pygame.mixer.music.play(-1)
                            enemyBoss[i] = False
                    else:

                        # Boss healthbar and levels
                        pygame.draw.rect(screen, (250, 25, 25), (enemyX[i] + 15, enemyY[i] + 85, (enemyHP[i] * 80 / bossMaxHp), 15), 0)
                        pygame.draw.rect(screen, (0, 0, 0), (enemyX[i] + 15, enemyY[i] + 85, 80, 15), 2)
                        lvlSurface = levelFont.render(("lvl " + str(bossLevel + 1)), False, (240, 240, 100))
                        screen.blit(lvlSurface, (enemyX[i] - 40, enemyY[i] + 85))

                if enemyHP[i] < bossMaxHp * 0.5:
                    screen.blit(dmgBossImg, (enemyX[i], enemyY[i]))
                else:
                    screen.blit(bossImg, (enemyX[i], enemyY[i]))

                # SHOOTING FOR BOSS
                if eCD <= 0 and random.randint(0, 15) == 1 and enemyHP[i] > 0 and enemyX > disLength - 240:
                    eCD = 150 - (bossLevel * 5)
                    if eCD < 100:
                        eCD = 100
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
                # level 2 and above boss gets bonus attack
                elif 65 >= eCD >= 63 and bossLevel >= 1 and random.randint(0 + bossLevel, 5 + bossLevel) >= 5\
                        and enemyX > disLength - 240 and enemyHP[i] > 0:
                    eCD += - 10
                    if bossLevel >= 4:  # level 5 and up shooting
                        for j in range(2):
                            eNextBul += 1
                            if eNextBul > 10:
                                eNextBul = 0
                            eBulX[eNextBul] = enemyX[i] + 15
                            eBulY[eNextBul] = enemyY[i] + 40

                            eBulTarX[eNextBul] = pX + 150
                            eBulTarY[eNextBul] = pY - 70 + (j * 120)
                            eBulOrgX[eNextBul] = eBulX[eNextBul]
                            eBulOrgY[eNextBul] = eBulY[eNextBul]
                    else:  # other level shooting
                        eNextBul += 1
                        eCD += - 10
                        if eNextBul > 10:
                            eNextBul = 0
                        eBulX[eNextBul] = enemyX[i] + 15
                        eBulY[eNextBul] = enemyY[i] + 40

                        eBulTarX[eNextBul] = pX + 150
                        eBulTarY[eNextBul] = pY - 15
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
                    eCD = 85 - (bossLevel * 3)
                    if eCD < 60:
                        eCD = 60
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
            if score > hi_score:
                with open('data/config.dat', 'wb') as file:
                    pickle.dump(score, file)
            splashScreen = pygame.image.load("data/dead.png")
            screen.blit(splashScreen, (0, 0))
            textSurface = scoreFont.render(("score:" + scoreText), False, (0, 0, 0))
            screen.blit(textSurface, (disLength - 140, 10))
            dead = True
            pygame.display.update()
            time.sleep(1)

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
                    expSound.play()

                    # do dmg to enemies
                    for j in range(4):
                        if bulX[i] - 45 < enemyX[j] + 25 < bulX[i] + 45 and bulY[i] - 60 < enemyY[j] + 10 < bulY[i] + 60:
                            enemyHP[j] -= 1
                            # enemy died
                            if enemyHP[j] == 0:
                                score += 20
                                # bonus score in boss mode
                                if enemyBoss[j] == True:
                                    score += 100 + (bossLevel * 40)  # 120 score for level 1 boss, 160 for level 2, etc
                                    # training scenario stuff
                                    if bossTrain == True:
                                        bossLevel += 2  # increases boss level by 2 if training.
                                        bossSpawn = 30
                                    else:  # normal game
                                        bossLevel += 1

                                    bossMaxHp = 15 + (bossLevel * 5)

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
                    if score > hi_score:
                        with open('data/config.dat', 'wb') as file:
                            pickle.dump(score, file)
                    splashScreen = pygame.image.load("data/dead.png")
                    screen.blit(splashScreen, (0, 0))
                    textSurface = scoreFont.render(("score:" + scoreText), False, (0, 0, 0))
                    screen.blit(textSurface, (disLength - 140, 10))
                    dead = True
                    pygame.display.update()
                    time.sleep(1)

        # SCORES
        scoreText = str(score)
        textSurface = scoreFont.render(("score:"+ scoreText), False, (0, 0, 0))
        screen.blit(textSurface, (disLength - 140, 10))

        # Draw fuel
        pygame.draw.rect(screen, (125, 225, 250), (disLength - 40, 40, 20, fuel / 2), 0)
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



