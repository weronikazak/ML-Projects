import numpy as np
import pygame
from pygame.locals import *
import sys
from logic import TABLICA, iterating, find_zero, print_tab


pygame.init()

class Sudoku():
	self.WHITE = (255, 255, 255)
	self.GRAY = (200, 200, 200)
	self.BLACK = (0, 0, 0)
	self.RED = (255, 43, 43)

	self.SIZE = 55
	self.COUNT = 9

	self.NUM_PADDING = 10
	self.FONT_SIZE = self.SIZE - 2*self.NUM_PADDING

	self.FONT = pygame.font.Font('freesansbold.ttf', self.FONT_SIZE)


	def guess(self, tab):
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


	def clear(self, tab):
		self.SCREEN.fill(self.WHITE)
		draw_grid()
		draw_numbers(tab)


	def draw_grid(self):
		for x in range(0, self.SIZE*self.COUNT, self.SIZE):
			if x % 3*self.SIZE == 0:
				pygame.draw.line(self.SCREEN, self.BLACK, (x, 0), (x, self.SIZE*self.COUNT))
			else:
				pygame.draw.line(self.SCREEN, self.GRAY, (x, 0), (x, self.SIZE*self.COUNT))

		for y in range(0, SIZE*COUNT, SIZE):
			if y % 3*SIZE == 0:
				pygame.draw.line(self.SCREEN, self.BLACK, (0, y), (self.SIZE*self.COUNT, y))
			else:
				pygame.draw.line(self.SCREEN, self.GRAY, (0, y), (self.SIZE*self.COUNT, y))


	def draw_numbers(self, tab, color=self.BLACK):
		for x in range(self.COUNT):
			for y in range(self.COUNT):
				if tab[x][y] == 0:
					continue
				cell_s = self.FONT.render(str(tab[x][y]), True, color)
				cell_rect = cell_s.get_rect()
				cell_rect.center = (y*self.SIZE + self.SIZE/2, x*self.SIZE + self.IZE/2)
				self.SCREEN.blit(cell_s, cell_rect)



	def draw_single_number(self, i, x, y, tab):
		clear(tab)
		cell_s = self.FONT.render(str(i), True, self.RED)
		cell_rect = cell_s.get_rect()
		cell_rect.center = (y*self.SIZE + self.SIZE/2, x*self.SIZE + self.SIZE/2)
		self.SCREEN.blit(cell_s, cell_rect)
		pygame.display.update()
		pygame.time.wait(60)


if __name__ == "__main__":
	start = False
	SUDOKU = TABLICA

	SCREEN = pygame.display.set_mode((55*9, 55*9))
	pygame.display.set_caption("Sudoku")
	SCREEN.fill((255, 255, 255))

	clear(SCREEN, SUDOKU)
	while True:
		if start:
			guess(SCREEN, SUDOKU)
		for event in pygame.event.get():			
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				start = True
		pygame.display.update()

