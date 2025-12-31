from os import path

# window
FRAME_RATE = 60
WINDOW_RESOLUTION = (16*55, 9*55)
WIDTH = WINDOW_RESOLUTION[0]
HEIGHT = WINDOW_RESOLUTION[1]
RESOLUTION = 10

# layout
LANE_WIDTH = 80
FRUIT_SIZE = 1
LEFT_MARGIN = 225 + LANE_WIDTH
#LANES = 7
LANES = 5
FIRST_LANE_CENTER = LEFT_MARGIN + LANE_WIDTH/2
LAST_LANE_CENTER = LEFT_MARGIN + LANES*LANE_WIDTH - LANE_WIDTH/2
RIGHT_MARGIN = WIDTH - (LAST_LANE_CENTER + LANE_WIDTH/2)
CENTER_LANE = 3

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 30)
GREEN = (23, 131, 23)
BLUEGREY = (91, 99, 113)
BLACK = (0, 0, 0)
PINK = (224, 18, 80)
ORANGE = (225, 128, 0)
GREY = (80, 80, 80)
LIGHT_GREY = (179, 179, 179)

# images
PLAYER_WIDTH = 4584/25
PLAYER_HEIGHT = 5000/25
PLAYER_Y = 390 #405

# directories
IMG_DIR = path.join(path.dirname(__file__), "Imgs")
SND_DIR = path.join(path.dirname(__file__), "Sounds")

# fruits
FRUIT_SPEEDS = [
    ["PINEAPPLE", 3],
    ["COCONUT", 3],
    ["BANANA", 3],
    ["WATERMELON", 3]
]

# hitbox size
HITBOX_SIZE_1, HITBOX_SIZE_1_Y = (64, 15), 360
HITBOX_SIZE_2, HITBOX_SIZE_2_Y = (82, 20), 362
HITBOX_SIZE_3, HITBOX_SIZE_3_Y = (100, 25), 357
HITBOX_SIZE_4, HITBOX_SIZE_4_Y = (120, 30), 352
HITBOX_SIZE_5, HITBOX_SIZE_5_Y = (140, 35), 347
HITBOX_SIZES = (HITBOX_SIZE_1, HITBOX_SIZE_2, HITBOX_SIZE_3, HITBOX_SIZE_4, HITBOX_SIZE_5)
HITBOX_YS = {HITBOX_SIZE_1: HITBOX_SIZE_1_Y, HITBOX_SIZE_2: HITBOX_SIZE_2_Y, HITBOX_SIZE_3: HITBOX_SIZE_3_Y, HITBOX_SIZE_4: HITBOX_SIZE_4_Y, HITBOX_SIZE_5: HITBOX_SIZE_5_Y}
HITBOX_X_ADD = 1

# FONTS
FONT_DIR = "Fonts"
MONEY_FONT = path.join(FONT_DIR, "HARLOWSI.TTF")
LABEL_FONT = path.join(FONT_DIR, "ROCKB.TTF")
SCORE_FONT = path.join(FONT_DIR, "ARLRDBD.TTF")

# upgrades
PLAYER_SPEEDS = (6, 7, 8, 9, 10)
SPEED_UPGRADE_PRICES = (40, 80, 170, 250, 300)
BASKET_UPGRADES_PRICES = (40, 90, 200, 500, 600)

# LEVEL SETUP
def eq(b, c, x, a = None):
    if a is not None:
        return int(x**a + x*b + c)
    else:
        return int(x*b + c)
LEVEL_COUNT = 12
LEVELS = []

# GENERATE LEVELS
for level_num in range(LEVEL_COUNT):
    level_num += 1
    level = {'level_len': eq(2, 5, level_num),
             'spawn_rate': eq(-4, 53, level_num), 
             'minimum_spawn': eq(-4, 55, level_num), 
             'fruit_value': eq(-1, 4, level_num, 1.5),
             'fruit_score': eq(2, 50, level_num, 2), 
             'score_add': eq(-1, 20, level_num), 
             'money_add': eq(-2, 150, level_num), 
             'level_value': eq(2, 20, level_num, 2.5), 
             'level_score': eq(0, 200, level_num, 3.5)}
    LEVELS.append(level)

# HIGH SCORE ASSETS
INITALS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
