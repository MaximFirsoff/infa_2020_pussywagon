import pygame
import pygame.draw
from pygame import gfxdraw

with open('list_leaves') as f:
    lines = f.readlines()
matrix_leaves = []
for line in lines:
    coefs = list(map(float, line.split()))
    matrix_leaves.append(coefs)
leaves = len(matrix_leaves)

with open('list_arcs') as q:
    lines = q.readlines()
matrix_arcs = []
for line in lines:
    coefs = list(map(float, line.split()))
    matrix_arcs.append(coefs)
arcs = len(matrix_arcs)

with open('list_lines') as h:
    lines = h.readlines()
matrix_lines = []
for line in lines:
    coefs = list(map(float, line.split()))
    matrix_lines.append(coefs)
lines_count = len(matrix_lines)

with open('background_color') as g:
    lines = g.readlines()
background_color = []
for line in lines:
    background_color = list(map(float, line.split()))



FPS = 30
screen_width = 981
screen_height = 654
screen = pygame.display.set_mode((screen_width, screen_height))

class leaf: # Объект лист
    def __init__ (self, height, width, x, y, angle, color=(0, 104, 52)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.angle = angle

    def draw (self):
        background_color = (255, 177, 129)
        surf = pygame.Surface((3 * self.width, self.height))
        surf.fill(background_color)
        pygame.draw.ellipse(surf, self.color, (0, 0, self.width, self.height))
        surf.set_colorkey(background_color)
        surf_new = pygame.transform.rotate(surf, self.angle)
        surf_new.set_alpha(255)
        screen.blit(surf_new, (self.x, self.y))

class bamboo: # Объект бамбук
    def __init__ (self, height, width, x, y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def draw (self, leaves, list, lines_count, matrix_lines, arcs, matrix_arcs):
        for i in range (leaves): # Рисуем листья
            leafi = leaf(
                        list[i][0] * self.height,
                        list[i][1] * self.width,
                        self.x + list[i][2] * self.width,
                        self.y + list[i][3] * self.height,
                        list[i][4],
            )
            leafi.draw()
        for i in range (lines_count): # Рисуем ствол
            pygame.draw.line(
                screen,
                leafi.color,
                (self.x - matrix_lines[i][0] * self.width, self.y - matrix_lines[i][1] * self.height),
                (self.x - matrix_lines[i][2] * self.width, self.y - matrix_lines[i][3] * self.height),
                int(self.width * matrix_lines[i][4]),
            )
        for i in range (arcs): # Рисуем ветки
            pygame.draw.arc(
                screen,
                leafi.color,
                (self.x - matrix_arcs[i][0] * self.width, self.y - matrix_arcs[i][1] * self.height,
                int(self.width * matrix_arcs[i][2]), int(self.height * matrix_arcs[i][3])),
                matrix_arcs[i][4],
                matrix_arcs[i][5],
                int(self.width * matrix_arcs[i][6]),
            )



pygame.draw.rect(screen, background_color, (0, 0, screen_width, screen_height))

#b = bamboo(360, 20, 800, 368)
#b.draw(leaves, matrix_leaves, lines_count, matrix_lines, arcs, matrix_arcs)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()

pygame.quit()
