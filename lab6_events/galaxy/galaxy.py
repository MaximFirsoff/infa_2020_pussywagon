import pygame
from random import randint

pygame.init()

dt = 1
font_size = 72
window_width = 1366
window_height = 768
FPS = 60

WHITE = (255, 255, 255)

font = pygame.font.SysFont('comicsans', 72)
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Galaxy game')
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
    for i in range(0, 60, 1):
        bomb = pygame.transform.scale(pygame.image.load('images/bomb.png'),
                                      (i * 10, i * 10) )
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


class Planet():

    def __init__ (self, alive = True, time = 0):
        self.x = randint(100, window_width - 100)
        self.y = randint(205, window_height - 100)
        self.vx = randint(-10,10)
        self.vy = randint(-10,10)
        self.alive = alive
        self.time = time
        self.r = randint(50,150)
        self.form = pygame.image.load(f"images/planet{randint(3,20)}.png")
        self.score = (160 - self.r) // 10 + max(abs(self.vx), abs(self.vy))

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



pygame.display.update()
clock = pygame.time.Clock()
playing = True
planets = []
time = -dt
score = 0
missed = 0

while playing:

    window.blit(background, (0, 0))
    miss = True

    clock.tick(FPS)
    time += dt
    new_planets = []
    click = (-1000, -1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                explode()
                for planet in planets:
                    score += planet.score
                planets.clear()
                new_planets.clear()
                window.blit(background, (0, 0))
            else:
                click = event.pos

    if (time % 180 == 0):
        planets.append(Planet())
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

    if ((miss == True) and not (click == (-1000, -1000))):
        missed += 1

    planets = new_planets

    score_string = font.render("Score: " + str(score), 1, WHITE)
    window.blit(score_string, (0,0))

    missed_string = font.render("Missed: " + str(missed), 1, WHITE)
    window.blit(missed_string, (window_width / 2, 0))

    if (missed == 100):
        lose()

    pygame.display.update()


pygame.quit()
