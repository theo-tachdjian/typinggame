import sys
import pygame
import json
import random
import time

import text
import words
from land_object import LandObject
from enemy_wave import *

WIDTH, HEIGHT = 800, 600
FPS = 30

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('League of Typing')
pygame.display.set_icon(pygame.image.load("design/icon.png"))
pygame.init()

TITLE_COLOR = (249, 231, 159)
PROMPT_COLOR = (88, 214, 141)
RECT_COLOR = (133, 193, 233)
INPUT_COLOR = (93, 173, 226)
RESULT_COLOR = (236, 112, 99)


class User:
    def __init__(self, word_count=4):
        self.word_count = word_count
        self.prompt = self.get_sentence()
        self.input = ''
        self.start_time = 0
        self.timer_started = False
        self.end = False
        self.accuracy = 0
        self.wpm = 0
        self.result = ''

    def get_sentence(self):
        data = words.liste_en_lane
        dat = random.choices(data, k=self.word_count)
        return ' '.join(dat)


def draw_background(surface):
    surface.fill((90, 90, 255))
    land.render(surface, world_x)
    # draw_text(surface, 'League of Typing', 100, 60, TITLE_COLOR)


def draw_text_overlay(surface):
    lis = user.prompt.split()  # convert words as a list
    w1 = ' '.join(lis[:len(lis) // 2])
    w2 = ' '.join(lis[len(lis) // 2:])
    text.draw_aligned_text(w1, surface.get_width()/2, 200, surface, text.get_font(16))
    text.draw_aligned_text(w2, surface.get_width()/2, 240, surface, text.get_font(16))
    surface.fill((0, 0, 0), (50, 300, 700, 80))
    pygame.draw.rect(surface, RECT_COLOR, (50, 300, 700, 80), 2)
    if user.input:
        if len(user.input) >= 45:
            lis = user.input.split()
            w1 = ' '.join(lis[:len(lis) // 2])
            w2 = ' '.join(lis[len(lis) // 2:])
            text.draw_aligned_text(w1, WIN.get_width() / 2, 320, WIN, text.get_font(12), INPUT_COLOR)
            text.draw_aligned_text(w2, WIN.get_width() / 2, 350, WIN, text.get_font(12), INPUT_COLOR)
        else:
            text.draw_aligned_text(user.input, WIN.get_width() / 2, 320, WIN, text.get_font(12), INPUT_COLOR)


def reset_game():
    user.start_time, user.time_taken = 0, 0
    user.timer_started, user.end = False, False
    user.prompt, user.input = user.get_sentence(), ''
    user.accuracy, user.wpm = 0, 0
    user.result = ''


def defeat_wave():
    global finished_time
    if user.timer_started and not user.end:
        user.timer_taken = time.time() - user.start_time

        count = 0
        for i, c in enumerate(user.prompt):
            try:
                if user.input[i] == c:
                    count += 1
            except:
                pass

        user.accuracy = count / len(user.prompt) * 100
        if user.timer_taken != 0:
            user.wpm = len(user.input) * 60 / (5 * user.timer_taken)
        else:
            user.wpm = len(user.input) * 60 / 5
        user.end = True
        user.result = f'Time : {round(time.time()-user.start_time)} || Accuracy : {round(user.accuracy)} || WPM : {round(user.wpm)}'
        print(user.result)
        finished_time = time.time()


running = True
clock = pygame.time.Clock()

land = LandObject()
world_x = 0

enemy_wave = EnemyWave()
enemy_wave_cout = 1
enemy_wave_pos_x = 700
MAX_NEXT_WAVE_POS_X = 912
MIN_NEXT_WAVE_POS_X = 712

finished_time = 0
TB_NEXT_WAVE = 2.0
PLAYER_POS_X = 64
player_health = 5
HEART_IMG = pygame.image.load("design/heart.png")
HEART_IMG = pygame.transform.scale(HEART_IMG, (30, 30))
HEART_EMPTY_IMG = pygame.image.load("design/heart_empty.png")
HEART_EMPTY_IMG = pygame.transform.scale(HEART_EMPTY_IMG, (30, 30))

score = 0

user = User(len(enemy_wave.enemies)*2)


def is_wave_in_range():
    return enemy_wave_pos_x-world_x <= PLAYER_POS_X+208


while running:
    clock.tick(FPS)

    draw_background(WIN)
    enemy_wave.render(WIN, enemy_wave_pos_x, world_x)
    for i in range(player_health):
        WIN.blit(HEART_IMG, (8+i*32, 16))
    for i in range(5-player_health):
        WIN.blit(HEART_EMPTY_IMG, (8 + (4 * 32)-(i*32), 16))
    text.draw_text("Score: "+str(score), 16, 56, WIN, text.get_font(16))

    if is_wave_in_range():
        if not user.timer_started:
            user.start_time = time.time()
            user.timer_started = True

        if user.end:
            if user.end:
                text.draw_aligned_text(user.result, WIN.get_width() / 2, 548, WIN, text.get_font(20))
            if time.time() > TB_NEXT_WAVE + finished_time:
                # spawn next wave
                enemy_wave_cout += 1
                score += enemy_wave.get_points()
                # spawn Tower every 5 turns
                if enemy_wave_cout % 5 == 0:
                    enemy_wave = TowerWave()
                else:
                    enemy_wave = EnemyWave()

                enemy_wave_pos_x += random.randint(MIN_NEXT_WAVE_POS_X, MAX_NEXT_WAVE_POS_X)
                if type(enemy_wave) == TowerWave:
                    user = User(10)
                else:
                    user = User(len(enemy_wave.enemies)*2)
        else:
            draw_text_overlay(WIN)
    else:
        # if not in range of wave, go forward
        world_x += 6

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if is_wave_in_range():
            if event.type == pygame.KEYDOWN:
                if user.timer_started and not user.end:
                    if event.key == pygame.K_RETURN:
                        defeat_wave()
                    elif event.key == pygame.K_BACKSPACE:
                        user.input = user.input[:-1]
                    else:
                        try:
                            user.input += event.unicode
                        except:
                            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # debug
                world_x += 50
            elif event.key == pygame.K_LEFT:
                # debug
                world_x -= 50

    pygame.display.update()
