import pygame
import math

zombie_size = 40  # Asegúrate de que coincida con el tamaño en el archivo principal
zombie_speed = 1.5  # Igual que en tu juego
RED = (255, 0, 0)

class Zombie:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, zombie_size, zombie_size)
        self.hp = 3  # Puedes ajustar este valor como quieras

    def draw(self, win):
        pygame.draw.rect(win, RED, self.rect)

    def move_towards(self, target_x, target_y):
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.rect.x += int((dx / dist) * zombie_speed)
            self.rect.y += int((dy / dist) * zombie_speed)

    def hit(self, damage):
        self.hp -= damage
        return self.hp <= 0 