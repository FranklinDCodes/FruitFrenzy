import pygame as pg
from random import choice
from settings import *

# sprite groups
fruit_sprites = pg.sprite.Group()
fruit_hitboxes = pg.sprite.Group()
all_buttons = []


# SPRITES
class Fruit(pg.sprite.Sprite):
    
    def __init__(self, window, fruit_types, availible_lanes):
        super().__init__()
        fruit_sprites.add(self)
        fruit = choice(fruit_types)
        self.lane = choice(availible_lanes)
        self.image = fruit[0]
        self.rect = self.image.get_rect(center=((self.lane*LANE_WIDTH + LANE_WIDTH/2 + LEFT_MARGIN), -10))
        self.speed = fruit[1]
        self.GAME_WINDOW = window

        # how much the rect should be ajusted fruit: (+x, +y, +width, +height)
        rect_ajust_fruits = {"WATERMELON": (0, 0, 5, 2),
                      "PINEAPPLE": (9, 11, -1, -1),
                      "COCONUT": (0, 0, -5, -5),
                      "BANANA": (-2, -2, -2, -2)}
        x, y, w, h = rect_ajust_fruits[fruit[2]]
        hit_rect = pg.Rect((self.lane*LANE_WIDTH + LANE_WIDTH/2 + LEFT_MARGIN), -10, self.rect.width/2 + w, self.rect.height/2 + h)
        hit_rect_location = list(self.rect.center)
        hit_rect_location[0] += x
        hit_rect_location[1] += y
        hit_rect.center = hit_rect_location
        self.hitbox = HitBox(self, hit_rect, window)
        fruit_hitboxes.add(self.hitbox)
        
    def update(self):
        self.rect.y += self.speed
        self.hitbox.rect.y += self.speed
        self.GAME_WINDOW.blit(self.image, (self.rect.x, self.rect.y))
        self.hitbox.update()

class Player(pg.sprite.Sprite):

    def __init__(self, window, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(CENTER_LANE*LANE_WIDTH + LEFT_MARGIN + -LANE_WIDTH/2, PLAYER_Y))
        self.GAME_WINDOW = window
        #hit_x = (round(LANES/2)*LANE_WIDTH + LEFT_MARGIN + -LANE_WIDTH/2 + -PLAYER_WIDTH/2 + (PLAYER_WIDTH - HITBOX_SIZE_MED[0])/2) + 3
        hit_rect = pg.Rect(0, 0, HITBOX_SIZE_1[0], HITBOX_SIZE_1[1])
        hit_rect.bottom = HITBOX_YS[HITBOX_SIZE_1]
        hit_rect.center = (self.rect.center[0] + HITBOX_X_ADD, hit_rect.center[1])
        self.hitbox = HitBox(self, hit_rect, window)
        
    def update(self):
        self.GAME_WINDOW.blit(self.image, (self.rect.x, self.rect.y))
        self.hitbox.update()

class HitBox(pg.sprite.Sprite):

    def __init__(self, super_sprite, rect, window):
        super().__init__()
        self.super_sprite = super_sprite
        self.rect = rect
        self.window = window

    def update(self):
        #pg.draw.rect(self.window, RED, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        pass

# OTHER CLASSES
class Button():

    def __init__(self, window, rect_value, color, label_txt, label_font, label_color, command, id, is_active=False, add_to_all_buttons=True):
        if add_to_all_buttons:
            all_buttons.append(self)
        self.rect_value = rect_value
        self.color = color
        self.title = label_txt
        self.title_font = label_font
        self.title_color = label_color
        self.command = command
        self.window = window
        self.id = id
        self.is_active = is_active
        
    def draw(self, is_active):
        if is_active:
            color = self.color
        else:
            color = BLUEGREY
        button = pg.draw.rect(self.window, color, self.rect_value, 0, 5)
        txt = self.title_font.render(self.title, True, self.title_color)
        size_rect = txt.get_rect()
        size_rect.center = button.center
        self.window.blit(txt, size_rect.topleft)
    
    def was_clicked(self, mouse_coords):
        
        # greater than x, but less than x + width
        x_bool = mouse_coords[0] >= self.rect_value[0] and mouse_coords[0] <= self.rect_value[0] + self.rect_value[2]

        # greater than y, but less than y + height
        
        y_bool = mouse_coords[1] >= self.rect_value[1] and mouse_coords[1] <= self.rect_value[1] + self.rect_value[3]

        if self.is_active:
            return x_bool and y_bool
        else:
            return False
    
    def kill(self):
        ind = 0
        for i in all_buttons:
            if i == self:
                break
            ind += 1
        all_buttons.pop(ind)


        

