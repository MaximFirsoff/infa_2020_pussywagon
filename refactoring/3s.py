import pygame
import pygame.draw
from pygame import gfxdraw

with open('list_bamboo') as p:
    lines = p.readlines()
matrix_bamboo = []
for line in lines:
    coefs = list(map(float, line.split()))
    matrix_bamboo.append(coefs)
bambooes = len(matrix_bamboo)

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

class leaf:
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

class bamboo:
    def __init__ (self, height, width, x, y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def leaves (self, leaves, list):
        for i in range (leaves):
            leafi = leaf(
                        list[i][0] * self.height,
                        list[i][1] * self.width,
                        self.x + list[i][2] * self.width,
                        self.y + list[i][3] * self.height,
                        list[i][4],
            )
            leafi.draw()

    def trunk (self, lines_count, matrix_lines):
        for i in range (lines_count):
            pygame.draw.line(
                screen,
                (0, 104, 52),
                (self.x - matrix_lines[i][0] * self.width, self.y - matrix_lines[i][1] * self.height),
                (self.x - matrix_lines[i][2] * self.width, self.y - matrix_lines[i][3] * self.height),
                int(self.width * matrix_lines[i][4]),
            )

    def branch (self, arcs, matrix_arcs):
        for i in range (arcs):
            pygame.draw.arc(
                screen,
                (0, 104, 52),
                (self.x - matrix_arcs[i][0] * self.width, self.y - matrix_arcs[i][1] * self.height,
                int(self.width * matrix_arcs[i][2]), int(self.height * matrix_arcs[i][3])),
                matrix_arcs[i][4],
                matrix_arcs[i][5],
                int(self.width * matrix_arcs[i][6]),
            )

    def draw (self, leaves, list, lines_count, matrix_lines, arcs, matrix_arcs):
        self.leaves(leaves, list)
        self.trunk(lines_count, matrix_lines)
        self.branch(arcs, matrix_arcs)


class panda:
    def __init__ (self, width, height, x, y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def head(self, x, y, width, height):
        pygame.draw.circle(screen, (0,0,0), (x,y), int(0.2*height))
        pygame.draw.circle(screen, (255,255,255), (x+int(0.2*width), y+int(0.3*height)), int(0.55*height))
        pygame.draw.circle(screen, (0,0,0), (x+int(0.3*width),y), int(0.2*height))
        pygame.draw.ellipse(screen, (0,0,0), (x-int(0.08*width), y+int(0.2*height), int(0.1*width), int(0.3*height)))
        pygame.draw.circle(screen, (0,0,0), (x+int(0.15*width),y+int(0.4*height)), int(0.14*height))
        pygame.draw.circle(screen, (0,0,0), (x+int(0.04*width),y+int(0.6*height)), int(0.07*height))

    def body(self, x, y, width, height):
        pygame.draw.circle(screen, (0,0,0), (x+int(0.9*width),y+int(0.3*height)), int(0.2*height))
        pygame.draw.ellipse(screen, (255,255,255), (x, y, width, height))
        pygame.draw.ellipse(screen, (255,255,255), (x, y+int(0.43*height), int(0.9*width), int(0.7*height)))

    def back_leg(self, x, y , width, height):
        pygame.draw.ellipse(screen, (0,0,0), (x+int(0.6*width),y+int(0.7*height), int(0.2*width), int(0.4*height)))

    def legs(self, x, y, width, height):
        pygame.draw.polygon(screen, (0, 0, 0), [(x+int(0.3*width),y+int(1)), (x+int(0.5*width),y+int(1)),
                                   (x+int(0.5*width),y+int(1*height)), (x+int(0.3*width),y+int(1*height))])
        pygame.draw.polygon(screen, (0, 0, 0), [(x,y, (x+int(0.1*width),y+int(0*height)),
                                   (x+int(0.2*width),y+int(1.2*height)), (x+int(0*width),y+int(1.5*height)), (x-int(0.05*width),y+int(1.2*height))])
        pygame.draw.polygon(screen, (0, 0, 0), [(x+int(0.25*width),y+int(1.5*height)), (x+int(0.55*width),y+int(1.4*height)),
                                   (x+int(0.5*width),y+int(1*height)), (x+int(0.3*width),y+int(1*height))])
        pygame.draw.ellipse(screen, (0,0,0), (x+int(0.2*width), y+int(1.25*height), int(0.3*width), int(0.3*height)))
        pygame.draw.ellipse(screen, (0,0,0), (x+int(0.25*width), y+int(1.25*height), int(0.3*width), int(0.3*height)))
        pygame.draw.ellipse(screen, (0,0,0), (x+int(0.28*width), y+int(1.30*height), int(0.25*width), int(0.3*height)))
        pygame.draw.ellipse(screen, (0,0,0), (x+int(0.23*width), y+int(1.30*height), int(0.3*width), int(0.20*height)))
        pygame.draw.ellipse(screen, (0,0,0), (x+int(0.20*width), y+int(1.30*height), int(0.3*width), int(0.30*height)))

        pygame.draw.ellipse(screen, (0,0,0), (x+int(0.85*width),y+int(0.45*height), int(0.2*width), int(0.9*height)))
        pygame.draw.ellipse(screen, (0,0,0), (x+int(0.8*width),y+int(0.95*height), int(0.2*width), int(0.4*height)))

    def draw(self):
        self.back_leg(self.x, self.y, self.width, self.height)
        self.body(self.x, self.y, self.width, self.height)
        self.legs(self.x, self.y, self.width, self.height)
        self.head(self.x, self.y, self.width, self.height)


pygame.draw.rect(screen, background_color, (0, 0, screen_width, screen_height))

for i in range(bambooes):
    bb = bamboo(matrix_bamboo[i][0], matrix_bamboo[i][1], matrix_bamboo[i][2], matrix_bamboo[i][3])
    bb.draw(leaves, matrix_leaves, lines_count, matrix_lines, arcs, matrix_arcs)

panda_small = panda(100, 50, 300, 500)
panda_small.draw()

panda_big = panda(250, 125, 500, 300)
panda_big.draw()

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
