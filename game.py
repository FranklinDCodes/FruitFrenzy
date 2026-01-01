import pygame as pg
from pygame import image, Surface, transform
from random import randint
from os import path
from sys import exit
from csv import reader, writer
from settings import *
from classes import *


class Game:

    def __init__(self):

        # init
        pg.init()
        pg.mixer.init()

        # window setup
        self.WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
        
        # load images
        self.load_media()

        # set icon
        pg.display.set_icon(self.PINEAPPLE)

        # set background
        self.BACKGROUND = self.BACKGROUND_IMG
        pg.display.set_caption("FRUIT FRENZY")

        # start music
        pg.mixer.music.load(path.join(SND_DIR, "game_song.wav"))
        pg.mixer.music.set_volume(.5)
        pg.mixer.music.play(-1)

    def load_media(self):

        def load(fl_name, size = (LANE_WIDTH*FRUIT_SIZE, LANE_WIDTH*FRUIT_SIZE)):
            global IMG_DIR
            fruit_img = image.load(path.join(IMG_DIR, fl_name))
            fruit_surf = Surface.convert_alpha(fruit_img)
            fruit = transform.scale(fruit_surf, size)
            return fruit
        
        #imgs
        self.COCONUT = load("Coconut.png")
        self.BANANA = load("Banana.png")
        self.WATERMELON = load("Watermelon.png")
        self.PINEAPPLE = load("Pineapple.png")
        self.PLAYER_IMG_1 = load("Guy_1.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_1_UP = load("Guy_1_Up.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_2 = load("Guy_2.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_2_UP = load("Guy_2_Up.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_3 = load("Guy_3.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_3_UP = load("Guy_3_Up.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_4 = load("Guy_4.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_4_UP = load("Guy_4_Up.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_5 = load("Guy_5.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_IMG_5_UP = load("Guy_5_Up.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.PLAYER_SIZES = ((self.PLAYER_IMG_1, self.PLAYER_IMG_1_UP), 
                             (self.PLAYER_IMG_2, self.PLAYER_IMG_2_UP), 
                             (self.PLAYER_IMG_3, self.PLAYER_IMG_3_UP),
                             (self.PLAYER_IMG_4, self.PLAYER_IMG_4_UP),
                             (self.PLAYER_IMG_5, self.PLAYER_IMG_5_UP))
        self.BACKGROUND_IMG = load("Background_0.png", WINDOW_RESOLUTION)
        self.LOGO = load('Logo.png', (8000/20, 4500/20))

        # snds
        self.miss_sound = pg.mixer.Sound(path.join(SND_DIR, "miss_sound.wav"))
        self.miss_sound.set_volume(.5)

        # different [fruit sprite images, and their speed]
        self.FRUIT_TYPES = list(zip([self.PINEAPPLE, self.COCONUT, self.BANANA, self.WATERMELON], [i[1] for i in FRUIT_SPEEDS], [i[0] for i in FRUIT_SPEEDS]))

        # Fonts
        self.MONEY_TEXT = pg.font.Font(LABEL_FONT, 24)
        self.LIVES_LABEL_TEXT = pg.font.Font(LABEL_FONT, 24)
        self.BUTTON_LABEL_TEXT = pg.font.Font(LABEL_FONT, 12)
        self.UPGRADE_PRICE_TEXT = pg.font.Font(LABEL_FONT, 18)
        self.SCORE_TEXT = pg.font.Font(SCORE_FONT, 48)
        self.SPLASH_TEXT = pg.font.Font(LABEL_FONT, 24)
        self.SPLASH_TEXT_BIG = pg.font.Font(LABEL_FONT, 36)
        self.INITIALS_TEXT = pg.font.Font(LABEL_FONT, 72)
        self.HIGH_SCORE_LABEL_TEXT = pg.font.Font(LABEL_FONT, 24)
        self.END_TEXT = pg.font.Font(LABEL_FONT, 120)

    def launch_game(self, prev_score=None):
        
        # running
        self.running = True

        # level
        self.level = 0
        self.in_level = True
        self.spawn_fruit = True
        self.fruit_spawned_count = 0

        # level settings
        self.level_length = 0
        self.fruit_spawn_rate = 0 #  The lower, the more spawn chance
        self.fruit_spawn_rate_minimum = 0 # the lower, the closer together the fruit are able to fall
        self.fruit_value = 0
        self.fruit_score= 0
        self.score_add_loop = 0
        self.MONEY_ADD_LOOP = 0
        self.level_completion_value = 0
        self.level_completion_score = 0

        # set clock
        self.clock = pg.time.Clock()

        # start screen
        self.splash_screen(prev_score)

        # blit background
        self.WINDOW.blit(self.BACKGROUND, (0, 0))

        # Blit player
        self.player = Player(self.WINDOW, self.PLAYER_IMG_1)

        # basket size (sm=0, med=1, lrg=2)
        self.size = 0

        # Player up images
        self.player_imgs = self.PLAYER_SIZES[self.size]

        # player speed level
        self.speed_level = 0

        # player status
        self.lives = 3
        self.score = 0
        self.money = 0

        # loop counter
        self.loop_counter = 0

        def upgrade_size():
            if self.size <= len(self.PLAYER_SIZES) - 1 and self.money >= BASKET_UPGRADES_PRICES[self.size]:
                self.money -= BASKET_UPGRADES_PRICES[self.size]
                self.size += 1
                self.player_imgs = self.PLAYER_SIZES[self.size]
                old_hitbox_rect = self.player.hitbox.rect
                new_size = HITBOX_SIZES[self.size]
                new_hitbox_rect = pg.Rect(0, 0, new_size[0], new_size[1])
                new_hitbox_rect.center = (old_hitbox_rect.center[0], new_hitbox_rect.center[1])
                new_hitbox_rect.bottom = HITBOX_YS[HITBOX_SIZES[self.size]]
                self.player.hitbox.rect = new_hitbox_rect
                self.player.image = self.player_imgs[0]
                
        def upgrade_speed():
            if self.speed_level <= 4 and self.money >= SPEED_UPGRADE_PRICES[self.speed_level]:
                    self.money -= SPEED_UPGRADE_PRICES[self.speed_level]
                    self.speed_level += 1

        # buttons
        self.bask_button = Button(self.WINDOW, (20, HEIGHT - 215, 70, 20), GREEN, "Upgrade", self.BUTTON_LABEL_TEXT, BLACK, upgrade_size, "bask")
        self.speed_button = Button(self.WINDOW, (20, HEIGHT - (215 + 100), 70, 20), GREEN, "Upgrade", self.BUTTON_LABEL_TEXT, BLACK, upgrade_speed, "speed")

        # track which lanes are occupied
        self.lanes_occupied = [False for i in range(LANES)]

        # time since last fruit spawn
        self.last_spawn = 0

        # is there a fruit waiting to spawn after minimum times is up
        self.spawn_in_queue = False

        self.level_setup()

        # draw elements
        self.draw()
    
    def reset_game(self):
        for i in fruit_sprites:
            i.kill()
        for i in fruit_hitboxes:
            i.kill()
        self.player.kill()

        end_surf = self.END_TEXT.render("Game Over", True, BLACK)
        self.WINDOW.blit(end_surf, (WIDTH/2 - end_surf.get_width()/2, HEIGHT/2 - end_surf.get_height()/2))

        pg.display.update()

        pg.time.wait(3000)

        try:

            with open(top_score_path, "r") as fl:
                highscores = list(reader(fl))

            if len(highscores) == 0:
                highscores = [[0, "---"] for i in range(5)]

        except FileNotFoundError:

            highscores = [[0, "---"] for i in range(5)]

        highscores = [[int(i[0]), i[1]] for i in highscores]
        highscores.sort(reverse=True)

        if self.score > highscores[-1][0]:
            
            highscores.append([self.score, None])
            highscores.sort(reverse=True)

            highscores = highscores[:5]

            new_high_scores = self.high_score_screen(self.score, highscores)

            with open(top_score_path, "w") as fl:
                w = writer(fl, lineterminator="\n")
                w.writerows(new_high_scores)

        self.launch_game(self.score)

    def main_loop(self):
        
        while self.running:
            self.clock.tick(FRAME_RATE)
            self.update()
            self.events()

            self.draw()
            self.loop_counter += 1
            pg.display.flip()

        pg.quit()
        exit(1)

    def splash_screen(self, score=None, win=False):
        
        if score == None:
            self.WINDOW.fill(BLUEGREY)
            self.WINDOW.blit(self.LOGO, (WIDTH/2 - self.LOGO.get_width()/2, (HEIGHT/2 - self.LOGO.get_height()/2) - 100))
            instruct_surface1 = self.SPLASH_TEXT.render("Use the arrows keys or A & D keys to move and catch the fruit,", True, WHITE)
            self.WINDOW.blit(instruct_surface1, (WIDTH/2 - instruct_surface1.get_width()/2, 280))
            instruct_surface2 = self.SPLASH_TEXT.render("but miss more than 3 fruit and you lose!", True, WHITE)
            self.WINDOW.blit(instruct_surface2, (WIDTH/2 - instruct_surface2.get_width()/2, 320))
            instruct_surface3 = self.SPLASH_TEXT.render("Press ENTER to start", True, WHITE)
            self.WINDOW.blit(instruct_surface3, (WIDTH/2 - instruct_surface3.get_width()/2, 400))
            pg.display.update()

            splash = True
            while splash:

                self.clock.tick(FRAME_RATE)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                        splash = False
                        break
                
                    if event.type == pg.KEYUP and event.key == pg.K_RETURN:
                        splash = False

        else:
            self.WINDOW.fill(BLUEGREY)
            self.WINDOW.blit(self.LOGO, (WIDTH/2 - self.LOGO.get_width()/2, (HEIGHT/2 - self.LOGO.get_height()/2) - 100))
            instruct_surface1 = self.SCORE_TEXT.render(f"Score: {score}", True, WHITE)
            self.WINDOW.blit(instruct_surface1, (WIDTH/2 - instruct_surface1.get_width()/2, 300))
            instruct_surface3 = self.SPLASH_TEXT.render("Press ENTER to start again", True, WHITE)
            self.WINDOW.blit(instruct_surface3, (WIDTH/2 - instruct_surface3.get_width()/2, 400))
            pg.display.update()

            splash = True
            while splash:

                self.clock.tick(FRAME_RATE)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                        splash = False
                        break
                
                    if event.type == pg.KEYUP and event.key == pg.K_RETURN:
                        splash = False         
    
    def high_score_screen(self, score, high_scores):
        
        # chosen letters
        lett_0_ind, lett_1_ind, lett_2_ind = 0, 0, 0

        # draw (update so that only initials are re-blited on button press?)
        def draw_high_score_screen(inds, score, high_scores, button_pressed = None):
            
            ind0, ind1, ind2 = inds

            # update letters
            if button_pressed == "Initial_0":
                ind0 += 1
                if ind0 == len(INITALS):
                    ind0 = 0
            elif button_pressed == "Initial_1": 
                ind1 += 1
                if ind1 == len(INITALS):
                    ind1 = 0
            elif button_pressed == "Initial_2": 
                ind2 += 1
                if ind2 == len(INITALS):
                    ind2 = 0

            # pop up window
            wind = pg.Surface((600, 400))
            wind.fill(LIGHT_GREY)
            outline = pg.Surface((610, 410))
            outline.fill(BLACK)
            
            # title
            title_surf = self.SPLASH_TEXT_BIG.render("You're on the leaderboard!", True, BLACK)
            wind.blit(title_surf, (10, 10))

            # initial boxes
            initals_0 = pg.Surface((80, 100))
            initals_1 = pg.Surface((80, 100))
            initals_2 = pg.Surface((80, 100))
            initals_0.fill(WHITE)
            initals_1.fill(WHITE)
            initals_2.fill(WHITE)
            wind.blit(initals_0, (50, 170))
            wind.blit(initals_1, (150, 170))
            wind.blit(initals_2, (250, 170))

            # score
            score_label_surf = self.HIGH_SCORE_LABEL_TEXT.render("Your score: ", True, BLACK)
            wind.blit(score_label_surf, (50, 80))
            score_surf = self.SCORE_TEXT.render(str(score), True, BLACK)
            wind.blit(score_surf, (50, 100))
            
            lett_0_surf = self.INITIALS_TEXT.render(INITALS[ind0], True, "BLACK")
            lett_1_surf = self.INITIALS_TEXT.render(INITALS[ind1], True, "BLACK")
            lett_2_surf = self.INITIALS_TEXT.render(INITALS[ind2], True, "BLACK")

            wind.blit(lett_0_surf, (50 + (80 - lett_0_surf.get_width())/2, 170 + (100 - lett_0_surf.get_height())/2))
            wind.blit(lett_1_surf, (150 + (80 - lett_1_surf.get_width())/2, 170 + (100 - lett_1_surf.get_height())/2))
            wind.blit(lett_2_surf, (250 + (80 - lett_2_surf.get_width())/2, 170 + (100 - lett_2_surf.get_height())/2))

            # blit pop-up window
            self.WINDOW.blit(outline, (WIDTH/2 - outline.get_width()/2, HEIGHT/2 - outline.get_height()/2))
            self.WINDOW.blit(wind, (WIDTH/2 - wind.get_width()/2, HEIGHT/2 - wind.get_height()/2))

            # score board
            board = pg.Surface((220, 200))
            board.fill(WHITE)

            # blit scorebord
            self.WINDOW.blit(board, (500, 130))

            # vertical lines
            pg.draw.line(self.WINDOW, GREY, (530, 130), (530, 330), 3)
            pg.draw.line(self.WINDOW, GREY, (620, 130), (620, 330), 3)

            # horizontal lines
            for line_num in range(1, 5):

                pg.draw.line(self.WINDOW, GREY, (500, (130 + line_num *40)), (720, (130 + line_num *40)), 3)

            # write numbers
            for line_num in range(1, 6):
                
                num_surf = self.HIGH_SCORE_LABEL_TEXT.render(str(line_num), True, BLACK)

                self.WINDOW.blit(num_surf, (515 - num_surf.get_width()/2, (130 + line_num *40 - 20) - num_surf.get_height()/2))

            # write names and scores
            line_num = 1
            for score, name in high_scores:
                
                if name is not None:
                    name_surf = self.HIGH_SCORE_LABEL_TEXT.render(name, True, BLACK)
                else:
                    name_surf = self.HIGH_SCORE_LABEL_TEXT.render(INITALS[ind0] + INITALS[ind1] + INITALS[ind2], True, BLACK)

                self.WINDOW.blit(name_surf, (575 - name_surf.get_width()/2, (130 + line_num *40 - 20) - name_surf.get_height()/2))

                score_surf = self.HIGH_SCORE_LABEL_TEXT.render(str(score), True, BLACK)

                self.WINDOW.blit(score_surf, (670 - score_surf.get_width()/2, (130 + line_num *40 - 20) - score_surf.get_height()/2))
                
                line_num += 1

            # continue text
            continue_surf = self.SPLASH_TEXT.render("Press ENTER to continue", True, BLACK)
            self.WINDOW.blit(continue_surf, (WIDTH/2 - continue_surf.get_width()/2 - 60, 385))

            return ind0, ind1, ind2
        
        draw_high_score_screen((0, 0, 0), score, high_scores)

        # define buttons
        # diff between wind.topleft and WINDOW.topleft: x + 140, y + 48
        b0 = Button(self.WINDOW, (int(50 + (80 - 30)/2 + 140), 280 + 48, 30, 30), WHITE, ">", self.SPLASH_TEXT, BLUEGREY, draw_high_score_screen, "Initial_0", True, False)
        b1 = Button(self.WINDOW, (int(150 + (80 - 30)/2 + 140), 280 + 48, 30, 30), WHITE, ">", self.SPLASH_TEXT, BLUEGREY, draw_high_score_screen, "Initial_1", True, False)
        b2 = Button(self.WINDOW, (int(250 + (80 - 30)/2 + 140), 280 + 48, 30, 30), WHITE, ">", self.SPLASH_TEXT, BLUEGREY, draw_high_score_screen, "Initial_2", True, False)

        # draw buttons
        b0.draw(True)
        b1.draw(True)
        b2.draw(True)

        pg.display.update()

        screen = True
        while screen:

            self.clock.tick(FRAME_RATE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    screen = False
                    break
                
                if event.type == pg.MOUSEBUTTONUP:
                    mouse = pg.mouse.get_pos()
                    for button in [b0, b1, b2]:
                        if button.was_clicked(mouse):
                            lett_0_ind, lett_1_ind, lett_2_ind = button.command((lett_0_ind, lett_1_ind, lett_2_ind), score, high_scores, button.id)
                            b0.draw(True)
                            b1.draw(True)
                            b2.draw(True)
                            pg.display.update()
                
                if event.type == pg.KEYUP and event.key == pg.K_RETURN:
                    final_highs = []
                    for score, name in high_scores:
                        if name is None:
                            final_highs.append([score, INITALS[lett_0_ind] + INITALS[lett_1_ind] + INITALS[lett_2_ind]])
                        else:
                            final_highs.append([score, name])
                    return final_highs

    def level_setup(self):
        lev = list(LEVELS[self.level].values())
        self.level_length = lev[0]
        self.fruit_spawn_rate = lev[1]
        self.fruit_spawn_rate_minimum = lev[2]
        self.fruit_value = lev[3]
        self.fruit_score= lev[4]
        self.score_add_loop = lev[5]
        self.MONEY_ADD_LOOP = lev[6]
        self.level_completion_value = lev[7]
        self.level_completion_score = lev[8]

    def update(self):
        self.WINDOW.blit(self.BACKGROUND, (0, 0))
        # update fruit sprites
        fruit_sprites.update()
        # update player next to keep it on the top layer
        self.player.update()

    def events(self):

        for event in pg.event.get():

            # check for quit
            if event.type == pg.QUIT:
                self.running = False
                
            if event.type == pg.MOUSEBUTTONUP and not self.in_level:
                mouse = pg.mouse.get_pos()
                for button in all_buttons:
                    if button.was_clicked(mouse):
                        button.command()

            if not self.in_level:
                if event.type == pg.KEYUP and event.key == pg.K_RETURN:
                    self.level += 1
                    self.level_setup()
                    self.in_level = True
                    self.spawn_fruit = True
                    self.fruit_spawned_count = 0
        
        if self.in_level:
            # set player image standard
            self.player.image = self.player_imgs[0]

            # check if left key IS pressed
            keymap = pg.key.get_pressed()
            if (keymap[pg.K_a] or keymap[pg.K_LEFT]) and self.player.rect.center[0] >= FIRST_LANE_CENTER:
                self.player.rect.x -= PLAYER_SPEEDS[self.speed_level]
                self.player.hitbox.rect.x -= PLAYER_SPEEDS[self.speed_level]
                self.player.image = self.player_imgs[1]

            # check if right key IS pressed
            if (keymap[pg.K_d] or keymap[pg.K_RIGHT]) and self.player.rect.center[0] <= LAST_LANE_CENTER:
                self.player.rect.x += PLAYER_SPEEDS[self.speed_level]
                self.player.hitbox.rect.x += PLAYER_SPEEDS[self.speed_level]
                self.player.image = self.player_imgs[1]

            if self.spawn_fruit:
                # fruit spawn conditions
                chance = not randint(0, self.fruit_spawn_rate)
                lanes = len([i for i in self.lanes_occupied if not i]) > 0
                time_elapsed = self.last_spawn >= self.fruit_spawn_rate_minimum
                queued = self.spawn_in_queue

                # test for fruit spawn
                if (queued and time_elapsed and lanes) or (chance and time_elapsed and lanes):
                    fruit = Fruit(self.WINDOW, self.FRUIT_TYPES, [i[1] for i in zip(self.lanes_occupied, range(LANES)) if not i[0]])
                    self.lanes_occupied[fruit.lane] = True
                    self.last_spawn = 0
                    self.spawn_in_queue = False
                    self.fruit_spawned_count += 1
                elif (chance and not time_elapsed):
                    self.spawn_in_queue = True
                else:
                    self.last_spawn += 1
                
                if self.fruit_spawned_count == self.level_length:
                    self.spawn_fruit = False
            
            else:
                # if trying to end the level (turned off spawning) check if fruit are all gone
                if len(fruit_sprites) == 0:
                    self.in_level = False
                    self.player.image = self.player_imgs[0]
                    for button in all_buttons:
                        button.is_active = True

            # check for sprite collide
            sprites = pg.sprite.spritecollide(self.player.hitbox, fruit_hitboxes, False)

            # check the details of the collide to see if fruit was caught
            for sprite in sprites:
                x_condition = sprite.rect.center[0] > self.player.hitbox.rect.left and sprite.rect.center[0] < self.player.hitbox.rect.right
                y_condition = sprite.rect.center[1] < self.player.hitbox.rect.top
                if x_condition and y_condition:
                    self.lanes_occupied[sprite.super_sprite.lane] = False
                    sprite.super_sprite.kill()
                    sprite.kill()
                    self.money += self.fruit_value
                    self.score += self.fruit_score

            # despawn fruits
            for fruit in fruit_sprites:
                if fruit.rect.top > HEIGHT:
                    self.lanes_occupied[fruit.lane] = False
                    fruit.hitbox.kill()
                    fruit.kill()
                    pg.mixer.Sound.play(self.miss_sound)
                    if self.lives == 1:
                        self.reset_game()
                    else:
                        self.lives -= 1

            if not self.loop_counter % self.score_add_loop:
                self.score += 1

            if not self.loop_counter % self.MONEY_ADD_LOOP:
                self.money += 1

    def draw(self):
        
        def draw_shape_counter(status, number, coordinates, dimentions, gap, color, stroke, shape="circle"):

            x = coordinates[0]
            y = coordinates[1]

            width = dimentions[0]
            height = dimentions[1]

            for i in range(number):
                if shape == "circle":
                    pg.draw.circle(self.WINDOW, color, (x + i*gap + i*width, y), width, [stroke, 0][status > i])
                else:
                    pg.draw.rect(self.WINDOW, color, (x + i*gap + i*width, y, width, height), [stroke, 0][status > i] )
        
        # score
        score_surface = self.SCORE_TEXT.render(str(self.score), True, BLACK)
        self.WINDOW.blit(score_surface, (10, 0))

        # money counter
        if not BASKET_UPGRADES_PRICES[self.size] is None or not SPEED_UPGRADE_PRICES[self.speed_level] is None:
            money_surface = self.MONEY_TEXT.render("$" + str(float(self.money)) + "0", True, GREEN)
            self.WINDOW.blit(money_surface, (10, 50))

        # lives counter label
        lives_label_surface = self.LIVES_LABEL_TEXT.render("Lives", True, BLACK)
        self.WINDOW.blit(lives_label_surface, (10, HEIGHT - 95))

        # lives
        draw_shape_counter(self.lives, 3, (35, HEIGHT - 35), (25, 25), 35, PINK, 6)

        # basket size
        basket_label_surface = self.LIVES_LABEL_TEXT.render("Basket Size", True, BLACK)
        self.WINDOW.blit(basket_label_surface, (10, HEIGHT - 285))

        price1 = ""
        if BASKET_UPGRADES_PRICES[self.size] is not None:
            price1 = "$" + str(BASKET_UPGRADES_PRICES[self.size])
        else:
            ind = 0
            for i in all_buttons:
                if i.id == "bask":
                    all_buttons.pop(ind)
                    break
                ind += 1

        basket_price_surface1 = self.UPGRADE_PRICE_TEXT.render(price1, True, GREEN)
        self.WINDOW.blit(basket_price_surface1, (100, HEIGHT - 218))

        draw_shape_counter(self.size + 1, 5, (10, HEIGHT - 250), (26, 25), 10, ORANGE, 6, "rect")

        # speed
        basket_label_surface = self.LIVES_LABEL_TEXT.render("Speed", True, BLACK)
        self.WINDOW.blit(basket_label_surface, (10, HEIGHT - (285 + 100)))

        price2 = ""
        if SPEED_UPGRADE_PRICES[self.speed_level] is not None:
            price2 = "$" + str(SPEED_UPGRADE_PRICES[self.speed_level])
        else:
            ind = 0
            for i in all_buttons:
                if i.id == "speed":
                    all_buttons.pop(ind)
                    break
                ind += 1
        basket_price_surface2 = self.UPGRADE_PRICE_TEXT.render(price2, True, GREEN)
        self.WINDOW.blit(basket_price_surface2, (100, HEIGHT - (218 + 100)))

        draw_shape_counter(self.speed_level + 1, 5, (10, HEIGHT - (250 + 100)), (26, 25), 10, ORANGE, 6, "rect")

        if not self.in_level:
            last_level_surface = self.SPLASH_TEXT.render(f"LEVEL {self.level + 1} COMPLETE", True, BLACK)
            self.WINDOW.blit(last_level_surface, (FIRST_LANE_CENTER + (LAST_LANE_CENTER - FIRST_LANE_CENTER)/2 - last_level_surface.get_width()/2, 150))
            next_level_surface = self.SPLASH_TEXT.render(f"PRESS ENTER TO BEGIN LEVEL {self.level + 2}", True, BLACK)
            self.WINDOW.blit(next_level_surface, (FIRST_LANE_CENTER + (LAST_LANE_CENTER - FIRST_LANE_CENTER)/2 - next_level_surface.get_width()/2, 185))

        # draw buttons
        for button in all_buttons:
            button.draw(not self.in_level)

