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

def pause_menu():
    paused = True
    font = pygame.font.SysFont(None, 50)
    small_font = pygame.font.SysFont(None, 30)

    while paused:
        WIN.fill((0, 0, 0))
        pause_text = font.render("Juego en pausa", True, (255, 255, 255))
        resume_text = small_font.render("Presiona Y para continuar o ESC para salir", True, (200, 200, 200))

        WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
        WIN.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    return False
    return True

def death_screen(player_num):
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 30)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    while True:
        WIN.fill((0, 0, 0))
        death_text = font.render(f"Jugador {player_num} ha muerto", True, (255, 0, 0))
        button_text = small_font.render("Volver al menú", True, (255, 255, 255))

        WIN.blit(death_text, (WIDTH // 2 - death_text.get_width() // 2, HEIGHT // 2 - 50))
        pygame.draw.rect(WIN, (100, 100, 100), button_rect)
        WIN.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                               button_rect.centery - button_text.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Volver al menú