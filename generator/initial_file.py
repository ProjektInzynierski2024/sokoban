import random

TILE_SIZE = 40
LEVEL_WIDTH = 20
LEVEL_HEIGHT = 15

def generate_level():
    level = []
    for y in range(LEVEL_HEIGHT):
        row = []
        for x in range(LEVEL_WIDTH):
            tile = random.choice([0, 1])
            row.append(tile)
        level.append(row)
    return level
