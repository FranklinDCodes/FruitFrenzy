import pygame as pg
from random import choice
from settings import *

# sprite groups
all_sprites = pg.sprite.Group()
fruit_sprites = pg.sprite.Group()


# SPRITES
class Fruit(pg.sprite.Sprite):
    
    def __init__(self, window, fruit_types, availible_lanes):
        super().__init__()
        fruit_sprites.add(self)
        all_sprites.add(self)
        fruit = choice(fruit_types)
        self.lane = choice(availible_lanes)
        self.image = fruit[0]
        self.rect = self.image.get_rect(center=(self.lane*LANE_WIDTH + LANE_WIDTH/2 + LEFT_MARGIN, -10))
        self.speed = fruit[1]
        self.GAME_WINDOW = window
        
    def update(self):
        self.rect.y += self.speed
        self.GAME_WINDOW.blit(self.image, (self.rect.x, self.rect.y))