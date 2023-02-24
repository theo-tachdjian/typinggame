import random

import pygame


class LandObject:

    def __init__(self):
        self.land = pygame.image.load("design/land.png")
        self.land = pygame.transform.scale(self.land, (self.land.get_width()*2, self.land.get_height()*2))
        self.assets = [
            pygame.image.load("design/bush.png"),
            pygame.image.load("design/bush_big.png"),
            pygame.image.load("design/bush_leaves.png"),
            pygame.image.load("design/tree.png"),
            pygame.image.load("design/tree_big.png")
        ]
        self.assets_order = [0, 1, 2, 3, 4]
        random.shuffle(self.assets_order)

    def render(self, surface: pygame.Surface, world_x):
        offset_x = world_x % self.land.get_width()
        y = surface.get_height()-self.land.get_height()
        for i in range(3):
            surface.blit(self.land, (-offset_x + (self.land.get_width() * i), y))
        for i in range(len(self.assets_order)):
            asset = self.assets[self.assets_order[i]]
            asset = pygame.transform.scale(asset, (asset.get_width()*2, asset.get_height()*2))
            for j in range(3):
                surface.blit(asset, (-(world_x % (surface.get_width()*3))+200 +(j*(surface.get_width() * 3)-(surface.get_width() * 3)) + i*550, surface.get_height()-asset.get_height()-self.land.get_height()))
