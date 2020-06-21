import numpy as np

TABLICA = [ [0, 8, 4, 3, 0, 0, 1, 0, 0],
			[9, 0, 0, 0, 0, 2, 0, 0, 4],
			[0, 0, 0, 0, 1, 0, 0, 0, 7],
			[0, 0, 3, 0, 2, 0, 0, 4, 0],
			[0, 9, 0, 0, 0, 1, 0, 0, 0],
			[1, 0, 0, 5, 0, 0, 3, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 5, 0],
			[0, 0, 0, 0, 0, 6, 0, 0, 0]
		]

size = len(TABLICA)


def print_tab(tab):
	for i1, row in enumerate(tab):
		if i1 % 3 == 0 and i1 != 0:
			print("-- --- --- --- --- --- --- --- --- --- --")

		line = "   " + str(row[0])
		for i2, pos in enumerate(row[1:]):
			if i2 % 3 == 2:
				spaces = "   |   "
			else: spaces = "  "

			line += spaces + str(pos)
		print(line, "\n")


def guess(tab):
	zero = find_zero(tab)

	if zero is None:
		return True
	else:
		x, y = zero

	for i in range(1, size+1):
		if iterating(i, x, y, tab):
			tab[x][y] = i

			if guess(tab):
				return True
			
			tab[x][y] = 0
	return False


def find_zero(tab):
	for x in range(size):
		for y in range(size):
			if tab[x][y] == 0:
				return (x, y)
	return None


def iterating(num, row, col, tab):
	# checking row
	for i in range(size):
		if tab[row][i] is num and col is not i:
			return False

	# checking col
	for i in range(size):
		if tab[i][col] is num and row is not i:
			return False

	bx = col // 3
	by = row // 3

	for i in range(by*3, (by+1)*3):
		for j in range(bx*3, (bx+1)*3):
			if tab[i][j] is num and (j, i) is not (row, col):
				return False
	return True
			


print_tab(TABLICA)
guess(TABLICA)
print("                        ")
print("                        ")
print("                        ")
print_tab(TABLICA)