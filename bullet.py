import pygame
from settings import BULLET_SPEED, WHITE

def create_bullet(pos, size, direction):
    dx, dy = direction
    abs_dx, abs_dy = abs(dx), abs(dy)

    center_x = pos[0] + size // 2
    center_y = pos[1] + size // 2

    if abs_dy >= abs_dx:
        bullet = pygame.Rect(center_x - 1, center_y - 10, 2, 20)
    else:
        bullet = pygame.Rect(center_x - 10, center_y - 1, 20, 2)

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