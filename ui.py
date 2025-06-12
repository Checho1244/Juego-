import pygame
import sys
from settings import WIDTH, HEIGHT, WIN, WHITE

def menu():
    font = pygame.font.SysFont(None, 60)
    options = ["1 Jugador", "2 Jugadores", "Opciones", "Salir"]
    selected = -1

    while True:
        WIN.fill((50, 50, 50))
        mx, my = pygame.mouse.get_pos()

        for i, text in enumerate(options):
            label = font.render(text, True, WHITE)
            rect = label.get_rect(center=(WIDTH // 2, 200 + i * 100))
            if rect.collidepoint(mx, my):
                pygame.draw.rect(WIN, (100, 100, 100), rect.inflate(20, 20))
                selected = i
            else:
                pygame.draw.rect(WIN, (70, 70, 70), rect.inflate(20, 20))
            WIN.blit(label, rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selected == 0:
                    return False
                elif selected == 1:
                    return True
                elif selected == 2:
                    show_options()
                elif selected == 3:
                    pygame.quit()
                    sys.exit()

def show_options():
    font = pygame.font.SysFont(None, 50)
    label = font.render("Presiona ESC para volver", True, WHITE)

    while True:
        WIN.fill((30, 30, 30))
        WIN.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return