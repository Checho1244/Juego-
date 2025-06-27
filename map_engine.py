import pygame

map_tiles = []

class Tile:
    def __init__(self, x, y, size, solid=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.solid = solid

    def draw(self, win):
        return

TILE_SIZE = 20

def generate_map(map_layout):
    global map_tiles
    map_tiles = []
    for y, row in enumerate(map_layout):
        for x, cell in enumerate(row):
            solid = (cell == 1)
            tile = Tile(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, solid)
            map_tiles.append(tile)
