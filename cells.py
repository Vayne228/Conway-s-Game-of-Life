import pygame
import random
import sys
import time

X_MAX = 500
Y_MAX = 500
CELL_SIZE = 25
pygame.init()
playSurface = pygame.display.set_mode((X_MAX, Y_MAX))
fpsController = pygame.time.Clock()
green = pygame.Color(0,255,0)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)

matrix = []

class matrix_cell():
    def __init__(self, x, y, size):
        self.size = size
        self.x = x * self.size
        self.y = y * self.size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.live = False
        self.neibours = 0
                 
def create_matrix(size):
    l = {}
    for i in range(Y_MAX//size):
        for j in range(X_MAX//size):
            l.update({(i, j): matrix_cell(i, j, size)})
    return l

def get_neibours(matrix, x, y):
    neibours = 0
    #if 0 < y < Y_MAX//CELL_SIZE-1 and 0 < x < X_MAX//CELL_SIZE-1:
    #    dx = [-1, 0, 1]
    #    dy = [-1, 0, 1]
    
    #elif x==0:
    #    dx = [X_MAX//CELL_SIZE-1, 0, 1]
    if y == 0:
        dy = [Y_MAX//CELL_SIZE-1, 0, 1]
    elif y == Y_MAX//CELL_SIZE-1:
        dy = [-1, 0, -Y_MAX//CELL_SIZE+1]
    else:
        dy = [-1, 0, 1]
        
    if x == 0:
        dx = [X_MAX//CELL_SIZE-1, 0, 1]
    elif x == X_MAX//CELL_SIZE-1:
        dx = [-1, 0, -X_MAX//CELL_SIZE+1]
    else:
        dx = [-1, 0, 1]
    for delx in dx:
        for dely in dy:
            if matrix[x+delx, y+dely].live:
                if not (delx==0 and dely==0):
                    neibours += 1
    return neibours

def draw_matrix(surface, matrix):
    for cords, rec in matrix.items():
        if rec.live:
            pygame.draw.rect(surface, green, rec.rect)
            pygame.draw.rect(surface, black, rec.rect, 1)
        else:
            pygame.draw.rect(surface, black, rec.rect, 1)

def clicked(matrix, x, y):
    if matrix[x//CELL_SIZE, y//CELL_SIZE].live:
        matrix[x//CELL_SIZE, y//CELL_SIZE].live = False
    else:
        matrix[x//CELL_SIZE, y//CELL_SIZE].live = True
    #print(x//CELL_SIZE, y//CELL_SIZE)

def update_state(matrix):
    for j in range(Y_MAX//CELL_SIZE):
        for i in range(X_MAX//CELL_SIZE):
            matrix[i,j].neibours = get_neibours(matrix, i, j)
            
    for j in range(Y_MAX//CELL_SIZE):
        for i in range(X_MAX//CELL_SIZE):
            if (matrix[i,j].live and matrix[i,j].neibours in [2, 3]) or ( not matrix[i,j].live and matrix[i,j].neibours == 3):
                matrix[i,j].live = True
            else:
                matrix[i,j].live = False

M = create_matrix(CELL_SIZE)
Start = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == ord('s'):
                if Start:
                    Start = False
                else:
                    Start = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x , y = event.pos
            clicked(M, x, y)
    playSurface.fill(white)
    draw_matrix(playSurface,M)
    if Start:
        update_state(M)
    pygame.display.flip()
    fpsController.tick(3) 
