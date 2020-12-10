import random
import pygame
import math
import time
import os
pygame.font.init()
pygame.init()

WIDTH = 1000
HEIGHT = 1000
window = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
BULLET_RED = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BULLET_GREEN = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BULLET_YELLOW = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
BULLET_BLUE = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
COLOR_MAP = {
            "red": BULLET_RED,
            "green": BULLET_GREEN,
            "blue": BULLET_BLUE,
            "yellow": BULLET_YELLOW,
}
class Ship:
    def __init__(self, x, y, speed = 5, angle = 1):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = 0

    def draw(self):
        self.img = pygame.transform.rotate(SHIP, self.angle)
        window.blit(self.img, (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, direction):
        pi_angle = self.angle / 180 * math.pi
        if direction == "UP":
            self.y -= self.speed * math.cos(pi_angle)
            self.x -= self.speed * math.sin(pi_angle)
        if direction == "DOWN":
            self.y += self.speed * math.cos(pi_angle)
            self.x += self.speed * math.sin(pi_angle)
        if direction == "RIGHT":
            self.x += self.speed * math.cos(pi_angle)
            self.y -= self.speed * math.sin(pi_angle)
        if direction == "LEFT":
            self.x -= self.speed * math.cos(pi_angle)
            self.y += self.speed * math.sin(pi_angle)

class Bullet():
    def __init__ (self, x, y, angle, color, speed = 20):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.type = COLOR_MAP[color]

    def move(self):
        pi_angle = self.angle / 180 * math.pi
        self.y -= self.speed * math.cos(pi_angle)
        self.x -= self.speed * math.sin(pi_angle)

    def draw(self):
        self.img = pygame.transform.rotate(self.type, self.angle)
        window.blit(self.img, (self.x, self.y))

class Planet():

    def __init__ (self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(205, HEIGHT - 100)
        self.vx = random.randint(-10,10)
        self.vy = random.randint(-10,10)
        self.alive = True
        self.r = random.randint(50,150)
        self.form = pygame.image.load(os.path.join("images", f"planet{random.randint(3,20)}.png"))
        self.score = (160 - self.r) // 10 + max(abs(self.vx), abs(self.vy))

    def update (self):
        self.x += self.vx
        if (self.x + self.r >= WIDTH):
            self.vx = -abs(self.vx)
        if (self.x <= 0):
            self.vx = abs(self.vx)
        self.y += self.vy
        if (self.y + self.r >= HEIGHT):
            self.vy = -abs(self.vy)
        if (self.y <= 0):
            self.vy = abs(self.vy)

    def draw(self):
        sprite = pygame.transform.scale(self.form, (self.r, self.r))
        window.blit(sprite, (self.x, self.y))

    def live (self, bullet):
        s = (bullet.x - self.x) ** 2 + (bullet.y - self.y) ** 2
        if (s <= self.r ** 2):
            self.alive = False

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    score = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    ship = Ship(WIDTH/2, HEIGHT/2)
    bullets = []
    new_bullets = []
    planets = []
    new_planets = []
    time = -1
    def redraw_window():
        window.blit(BG, (0,0))
        #draw statistics
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        score_label = main_font.render(f"Score: {score}", 1, (255,255,255))
        window.blit(lives_label, (10,10))
        window.blit(score_label, (WIDTH - 10 - score_label.get_width(), 10))
        ship.draw()
        for bullet in bullets:
            bullet.draw()
        for planet in new_planets:
            planet.draw()
        pygame.display.update()

    while run:
        clock.tick(FPS)
        time += 1
        bullets = new_bullets
        new_bullets = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # SHIP AND BULLETS
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            ship.move("UP")
        if keys[pygame.K_a]:
            ship.move("LEFT")
        if keys[pygame.K_s]:
            ship.move("DOWN")
        if keys[pygame.K_d]:
            ship.move("RIGHT")
        if keys[pygame.K_q]:
            ship.angle += ship.speed
        if keys[pygame.K_e]:
            ship.angle -= ship.speed
        if keys[pygame.K_SPACE]:
            bullets.append(Bullet(ship.x, ship.y, ship.angle, random.choice(["red", "yellow", "blue", "green"])))
        for bullet in bullets:
            bullet.move()
            if (0 < bullet.x < WIDTH) and (0 < bullet.y < HEIGHT):
                new_bullets.append(bullet)

        # PLANETS
        planets = new_planets
        new_planets = []
        if (time % 180 == 0):
            planets.append(Planet())
        for planet in planets:
            planet.update()
        for planet in planets:
            for bullet in bullets:
                planet.live(bullet)
            if (planet.alive == True):
                new_planets.append(planet)
            else:
                score += planet.score

        #LIVES
        for planet in new_planets:
            s = (planet.x - ship.x) ** 2 + (planet.y - ship.y) ** 2
            if math.sqrt(s) < planet.r:
                lives -= 1
                planet.alive = False
                score -= planet.score

        redraw_window()

main()
