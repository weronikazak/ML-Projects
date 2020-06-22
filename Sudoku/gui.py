import numpy as np
import pygame
from pygame.locals import *
import sys
from logic import TABLICA, iterating, find_zero, print_tab


pygame.init()


WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 43, 43)

SIZE = 55
COUNT = 9

NUM_PADDING = 10
FONT_SIZE = SIZE - 2*NUM_PADDING

FONT = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

screen = pygame.display.set_mode((SIZE*COUNT, SIZE*COUNT))
pygame.display.set_caption("Sudoku")
screen.fill(WHITE)


def guess(tab):
	zero = find_zero(tab)

	if zero is None:
		return True
	else:
		x, y = zero

	for i in range(1, 10):
		if iterating(i, x, y, tab):
			draw_single_number(i, x, y, tab)
			tab[x][y] = i

			if guess(tab): return True

			tab[x][y] = 0
	return False


def clear(tab):
	screen.fill(WHITE)
	draw_grid()
	draw_numbers(tab)
	# draw_numbers(TABLICA, RED)


def draw_grid():
	for x in range(0, SIZE*COUNT, SIZE):
		if x % 3*SIZE == 0:
			pygame.draw.line(screen, BLACK, (x, 0), (x, SIZE*COUNT))
		else:
			pygame.draw.line(screen, GRAY, (x, 0), (x, SIZE*COUNT))

	for y in range(0, SIZE*COUNT, SIZE):
		if y % 3*SIZE == 0:
			pygame.draw.line(screen, BLACK, (0, y), (SIZE*COUNT, y))
		else:
			pygame.draw.line(screen, GRAY, (0, y), (SIZE*COUNT, y))


def draw_numbers(tab, color=BLACK):
	for x in range(COUNT):
		for y in range(COUNT):
			if tab[x][y] == 0:
				continue
			cell_s = FONT.render(str(tab[x][y]), True, color)
			cell_rect = cell_s.get_rect()
			cell_rect.center = (y*SIZE + SIZE/2, x*SIZE + SIZE/2)
			screen.blit(cell_s, cell_rect)



def draw_single_number(i,x, y, tab):
	clear(tab)
	cell_s = FONT.render(str(i), True, RED)
	cell_rect = cell_s.get_rect()
	cell_rect.center = (y*SIZE + SIZE/2, x*SIZE + SIZE/2)
	screen.blit(cell_s, cell_rect)
	pygame.display.update()
	pygame.time.wait(60)


if __name__ == "__main__":
	start = False
	SUDOKU = TABLICA[:]

	clear(SUDOKU)
	while True:
		if start:
			guess(SUDOKU)
		for event in pygame.event.get():			
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				start = True
		pygame.display.update()

