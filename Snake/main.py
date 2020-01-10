import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        # change our position

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows # width/height of each cube
        i = self.pos[0] #current row
        j = self.pos[1] # current column

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        # poprzez mnożenie row i column przez szerokosc i wysokosc
        # każdego klocka mozemy zdeterminowac gdzie to narysowac

        if eyes:
            centre = dis//2 # // to forcing dzielenia na liczbe integrer
            radius = 3
            circle_middle = (i*dis+centre-radius, j*dis+8)
            circle_middle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) # head will be at the fron of the snake
        self.body.append(self.head) # add head to body list

        # representatives of directions the snake is moving
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]



            for i, c in enumerate(self.body): #loop through every cube in snakes body
                p = c.pos[:] # store cubes position on the grid
                # znak [:] odwoluje sie do wszystkich elementy w tablicy

                if p in self.turns: # jeśli aktualna pozycja klocka jest gdzie skręcilismy
                    turn = self.turns[p] # znajdz kierunek w ktory snake powinien skręcić
                    c.move(turn[0], turn[1])  # porusz klockiem w tym kierunku
                    if i == len(self.body)-1: # jeśli to ostatni klocek w ciele
                        self.turns.pop(p) # .. to usuń go z tabeli
                else: # if we are not turning the cube

                    # jeśli klocek dotknie jakiegoś końca ekranu,
                    # to nim przerzuci na drugą stronę
                    if c.dirnx == -1 and c.pos[0] <= 0:
                        c.pos = (c.rows-1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                        c.pos = (0, c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows -1:
                        c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0:
                        c.pos = (c.pos[0], c.rows-1)
                    else:
                        c.move(c.dirnx, c.dirny) # jeśli nie doknal krawedzi, po prostu niech idzie dalej
            
                

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # check the directioon snake is moving in to
        # determine where a cube is neede (left, right, above, below)

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube(tail.pos[0]+1, tail.pos[1]))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        # set the cues direction to the direction of the snake
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0: # na pierwszym klocku oczy
                c.draw(surface, True)
            else:
                c.draw(surface)

def draw_grid(w, rows, surface):
    size_between = w // rows # gives the distance between the lines

    x = 0 # keeps the track of current x
    y = 0 # keeps the track of current y
    for l in range(rows): # draw one vertical and one horizntal line each loop
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, x), (w, y))

def redraw_window(surface):
    global rows, width, snack, s
    surface.fill((0, 0, 0)) # fills the screen with black
    snack.draw(surface)
    s.draw(surface)   
    draw_grid(width, rows, surface)
    pygame.display.update()

def random_snack(rows, item):
    positions = item.body # wszystkie pozycje klockow w snake'u

    # keep generating random positions until we get a valid ne
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            # check if the generated position is occupied by the snake
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    flag = True
    clock = pygame.time.Clock()

    snack = cube(random_snack(rows, s), color=(0, 255, 0))

    while flag:
        pygame.time.delay(50) # delay the game if it doesnt run too quickly
        clock.tick(10) # ensure the game runs at 10 FPS
        s.move()

        if s.body[0] == snack.pos: # checks if the head collides with the snack
            s.add_cube() # adds a new cube to the snake
            snack = cube(random_snack(rows, s), color=(0, 255, 0)) # creates a new snack object

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                # check if any of the positions in snake body list overlap
                print('Score: ', len(s.body))
                message_box('You lost!', 'Play again...')
                s.reset((10, 10))
                break
        
        redraw_window(win) # refresh the screen


main()