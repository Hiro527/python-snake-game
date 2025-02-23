import pygame
from pygame.locals import *

from random import randint

from time import sleep

import sys

# 定数

FPS = 10
FRAME_TIME = 1.0 / FPS

SPEED = 1

WORLD_SIZE = 15
CELL_SIZE = 40

WIDTH = WORLD_SIZE * CELL_SIZE
HEIGHT = WORLD_SIZE * CELL_SIZE + 50

EMPTY = 0
SNAKE = 1
APPLE = 2

STOP = -1
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

DEFAULT_WORLD = [[EMPTY for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]

DEFAULT_SNAKE_POS = (2, 2)

DEFAULT_WORLD[DEFAULT_SNAKE_POS[1]][DEFAULT_SNAKE_POS[0]] = SNAKE

# 関数


def get_random_empty_cell(world):
    x = randint(0, WORLD_SIZE - 1)
    y = randint(0, WORLD_SIZE - 1)

    while world[y][x] != EMPTY:
        x = randint(0, WORLD_SIZE - 1)
        y = randint(0, WORLD_SIZE - 1)

    return x, y


def update_world(world, x, y, value):
    world[y][x] = value
    return world


def is_done(length):
    return length == WORLD_SIZE ** 2


def main():
    pygame.init()

    world = DEFAULT_WORLD.copy()

    frame_count = 0

    pausing = True

    game_over = False

    score = 0
    length = 1
    sound = 0

    head_pos = (5, 5)
    history = [head_pos]

    food_pos = get_random_empty_cell(world)
    world = update_world(world, food_pos[0], food_pos[1], APPLE)

    direction = STOP

    font_file = open('./fonts/PressStart2P-vaV7.ttf', 'rb')
    font_title = pygame.font.Font(font_file, 30)
    font_subtitle = pygame.font.Font(font_file, 15)
    font_score = pygame.font.Font(font_file, 20)

    sound_move = [pygame.mixer.Sound('./music/music_move_1.mp3'), pygame.mixer.Sound('./music/music_move_2.mp3'),
                  pygame.mixer.Sound('./music/music_move_3.mp3'), pygame.mixer.Sound('./music/music_move_4.mp3')]
    sound_eat = pygame.mixer.Sound('./music/music_food.mp3')
    sound_gameover = pygame.mixer.Sound('./music/music_gameover.mp3')

    scr = pygame.display.set_mode(
        (WORLD_SIZE * CELL_SIZE, WORLD_SIZE * CELL_SIZE + 50))
    pygame.display.set_caption('SNAKE GAME')

    while True:
        frame_count += 1

        world = [[EMPTY for _ in range(WORLD_SIZE)]
                 for _ in range(WORLD_SIZE)]

        old_direction = direction

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                pausing = False

                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if game_over:
                    world = DEFAULT_WORLD.copy()
                    frame_count = 0
                    pausing = True
                    game_over = False
                    score = 0
                    length = 1
                    sound = 0
                    head_pos = (5, 5)
                    history = [head_pos]
                    direction = STOP
                    food_pos = get_random_empty_cell(world)
                    world = update_world(
                        world, food_pos[0], food_pos[1], APPLE)
                    direction = RIGHT

                if event.key == K_w or event.key == K_UP:
                    direction = UP if (
                        direction != DOWN or length == 1) else direction
                elif event.key == K_s or event.key == K_DOWN:
                    direction = DOWN if (
                        direction != UP or length == 1) else direction
                elif event.key == K_a or event.key == K_LEFT:
                    direction = LEFT if (
                        direction != RIGHT or length == 1) else direction
                elif event.key == K_d or event.key == K_RIGHT:
                    direction = RIGHT if (
                        direction != LEFT or length == 1) else direction

        if old_direction != direction:
            sound_move[sound].play()
            sound = (sound + 1) % 4

        if not pausing and not game_over:
            if direction == UP:
                head_pos = (head_pos[0], max(head_pos[1] - SPEED, 0))
            elif direction == DOWN:
                head_pos = (head_pos[0], min(
                    head_pos[1] + SPEED, WORLD_SIZE - 1))
            elif direction == LEFT:
                head_pos = (max(head_pos[0] - SPEED, 0), head_pos[1])
            elif direction == RIGHT:
                head_pos = (min(head_pos[0] + SPEED,
                            WORLD_SIZE - 1), head_pos[1])
            else:
                pass

            if head_pos in history:
                game_over = True
                sound_gameover.play()

            history.append(head_pos)

            length = score + 1

        for idx, pos in enumerate(reversed(history)):
            if idx >= length:
                break

            world = update_world(world, pos[0], pos[1], SNAKE)

        if len(history) > length:
            history = history[-length:]

        if head_pos == food_pos:
            score += 1
            food_pos = get_random_empty_cell(world)
            sound_eat.play()

        world = update_world(world, food_pos[0], food_pos[1], APPLE)

        for y, row in enumerate(world):
            for x, cell in enumerate(row):
                color = (170, 215, 81) if (x + y) % 2 == 0 else (162, 209, 73)
                if cell == APPLE:
                    color = (231, 71, 29)
                elif cell == SNAKE:
                    color = (79, 120, 248)

                scr.fill(color, Rect(x * CELL_SIZE, y *
                         CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))

        if pausing and frame_count % 10 < 5:
            text = font_title.render('PRESS ANY KEY', False, (255, 255, 255))
            text_rect = text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2))
            scr.blit(text, text_rect)

        if game_over:
            text_gameover = font_title.render(
                'GAME OVER'.format(score), False, (255, 255, 255))
            text_gameover_rect = text_gameover.get_rect(
                center=(WIDTH // 2, (HEIGHT) // 2))
            text_replay = font_subtitle.render(
                'PRESS ANY KEY TO REPLAY', False, (255, 255, 255))
            text_replay_rect = text_replay.get_rect(
                center=(WIDTH // 2, (HEIGHT) // 2 + 30))

            scr.blit(text_gameover, text_gameover_rect)
            scr.blit(text_replay, text_replay_rect)

        scr.fill((87, 138, 52), Rect(0, 0, WIDTH, 50))

        score_text = font_score.render(
            'SCORE: {}'.format(score), False, (255, 255, 255))
        scr.blit(score_text, (15, 15))

        pygame.display.update()

        sleep(FRAME_TIME)


if __name__ == '__main__':
    main()
