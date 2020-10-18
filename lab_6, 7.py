import pygame
from pygame.draw import *
from random import randint
from math import pi, sin, cos
import csv
from time import asctime

pygame.init()

screen_width, screen_height = 1200, 600
FPS = 50
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
score = 0
number_ball = 3
number_rect = 3
radius = 55
rect_width, rect_height = 40, 25
lap = 2.5


def parameters(n, v=3):
    param = []
    for i in range(n):
        angle = randint(0, int(2 * pi * 100))
        param.append({
            'x': randint(100, screen_width - 100),
            'y': randint(100, screen_height - 100),
            'vx': v * cos(angle / 100),
            'vy': v * sin(angle / 100),
            'r': randint(40, 255),
            'g': randint(40, 255),
            'b': randint(40, 255)
        })
    return param


def balls_movement():
    for item in balls:
        ellipse(screen, (item['r'], item['g'], item['b']),
                (item['x'] - radius, item['y'] - radius, 2 * radius, 2 * radius))
        item['x'] += item['vx']
        item['y'] += item['vy']





def ricochet(param, w, h):
    for item in param:
        if item['x'] - w <= 0:
            item['vx'] = abs(item['vx'])
        if item['y'] - h <= 0:
            item['vy'] = abs(item['vy'])
        if item['x'] + w >= screen_width:
            item['vx'] = -abs(item['vx'])
        if item['y'] + h >= screen_height:
            item['vy'] = -abs(item['vy'])


def show_score():
    """Draws player's score in top left corner of the screen"""
    font = pygame.font.SysFont('arial', 25, True)
    text_1 = font.render("Score : {}".format(score), True, WHITE)
    screen.blit(text_1, (0, 0))


def dialog():
    screen.fill(BLACK)
    font = pygame.font.SysFont('arial', 32, True)
    text_1 = font.render("Your score is {}".format(score), True, WHITE)
    text_2 = font.render("Please enter your name and press F1", True, WHITE)
    screen.blit(text_1, text_1.get_rect(center=(screen_width / 2, screen_height / 3)))
    screen.blit(text_2, text_2.get_rect(center=(screen_width / 2, screen_height * 2 / 3)))


def user_text():
    global user_name, finished
    font = pygame.font.SysFont('arial', 32, True)
    text_1 = font.render(user_name, True, WHITE)
    screen.blit(text_1, text_1.get_rect(center=(screen_width / 2, screen_height / 2)))
    pygame.display.update()
    for events in pygame.event.get():
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_BACKSPACE:
                user_name = user_name[:-1]
            elif events.key == pygame.K_ESCAPE:
                finished = True
            elif events.key == pygame.K_F1:
                if user_name != "":
                    with open('Best scores.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow([user_name, score, asctime()])
                finished = True
            else:
                user_name += events.unicode


def click():
    global score
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for item in balls:
        if (mouse_x - item['x']) ** 2 + (mouse_y - item['y']) ** 2 <= radius ** 2:
            score += 1
            item['x'], item['y'] = 2 * screen_width, 2 * screen_height
            item['vx'], item['vy'] = 0, 0
            print("score -", score)



def time(present_t, start_t):
    if present_t - start_t >= lap:
        start_t = present_t
    return start_t


clock = pygame.time.Clock()
finished = False
user_name = ""

while not finished:
    screen.fill(BLACK)
    clock.tick(FPS)
    balls = parameters(number_ball)
    start_time = time(pygame.time.get_ticks(), 0)
    present_time = 0
    while (present_time - start_time) / 1000 < lap:
        present_time = pygame.time.get_ticks()
        balls_movement()
        ricochet(balls, radius, radius)
        show_score()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                while not finished:
                    dialog()
                    user_text()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click()
        pygame.display.update()
        screen.fill(BLACK)

pygame.quit()
