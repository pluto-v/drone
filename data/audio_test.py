import pygame
import sys
import random
import time

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.font.init()

for i in range(4):
    atkSound = pygame.mixer.Sound("attackSound.wav")
    atkSound.play()
    time.sleep(1)

