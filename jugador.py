from settings import PLAYER_SIZE, PLAYER_SPEED, ARMAS
import pygame
import map_engine

class Player:
    def __init__(self, x, y, color, keys):
        self.pos = [x, y]
        self.color = color
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.shoot_dir = (0, 1)
        self.arma_index = 0
        self.last_shoot = 0
        self.keys = keys 

    def move(self, keys_pressed):
        dx, dy = 0, 0
        if keys_pressed[self.keys["left"]]:
            dx -= self.speed
        if keys_pressed[self.keys["right"]]:
            dx += self.speed
        if keys_pressed[self.keys["up"]]:
            dy -= self.speed
        if keys_pressed[self.keys["down"]]:
            dy += self.speed

        new_rect = pygame.Rect(
            self.pos[0] + dx,
            self.pos[1] + dy,
            self.size,
            self.size
        )

        for tile in map_engine.map_tiles:
            if tile.solid and tile.rect.colliderect(new_rect):
                return

        self.pos[0] += dx
        self.pos[1] += dy

    def update_shoot_dir(self, keys_pressed):
        if keys_pressed[self.keys["up"]]:
            self.shoot_dir = (0, -1)
        elif keys_pressed[self.keys["down"]]:
            self.shoot_dir = (0, 1)
        elif keys_pressed[self.keys["left"]]:
            self.shoot_dir = (-1, 0)
        elif keys_pressed[self.keys["right"]]:
            self.shoot_dir = (1, 0)