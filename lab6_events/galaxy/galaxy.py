import pygame
from random import randint
import numpy as np
pygame.init()

dt = 1
font_size = 72
window_width = 1366
window_height = 768
FPS = 60

font = pygame.font.SysFont('timesnewromanboldttf', 72)
window = pygame.display.set_mode((window_width, window_height))
background = pygame.image.load('images/background.jpg')
background = pygame.transform.scale(background, (window_width, window_height))


def update_score(score, nickname):
    with open('Scores') as file:
        top_list = file.readlines()
    top_scores = []
    for player in top_list:
        tmp = player.split()
        tmp[0] = int(tmp[0])
        top_scores.append(tmp)
    top_scores.append([int(score), nickname])
    top_scores.sort()
    output = open('Scores', 'w')
    for i in range(len(top_scores) - 10, len(top_scores), 1):
        output.write(f"{top_scores[i][0]} {top_scores[i][1]}\n")
    output.close()



def explode():
    bomb_0 = pygame.image.load('bomb.png')
    for i in range(0, 60, 1):
        bomb = pygame.transform.scale(bomb_0, (i * 10, i * 10))
        window.blit(bomb, (window_width / 2 - i * 5, window_height / 2 - i * 5))
        pygame.display.update()
        clock.tick(FPS)


def lose():
    global planets, time, score, missed
    nickname = input('Your nickname: ')
    update_score(score, nickname)
    planets = []
    time = -dt
    score = 0
    missed = 0
    window.blit(background, (0, 0))
    pygame.draw.line(window, (0, 0, 0), (0, 100), (window_width, 100), 5)


class planet():

    def __init__ (self, x, y, r, form, vx, vy, alive = True, time = 0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.alive = alive
        self.time = time
        self.r = r
        self.form = pygame.image.load(f"images/planet{form}.png")
        self.score = (160 - r) // 10 + max(self.vx, self.vy)

    def update (self):
        self.x += self.vx * dt
        if (self.x + self.r >= window_width):
            self.vx = -abs(self.vx)
        if (self.x <= 0):
            self.vx = abs(self.vx)
        self.y += self.vy * dt
        if (self.y + self.r >= window_height):
            self.vy = -abs(self.vy)
        if (self.y <= 0):
            self.vy = abs(self.vy)
        self.time += dt
        sprite = pygame.transform.scale(self.form, (self.r, self.r))
        window.blit(sprite, (self.x, self.y))

    def live (self, pos):
        s = (pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2
        if (s <= self.r ** 2):
            self.alive = False

def rand_planet():
    return planet(
                randint(100, window_width - 100),
                randint(205, window_height - 100),
                randint(50,150),
                randint(3,20),
                randint(1,10),
                randint(1,10),
                )

pygame.display.update()
clock = pygame.time.Clock()
finished = False
planets = []
time = -dt
score = 0
missed = 0

while not finished:

    window.blit(background, (0, 0))
    miss = True

    clock.tick(FPS)
    time += dt
    new_planets = []
    click = (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                explode()
                score += len(planets)
                planets.clear()
                new_planets.clear()
                window.blit(background, (0, 0))
            else:
                click = event.pos

    if (time % 180 == 0):
        planets.append(rand_planet())
    for planet_i in planets:
        planet_i.update()
        planet_i.live(click)
        if (planet_i.alive == False):
            miss = False
        if planet_i.time >= 1000:
            planet_i.alive = False
            missed += 10
            score -= planet_i.score
        if (planet_i.alive == True):
            new_planets.append(planet_i)
        else:
            score += planet_i.score

    if ((miss == True) and not (click == (0, 0))):
        missed += 1

    planets = new_planets

    score_string = font.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(score_string, (0,0))

    missed_string = font.render("Missed: " + str(missed), 1, (255, 255, 255))
    window.blit(missed_string, (window_width / 2, 0))

    if (missed == 100):
        lose()

    pygame.display.update()


pygame.quit()
