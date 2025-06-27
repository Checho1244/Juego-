import pygame
import os
import sys
from settings import WIDTH, HEIGHT, WIN, WHITE
from map_loader import list_available_maps, load_map

selected = 0

# Carga y escala las imágenes de fondo
def load_backgrounds(path):
    images = []
    for filename in sorted(os.listdir(path)):
        if filename.endswith((".png", ".jpg", ".bmp")):
            img = pygame.image.load(os.path.join(path, filename)).convert()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            images.append(img)
    return images

# Función para hacer fade entre dos imágenes
def fade_between(surf1, surf2, alpha):
    # surf1 y surf2 deben tener el mismo tamaño
    temp = surf1.copy()
    surf2.set_alpha(alpha)
    temp.blit(surf2, (0, 0))
    surf2.set_alpha(255)
    return temp



def menu():
    font = pygame.font.SysFont(None, 60)
    options = ["1 Jugador", "2 Jugadores", "Opciones", "Salir"]
    selected = -1

    while True:
        WIN.fill((50, 50, 50))
        mx, my = pygame.mouse.get_pos()

        # Cargar fondos
        backgrounds = load_backgrounds("assets/menu_backgrounds")
        if not backgrounds:
            print("No se encontraron imágenes de fondo en assets/menu_backgrounds")
            pygame.quit()
            sys.exit()

        clock = pygame.time.Clock()
        bg_index = 0
        next_bg_index = 1
        fade_alpha = 0
        fade_speed = 3  # Controla la velocidad de la transición
        fading = False
        fade_delay = 3000  # milisegundos antes de empezar a hacer fade
        last_change_time = pygame.time.get_ticks()

        running = True
        while running:
            now = pygame.time.get_ticks()

            # Manejo del cambio de fondo con fade
            if not fading and now - last_change_time > fade_delay:
                fading = True
                fade_alpha = 0

            if fading:
                fade_alpha += fade_speed
                if fade_alpha >= 255:
                    fade_alpha = 255
                    fading = False
                    bg_index = next_bg_index
                    next_bg_index = (next_bg_index + 1) % len(backgrounds)
                    last_change_time = now

            # Dibujar fondo con transición
            if fading:
                bg_surface = fade_between(backgrounds[bg_index], backgrounds[next_bg_index], fade_alpha)
            else:
                bg_surface = backgrounds[bg_index]

            WIN.blit(bg_surface, (0, 0))


            mx, my = pygame.mouse.get_pos()
            for i, text in enumerate(options):
                label = font.render(text, True, WHITE)
                rect = label.get_rect(center=(WIDTH // 2, 200 + i * 100))
                hovered = rect.collidepoint(mx, my)
                color = (50, 50, 100) if not hovered else (100, 100, 255)
                pygame.draw.rect(WIN, color, rect.inflate(40, 20), border_radius=12)
                WIN.blit(label, rect)
                if hovered:
                    selected = i

            pygame.display.update()
            clock.tick(60)

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
    font = pygame.font.SysFont(None, 40)
    title_font = pygame.font.SysFont(None, 60)
    
    title = title_font.render("Controles del Juego", True, WHITE)
    controls = [
        "JUGADOR 1",
        "Flechas: arriba / abajo / izquierda / derecha - Moverse",
        "O - Para cambiar de arma",
        "P - Para disparar",
        " ",
        "JUGADOR 2",
        "A: arriba / S: abajo / A: izquierda / D: derecha - Moverse",
        "C - Para cambiar de arma",
        "espacio - Para disparar"
    ]
    
    esc_text = "Presiona ESC para volver"
    esc_font = pygame.font.SysFont(None, 35)

    while True:
        WIN.fill((30, 30, 30))
        
        # Título
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # Controles
        for i, text in enumerate(controls):
            label = font.render(text, True, WHITE)
            WIN.blit(label, (WIDTH // 2 - label.get_width() // 2, 160 + i * 50))
        
        # ESC button hover effect
        mouse_pos = pygame.mouse.get_pos()
        esc_label = esc_font.render(esc_text, True, WHITE)
        esc_rect = esc_label.get_rect(center=(WIDTH // 2, 660))
        
        if esc_rect.collidepoint(mouse_pos):
            esc_label = esc_font.render(esc_text, True, (255, 100, 100))  # Cambiar color al pasar mouse

        WIN.blit(esc_label, esc_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and esc_rect.collidepoint(mouse_pos):
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

def select_map():
    maps = list_available_maps()
    global selected
    font = pygame.font.SysFont(None, 36)

    while True:
        WIN.fill((20, 20, 20))
        title = font.render("Selecciona un mapa:", True, (255, 255, 255))
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, map_name in enumerate(maps):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            text = font.render(map_name, True, color)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(maps)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(maps)
                elif event.key == pygame.K_RETURN:
                    return load_map(maps[selected]), selected