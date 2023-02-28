import pygame as pg
from pygame import image, Surface, transform
from random import choice, randint
from os import path
from settings import *
from sprites import *

class Game:

    def __init__(self):

        # init
        pg.init()
        pg.mixer.init()

        # window setup
        self.WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
        self.BACKGROUND = pg.Surface(WINDOW_RESOLUTION)
        pg.display.set_caption("FRUIT FRENZY")

        # load images
        self.load_all_imgs()

        # start running
        self.running = True

        # start screen
        self.splash_screen()

    def load_all_imgs(self):

        def load(fl_name, size = (LANE_WIDTH*FRUIT_SIZE, LANE_WIDTH*FRUIT_SIZE)):
            global IMG_DIR
            fruit_img = image.load(path.join(IMG_DIR, fl_name))
            fruit_surf = Surface.convert_alpha(fruit_img)
            fruit = transform.scale(fruit_surf, size)
            return fruit

        self.LEMON = load("orb5.png")
        self.COCONUT = load("orb6.png")
        self.BANANA = load("orb1.png")
        self.ORANGE = load("orb6.png")
        self.PINEAPPLE = load("orb1.png")

        # different [fruit sprite images, and their speed]
        self.FRUIT_TYPES = list(zip([self.PINEAPPLE, self.COCONUT, self.BANANA, self.ORANGE, self.LEMON], [i[1] for i in FRUIT_SPEEDS]))
        

    def launch_game(self):
        
        # blit background
        self.WINDOW.blit(self.BACKGROUND, (0, 0))

        # Draw Lines
        for i in range(LANES + 1):
            pg.draw.line(self.WINDOW, WHITE, (i*LANE_WIDTH + LEFT_MARGIN, 0), (i*LANE_WIDTH + LEFT_MARGIN, 350), 4)

        # track which lanes are occupied
        self.lanes_occupied = [False for i in range(LANES)]

        # set clock
        self.clock = pg.time.Clock()

    def main_loop(self):
        
        self.playing = True
        while self.playing:
            self.clock.tick(FRAME_RATE)
            self.update()
            self.events()
            self.draw()
            pg.display.flip()

    def splash_screen(self, score=None):
        pass
    
    def update(self):
        self.WINDOW.blit(self.BACKGROUND, (0, 0))
        all_sprites.update()

    def events(self):
        for event in pg.event.get():

            # check for quit
            if event.type == pg.QUIT:
                self.running = False
                if self.playing:
                    self.playing = False
        
        # spawn fruits
        if not randint(0, FRUIT_SPAWN_RATE) and len([i for i in self.lanes_occupied if not i]) > 0:
            fruit = Fruit(self.WINDOW, self.FRUIT_TYPES, [i[1] for i in zip(self.lanes_occupied, range(LANES)) if not i[0]])
            self.lanes_occupied[fruit.lane] = True

        # despawn fruits
        for fruit in fruit_sprites:
            if fruit.rect.top > HEIGHT:
                self.lanes_occupied[fruit.lane] = False
                fruit.kill()

    def draw(self):
        for i in range(LANES + 1):
            pg.draw.line(self.WINDOW, WHITE, (i*LANE_WIDTH + LEFT_MARGIN, 0), (i*LANE_WIDTH + LEFT_MARGIN, 350), 4)

