from os import path

# window
FRAME_RATE = 60
WINDOW_RESOLUTION = (850, 500)
WIDTH = WINDOW_RESOLUTION[0]
HEIGHT = WINDOW_RESOLUTION[1]

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
SND_DIR = path.join(path.dirname(__file__), "Sounds")

# game mechanics
FRUIT_SPAWN_RATE = 100 # < The lower, the more spawn
FRUIT_SPEEDS = [
    ["PINEAPPLE", 3],
    ["COCONUT", 3],
    ["BANANA", 3],
    ["ORANGE", 3],
    ["LEMON", 3]
]
