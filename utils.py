import pygame
import math
import os
from map_loader import list_available_maps

def rotate_direction(direction, angle_degrees):
    angle_rad = math.radians(angle_degrees)
    dx, dy = direction
    new_dx = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    new_dy = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
    length = math.hypot(new_dx, new_dy)
    return (new_dx / length, new_dy / length) if length != 0 else (0, 1)

def generate_map(map_layout):
    global map_tiles
    TILE_SIZE = 50
    map_tiles = []
    for y, row in enumerate(map_layout):
        for x, cell in enumerate(row):
            solid = (cell == 1)
            tile = Tile(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, solid)
            map_tiles.append(tile)

def mapa_carga(selected):
    mapas = list_available_maps()

    ruta_fondo = f"assets/fondos/{mapas[selected]}.png"

    fondo_actual = pygame.image.load(ruta_fondo)
    return fondo_actual