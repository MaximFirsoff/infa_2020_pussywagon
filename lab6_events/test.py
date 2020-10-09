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
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.update()
clock = pygame.time.Clock()
finished = False
balls = []
time = -dt
score = 0
missed = 0
bomb_0 = pygame.image.load('bomb.png')

while not finished:
    clock.tick(FPS)
    time += dt
    bomb = pygame.transform.scale(bomb_0, (time * 10, time * 10))
    screen.blit(bomb, (screen_width / 2 - time * 5, screen_height / 2 - time * 5))
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()

pygame.quit()
