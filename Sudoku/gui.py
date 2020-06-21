import numpy as np
import pygame
from pygame.locals import *
import sys

pygame.init()
screen = pygame.display.set_mode((400, 300))

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
