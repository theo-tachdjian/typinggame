import sys
import pygame
import json
import random
import time

from typping_game import words

WIDTH, HEIGHT = 800, 600
FPS = 30

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Typing Test')
pygame.init()


# background = pygame.image.load(trouverunbackgroundutilisable)
# background = pygame.transform.scale(background, (WIDTH,HEIGHT))

TITLE_COLOR = (249,231,159)
PROMPT_COLOR = (88,214,141)
RECT_COLOR =(133,193,233)
INPUT_COLOR=(93,173,226)
RESULT_COLOR=(236,112,99)

class User:
    def __init__(self):
        self.prompt = self.get_sentence()
        self.input = ''
        self.start_time=0
        self.time_taken=0
        self.timer_started=False
        self.end=False
        self.accuracy=0
        self.wpm=0
        self.result=''

    def get_sentence(self):
        data = words.liste_en_lane
        dat= random.choices(data, k=10)
        return ' '.join(dat)

def draw_text(surface, message, y_cord, font_size, color):
    font = pygame.font.Font(None, font_size)
    text = font.render(message,1,color)
    text_rect = text.get_rect(center=(WIDTH/2, y_cord))
    surface.blit(text, text_rect)

def draw_surface(surface):
    surface.fill((0,0,0))
    # surface.blit(background(0,0))
    draw_text(surface, 'League of Typing', 100, 60,TITLE_COLOR)
    if user.prompt:
        if len(user.prompt)>=60:
            lis=user.prompt.split()
            w1=' '.join(lis[:len(lis)//2])
            w2=' '.join(lis[len(lis)//2:])
            draw_text(surface,w1,200,20, PROMPT_COLOR)
            draw_text(surface, w2, 240, 20, PROMPT_COLOR)
    surface.fill((0,0,0),(50,300,700,80))
    pygame.draw.rect(surface,RECT_COLOR,(50,300,700,80),2)
    if user.input:
        if len(user.input)>=45:
            lis = user.input.split()
            w1 = ' '.join(lis[:len(lis) // 2])
            w2 = ' '.join(lis[len(lis) // 2:])
            draw_text(surface, w1, 325, 17, INPUT_COLOR)
            draw_text(surface, w2, 355, 17, INPUT_COLOR)
        else:
            draw_text(surface,user.input, 325,17, INPUT_COLOR)
    if user.end:
        draw_text(surface,user.result,500,22,RESULT_COLOR)
    pygame.display.update()

def reset_game():
    user.start_time, user.time_taken=0,0
    user.timer_started, user.end= False, False
    user.prompt, user.input= user.get_sentence(),''
    user.accuracy, user.wpm=0,0
    user.result=''

def show_result():
    if user.timer_started and not user.end:
        user.timer_taken = time.time()-user.start_time

        count = 0
        for i, c in enumerate(user.prompt):
            try:
                if user.input[i]==c:
                    count+=1
            except:
                pass

        user.accuracy = count/len(user.prompt)*100
        user.wpm = len(user.input)*60/(5*user.timer_taken)
        user.end=True
        user.result = f'Time : {round(user.time_taken)} || Accuracy : {round(user.accuracy)} || WPM : {round(user.wpm)}'
        print(user.result)

running = True
clock = pygame.time.Clock()
user=User()
while running:
    clock.tick(FPS)
    draw_surface(WIN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            if not user.timer_started:
                user.start_time = time.time()
                user.timer_started = True
            x,y = pygame.mouse.get_pos()
            if user.end:
                reset_game()
        elif event.type == pygame.KEYDOWN:
            if user.timer_started and not user.end:
                if event.key==pygame.K_RETURN:
                    show_result()
                elif event.key == pygame.K_BACKSPACE:
                    user.input=user.input[-1]
                else:
                    try:
                        user.input+=event.unicode
                    except:
                        pass
            if not user.timer_started and not user.end:
                user.start_time = time.time()
                user.timer_started= True
                try:
                    user.input+= event.unicode
                except:
                    pass
    pygame.display.update()