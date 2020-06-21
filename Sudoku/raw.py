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

def draw(tab):
	for i1, row in enumerate(tab):
		if i1 % 3 == 0 and i1 != 0:
			print("--- --- --- --- --- --- --- --- --- ---")

		line = "   " + str(row[0])
		for i2, pos in enumerate(row[1:]):
			if i2 % 3 == 2:
				spaces = "   |   "
			else: spaces = "  "

			line += spaces + str(pos)
		print(line, "\n")


def guess(tab):
	t = tab
	all_guesses = list(np.array(tab).flatten()).count(0)
	guess_tab = []

	for row in t:
		for pos in row:
			if pos == 0:
				i = 1
				while i not in row:
					i += 1
		t.index


if __name__ == "__main__":
	# draw(TABLICA)
	guess(TABLICA)