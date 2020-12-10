import pygame
import sys
import pygame.draw
import os
import math
import time
import random

FPS = 60

screen_width = 1000
screen_height = 850
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
black = (0, 0, 0)
white = (255, 255, 255)
hero_size = {'x': 10, 'y': 10}
hero_velocity = 350
mouse_pos = {'x':  screen_width/2,'y': screen_height/2}
mouse_impact = 0.2

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

class all_map():
    def __init__(self, objects):
        """ Конструктор класса all_map
        придает всем объектам нна карте класс all_map, чтобы их можно
        было все одновременно двигать, не двигая персоннажа
        Args:
        objects - объект класса all_map
        """
        self.objects = objects
        self.color = black

    def render(self):
        screen.fill(white)
        for object in self.objects:
            object.draw()

    def forward(self, axis_x, axis_y):
        #функция движения всей карты вперед
        t = True
        for object in self.objects:
            t = t and not (object.x + object.width >= hero.x and object.x <= hero.x and object.y + object.height * 0.4 >= hero.y and object.y <= hero.y + 9)
        for object in self.objects:
            if t:
                if axis_y == 1:
                    object.y -= hero_velocity / FPS / (2**0.5)
                else:
                    object.y -= hero_velocity / FPS
            else:
                pass

    def backward(self, axis_x, axis_y):
        #функция движения всей карты вниз
        t = True
        for object in self.objects:
            t = t and not (object.x + object.width >= hero.x and object.x  <= hero.x and object.y+ object.height >= hero.y - 9 and object.y + object.height * 0.6 <= hero.y)
        for object in self.objects:
            if t:
                if axis_y == 1:
                    object.y += hero_velocity / FPS / (2**0.5)
                else:
                    object.y += hero_velocity / FPS
            else:
                pass

    def left(self, axis_x, axis_y):
        #функция движения всей карты влево
        t = True
        for object in self.objects:
            t = t and not (object.x <= hero.x + 9 and object.x + object.width * 0.4 >= hero.x and object.y <= hero.y and object.y  + object.height >= hero.y)
        for object in self.objects:
            if t:
                if axis_x == 1:
                    object.x -= hero_velocity / FPS / (2**0.5)
                else:
                    object.x -= hero_velocity / FPS
            else:
                pass

    def right(self, axis_x, axis_y):
        #функция движения всей карты вправо
        t = True
        for object in self.objects:
            t = t and not (object.x+ object.width * 0.6 <= hero.x and object.x  + object.width >= hero.x - 9 and object.y <= hero.y and object.y  + object.height >= hero.y)
        for object in self.objects:
            if t:
                if axis_x == 1:
                    object.x += hero_velocity / FPS / (2**0.5)
                else:
                    object.x += hero_velocity / FPS
            else:
                pass


class Wall():
    def __init__(self, x, y, width, height):
        """ Конструктор класса wall
        Args:
        x - положение стены по горизонтали
        y - положение стены по вертикали
        width - длина
        height - высота
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = black

    def draw(self):
        #функция рисования стены на карте
        pygame.draw.rect(screen, black, (self.x - mouse_pos['x'] * mouse_impact, self.y - mouse_pos['y'] * mouse_impact, self.width, self.height))


class Hero():
    def __init__(self):
        """ Конструктор класса hero
        """
        self.color = black
        self.x = screen_width/2
        self.y = screen_height/2

    def draw(self):
        #функция рисования героя на карте
        pygame.draw.rect(screen, black, (self.x*(1 + mouse_impact) - mouse_pos['x'] * mouse_impact - hero_size['x'] / 2, self.y*(1 + mouse_impact) -  hero_size['y'] / 2 - mouse_pos['y'] * mouse_impact, 10, 10))



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
        screen.blit(self.img, (self.x - mouse_pos['x'] * mouse_impact, self.y - mouse_pos['y'] * mouse_impact))

hero = Hero()
walls = [Wall(200, 200, 600, 16), Wall(200, 200, 16, 200), Wall(200, 400, 200, 16), Wall(800, 200, 16, 200), Wall(440, 400, 376, 16)]
mymap = all_map(walls)
bullets = []

pygame.display.update()
clock = pygame.time.Clock()

flag = {'forward': 0, 'backward': 0, 'left': 0, 'right': 0, 'space' : 0}
scripts = {'forward': mymap.forward, 'backward': mymap.backward, 'left': mymap.left, 'right': mymap.right}
buttons = {'forward': pygame.K_s, 'backward': pygame.K_w, 'left': pygame.K_d, 'right': pygame.K_a, 'space': pygame.K_SPACE,}
axis = {'Ox': 0, 'Oy': 0}



while 1:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            for key in buttons:
                if event.key == buttons[key]:
                    flag[key] = 1
                    if (flag['left'] == 1 or flag['right'] == 1) and flag['left'] != flag['right']:
                        axis['Oy'] = 1
                    if (flag['forward'] == 1 or flag['backward'] == 1) and flag['forward'] != flag['backward']:
                        axis['Ox'] = 1


        if event.type == pygame.MOUSEMOTION:
            mouse_pos['x'], mouse_pos['y'] = event.pos

        if event.type == pygame.KEYUP:
            for key in buttons:
                if event.key == buttons[key]:
                    flag[key] = 0
                    if (flag['left'] != 1 and flag['right'] != 1) or flag['left'] == flag['right']:
                        axis['Oy'] = 0
                    if (flag['forward'] != 1 and flag['backward'] != 1) or flag['forward'] == flag['backward']:
                        axis['Ox'] = 0


    for key in flag:
        if flag[key] and (key == 'forward' or key == 'backward' or key == 'right' or key == 'left'):
            scripts[key](axis['Ox'], axis['Oy'])

    if flag['space'] == 1:
        angle = math.atan ((mouse_pos['y'] - hero.y) / (mouse_pos['x'] - hero.x))
        sin = (mouse_pos['x'] - hero.x) / math.sqrt( (mouse_pos['x'] - hero.x) ** 2 + (mouse_pos['y'] - hero.y) ** 2 )
        cos = (mouse_pos['y'] - hero.y) / math.sqrt( (mouse_pos['x'] - hero.x) ** 2 + (mouse_pos['y'] - hero.y) ** 2 )
        bullets.append(Bullet(hero.x*(1 + mouse_impact) - mouse_pos['x'] * mouse_impact - hero_size['x'] / 2, hero.y*(1 + mouse_impact) -  hero_size['y'] / 2 - mouse_pos['y'] * mouse_impact, cos, sin, angle, random.choice(["red", "yellow", "blue", "green"])))



    mymap.render()
    hero.draw()
    for bullet in bullets:
        bullet.move()
        bullet.draw()
    pygame.display.update()
