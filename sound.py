import time, sys
import pygame
import os
from pygame import mixer
mixer.init()

sound = pygame.mixer.Sound(os.path.join('data', 'Bubble_pop.wav'))

sound.play()

time.sleep(5)
