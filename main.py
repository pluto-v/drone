import pygame
import random


# initiate pygame
pygame.init()
pygame.font.init()

# initialize random stuff
displayLength = 800
displayHeight = 400
clock = pygame.time.Clock()

while True:
    pygame.display.update()  # updates display

    clock.tick(60)  # should make it 60FPS max
