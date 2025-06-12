import pygame
from settings import BULLET_SPEED, WHITE

def create_bullet(pos, size, direction):
    if direction in [(0, 1), (0, -1)]:
        bullet = pygame.Rect(pos[0] + size//2, pos[1] + size//2, 1, 20)
    else:
        bullet = pygame.Rect(pos[0] + size//2, pos[1] + size//2, 20, 1)
    return (bullet, direction)

def move_bullets(bullets, width, height):
    for b in bullets[:]:
        b[0].x += b[1][0] * BULLET_SPEED
        b[0].y += b[1][1] * BULLET_SPEED
        if b[0].x < 0 or b[0].x > width or b[0].y < 0 or b[0].y > height:
            bullets.remove(b)

def draw_bullets(win, bullets):
    for b in bullets:
        pygame.draw.rect(win, WHITE, b[0])