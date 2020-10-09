import pygame
from pygame.draw import *
from random import randint
pygame.init()

dt = 1
font_size = 72
screen_width = 1200
screen_height = 768
FPS = 60
background_color = (255, 177, 129)

font = pygame.font.SysFont('timesnewromanboldttf', 72)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.draw.rect(screen, background_color, (0, 0, screen_width, screen_height))
pygame.draw.line(screen, (0, 0, 0), (0, 100), (screen_width, 100), 5)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def explode():
    bomb_0 = pygame.image.load('bomb.png')
    for i in range(0, 60, 1):
        bomb = pygame.transform.scale(bomb_0, (i * 10, i * 10))
        screen.blit(bomb, (screen_width / 2 - i * 5, screen_height / 2 - i * 5))
        pygame.display.update()
        clock.tick(FPS)


def lose():
    global balls, time, score, missed
    output = open('Scores', 'a')
    nickname = input('Your nickname: ')
    output.write(f'{nickname} {score}\n')
    output.close()
    balls = []
    time = -dt
    score = 0
    missed = 0
    pygame.draw.rect(screen, background_color, (0, 0, screen_width, screen_height))
    pygame.draw.line(screen, (0, 0, 0), (0, 100), (screen_width, 100), 5)


class ball():

    def __init__ (self, x, y, r, color, vx, vy, alive = True, time = 0):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy
        self.alive = alive
        self.time = time

    def update (self):
        pygame.draw.circle(screen, background_color, (self.x, self.y), self.r)
        self.x += self.vx * dt
        if (self.x + self.r >= screen_width):
            self.x = screen_width - 1 - self.r
            self.vx = -self.vx
        if (self.x - self.r <= 0):
            self.x = 1 + self.r
            self.vx = -self.vx
        self.y += self.vy * dt
        if (self.y + self.r >= screen_height):
            self.y = screen_height - 1 - self.r
            self.vy = -self.vy
        if (self.y - self.r <= 105):
            self.y = 106 + self.r
            self.vy = -self.vy
        self.time += dt
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def live (self, pos):
        s = (pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2
        if (s <= self.r ** 2):
            self.alive = False

    def kill (self):
        pygame.draw.circle(screen, background_color, (self.x, self.y), self.r)


pygame.display.update()
clock = pygame.time.Clock()
finished = False
balls = []
time = -dt
score = 0
missed = 0

while not finished:

    miss = True

    clock.tick(FPS)
    time += dt
    new_balls = []
    click = (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                explode()
                score += len(balls)
                balls.clear()
                new_balls.clear()
                pygame.draw.rect(screen, background_color, (0, 105, screen_width, screen_height - 105))
            else:
                click = event.pos

    if (time % 180 == 0):
        balls.append( ball(
                        randint(100, screen_width - 100),
                        randint(205, screen_height - 100),
                        randint(0,100),
                        COLORS[randint(0, 5)],
                        randint(1,10),
                        randint(1,10),
                        ))
    for ball_i in balls:
        ball_i.update()
        ball_i.live(click)
        if (ball_i.alive == False):
            miss = False
        if ball_i.time == 600:
            ball_i.alive = False
            missed += 10
            score -= 1
        if (ball_i.alive == True):
            new_balls.append(ball_i)
        else:
            ball_i.kill()
            score += 1

    if ((miss == True) and not (click == (0, 0))):
        missed += 1

    balls = new_balls

    pygame.draw.rect(screen, background_color, (200, 10, 250, 60))
    score_string = font.render("Score: " + str(score), 1, (0, 0, 0))
    screen.blit(score_string, (0,0))

    pygame.draw.rect(screen, background_color, (200 + screen_width / 2, 10, 250 + screen_width / 2, 60))
    missed_string = font.render("Missed: " + str(missed), 1, (0, 0, 0))
    screen.blit(missed_string, (screen_width / 2, 0))

    if (missed == 100):
        lose()

    pygame.display.update()


pygame.quit()
