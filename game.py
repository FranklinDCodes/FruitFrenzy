# imports
import pygame as pg
from pygame import image, Surface, transform
from random import choice, randint
from os import path

# Init pygame
pg.init()

# CONSTANTS
# game
FRAME_RATE = 60
WINDOW_RESOLUTION = (850, 500)

# Create window
GAME_WINDOW = pg.display.set_mode(WINDOW_RESOLUTION)
pg.display.set_caption("Fruit Frenzy!")
BACKGROUND = pg.Surface(WINDOW_RESOLUTION)
GAME_WINDOW.blit(BACKGROUND, (0, 0))

# layout
LANE_WIDTH = 80
FRUIT_SIZE = .5
LEFT_MARGIN = 225
LANES = 7

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 30)

# directories
IMG_DIR = path.join(path.dirname(__file__), "Imgs")

# fruits
FRUIT_SPAWN_RATE = 50
def load_img(fl_name, size = (LANE_WIDTH*FRUIT_SIZE, LANE_WIDTH*FRUIT_SIZE)):
    global IMG_DIR
    fruit_img = image.load(path.join(IMG_DIR, fl_name))
    fruit_surf = Surface.convert_alpha(fruit_img)
    fruit = transform.scale(fruit_surf, size)
    return fruit

LEMON = load_img("orb5.png")
COCONUT = load_img("orb6.png")
BANANA = load_img("orb1.png")
#ORANGE = None
#PINEAPPLE = None

# different fruit sprites and their speed
fruit_types = [
    #[PINEAPPLE, 4],
    [COCONUT, 2],
    [BANANA, 1],
    #[ORANGE, 1],
    [LEMON, 1]
    ]

# SPRITES
class Fruit(pg.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        fruit_sprites.add(self)
        fruit = choice(fruit_types)
        self.lane = randint(1, LANES)
        self.image = fruit[0]
        self.rect = self.image.get_rect(center=(self.lane*LANE_WIDTH + LANE_WIDTH/2 + LEFT_MARGIN, -10))
        self.speed = fruit[1]
        
    def update(self):
        GAME_WINDOW.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        self.rect.y += self.speed
        GAME_WINDOW.blit(self.image, (self.rect.x, self.rect.y))

# LEVELS
class Level(object):

    def __init__(self, name, spawn_rate, fruits):
        self.name = name
        self.spawn_rate = spawn_rate
        self.fruits = fruits

    def update(self):
        pass

"""# test
for i in range(1000):
    lane = choice(range(7, 14))
    pg.draw.circle(BACKGROUND, RED, (lane*50 + 25, 10), 5)"""

# Draw Line
for i in range(LANES + 1):
    pg.draw.line(GAME_WINDOW, WHITE, (i*LANE_WIDTH + LEFT_MARGIN, 0), (i*LANE_WIDTH + LEFT_MARGIN, 350), 4)

# sprites
fruit_sprites = pg.sprite.Group()

# --------------------------------------------------
# Start Main Game Loop
game_running = True
program_running = True
clock = pg.time.Clock()

while game_running:

    # Check for events
    for event in pg.event.get():

        # Exit loop if quit
        if event.type == pg.QUIT:
            game_running = False
            program_running = False
    
    if not randint(0, FRUIT_SPAWN_RATE):
        Fruit()
        
    fruit_sprites.update()

    pg.display.update()

    clock.tick(FRAME_RATE)
