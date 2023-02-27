import random

import pygame


CREEP_MAGE = pygame.image.load("design/creep_mage128.png")
CREEP_MELEE = pygame.image.load("design/creep_melee8bits128.png")
TOWER = pygame.image.load("design/tower.png")


class EnemyWave:

    def __init__(self):
        self.enemies: list[pygame.Surface] = []
        for i in range(random.randint(1, 4)):
            self.enemies.append(random.choice([CREEP_MAGE, CREEP_MELEE]))

        self.anim_ended = False

    def render(self, screen: pygame.Surface, pos_x, world_x):
        offset = ((4-len(self.enemies))*self.enemies[0].get_width())/2
        for i in range(len(self.enemies)):
            screen.blit(self.enemies[i], (pos_x-world_x + i*128 + offset, screen.get_height()-self.enemies[i].get_height()-96))

    def get_points(self):
        return len(self.enemies) * 10


class TowerWave(EnemyWave):

    def __init__(self):
        super().__init__()
        self.enemies = [TOWER]

    def render(self, screen: pygame.Surface, pos_x, world_x):
        for i in range(len(self.enemies)):
            screen.blit(self.enemies[i], (pos_x-world_x + i*128 + 64, screen.get_height()-self.enemies[i].get_height()-96))

    def get_points(self):
        return 65
