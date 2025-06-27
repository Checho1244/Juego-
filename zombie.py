import pygame
import math
import map_engine

zombie_size = 40
zombie_speed = 1.5  
RED = (255, 0, 0)
boss_size = 80
boss_speed = 2
BOSS_COLOR = (255, 100, 0)


class Zombie:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, zombie_size, zombie_size)
        self.hp = 3  

    def draw(self, win):
        pygame.draw.rect(win, RED, self.rect)

    def move_towards(self, target_x, target_y):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        dx = (dx / dist) * zombie_speed
        dy = (dy / dist) * zombie_speed

        new_rect = self.rect.move(dx, dy)

        for tile in map_engine.map_tiles:
            if tile.solid and tile.rect.colliderect(new_rect):
                return

        self.rect = new_rect

    def hit(self, damage):
        self.hp -= damage
        return self.hp <= 0 

class Boss(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, boss_size, boss_size)
        self.hp = 20
        self.pos_x = float(x)
        self.pos_y = float(y)

    def draw(self, win):
        pygame.draw.rect(win, BOSS_COLOR, self.rect)

    def move_towards(self, target_x, target_y):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        dx = (dx / dist) * boss_speed
        dy = (dy / dist) * boss_speed

        new_pos_x = self.pos_x + dx
        new_pos_y = self.pos_y + dy
        new_rect = pygame.Rect(int(new_pos_x), int(new_pos_y), self.rect.width, self.rect.height)

        for tile in map_engine.map_tiles:
            if tile.solid and tile.rect.colliderect(new_rect):
                return

        self.pos_x = new_pos_x
        self.pos_y = new_pos_y
        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

    def hit(self, damage):
        self.hp -= damage
        return self.hp <= 0