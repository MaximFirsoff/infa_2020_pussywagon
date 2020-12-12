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

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))
PLAYER_0 = pygame.image.load(os.path.join("kenney_platformercharacters", "PNG", "Player", "Poses", "player_stand.png"))
PLAYER_1 = pygame.image.load(os.path.join("kenney_platformercharacters", "PNG", "Player", "Poses", "player_walk1.png"))
PLAYER_2 = pygame.image.load(os.path.join("kenney_platformercharacters", "PNG", "Player", "Poses", "player_walk2.png"))
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
ZOMBIE = pygame.image.load(os.path.join("kenney_platformercharacters", "PNG", "Zombie", "Poses", "zombie_stand.png"))
class Player:
    def __init__(self, x, y, speed = 5):
        self.x = x
        self.y = y
        self.speed = speed
        self.img_0 = PLAYER_0
        self.time = 0
        self.img = PLAYER_0
        self.cooldown = 0

    def draw(self):
        window.blit(self.img, (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, direction):
        if direction == "UP":
            self.img = pygame.transform.rotate(self.img_0, 0)
            self.y -= self.speed
        if direction == "DOWN":
            self.img = pygame.transform.rotate(self.img_0, 180)
            self.y += self.speed
        if direction == "RIGHT":
            self.img = pygame.transform.rotate(self.img_0, -90)
            self.x += self.speed
        if direction == "LEFT":
            self.img = pygame.transform.rotate(self.img_0, 90)
            self.x -= self.speed
    def moving(self):
        if (self.time // 5) % 2 == 1:
            self.img_0 = PLAYER_1
        else:
            self.img_0 = PLAYER_2

class Bullet():
    def __init__ (self, x, y, cos, sin, angle, color, speed = 20):
        self.x = x
        self.y = y
        self.cos = cos
        self.sin = sin
        self.speed = speed
        self.type = COLOR_MAP[color]
        self.angle = - (angle / math.pi)*180 - 90

    def move(self):
        self.y += self.speed * self.cos
        self.x += self.speed * self.sin

    def draw(self):
        self.img = pygame.transform.rotate(self.type, self.angle)
        window.blit(self.img, (self.x, self.y))

class Enemy():

    def __init__ (self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(205, HEIGHT - 100)
        self.alive = True
        self.img = ZOMBIE
        self.r = 20

    def update (self):
        self.x += random.randint(-10,10)
        self.y += random.randint(-10,10)

    def draw(self):
        window.blit(self.img, (self.x, self.y))

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
    player = Player(WIDTH/2, HEIGHT/2)
    bullets = []
    new_bullets = []
    enemies = []
    new_enemies = []
    time = 0
    def redraw_window():
        window.blit(BG, (0,0))
        #draw statistics
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        score_label = main_font.render(f"Score: {score}", 1, (255,255,255))
        window.blit(lives_label, (10,10))
        window.blit(score_label, (WIDTH - 10 - score_label.get_width(), 10))
        player.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in new_enemies:
            enemy.draw()
        pygame.display.update()

    while run:
        clock.tick(FPS)
        time += 1
        if player.cooldown > 0:
            player.cooldown -= 1
        player.time += 1
        bullets = new_bullets
        new_bullets = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # SHIP AND BULLETS
        player.img = PLAYER_0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.moving()
            player.move("UP")
        if keys[pygame.K_a]:
            player.moving()
            player.move("LEFT")
        if keys[pygame.K_s]:
            player.moving()
            player.move("DOWN")
        if keys[pygame.K_d]:
            player.moving()
            player.move("RIGHT")
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if player.cooldown == 0:
                (x, y) = pygame.mouse.get_pos()
                if x-player.x == 0:
                    x = player.x + 1
                angle = math.atan ((y - player.y) / (x - player.x))
                sin = (x - player.x) / math.sqrt( (x - player.x) ** 2 + (y - player.y) ** 2 )
                cos = (y - player.y) / math.sqrt( (x - player.x) ** 2 + (y - player.y) ** 2 )
                bullets.append(Bullet(player.x, player.y, cos, sin, angle, random.choice(["red", "yellow", "blue", "green"])))
                player.cooldown = 10
        for bullet in bullets:
            bullet.move()
            if (0 < bullet.x < WIDTH) and (0 < bullet.y < HEIGHT):
                new_bullets.append(bullet)

        # ENEMIES
        enemies = new_enemies
        new_enemies = []
        if (time % 180 == 0):
            enemies.append(Enemy())
        for enemy in enemies:
            enemy.update()
        for enemy in enemies:
            for bullet in bullets:
                enemy.live(bullet)
            if (enemy.alive == True):
                new_enemies.append(enemy)


        redraw_window()

main()
