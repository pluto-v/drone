import pygame
import sys
import random
import pyganim
import time


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

while True:
    screen.fill(sky)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # moving plane
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] == 1 and acc > -3:
        acc += - 0.25
    elif acc < 3:
        acc += 0.25
    pY += acc

    screen.blit(planeImg, (pX, pY))

    # shooting


    pygame.display.update()  # updates display
    clock.tick(60)  # should make it 60FPS max

# exiting
pygame.quit()
quit()

