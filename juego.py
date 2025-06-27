import pygame
import sys
import random
import math
from settings import WIDTH, HEIGHT, WIN, PLAYER_SIZE, ARMAS
from jugador import Player
from bullet import create_bullet, move_bullets, draw_bullets
from zombie import Zombie, Boss, zombie_size, boss_size
from ui import menu, pause_menu, death_screen, select_map
from utils import rotate_direction, mapa_carga
from armas import Weapon
import map_engine

pygame.init()
clock = pygame.time.Clock()

# Listas globales
zombies = []
bullets_p1 = []
bullets_p2 = []

ARMAS = [
    Weapon("Pistola", 30),
    Weapon("Escopeta", 45),
    Weapon("Automatica", 10),
]

# Variables de oleadas
wave = 1
zombies_remaining = wave * 5
zombies_alive = 0
spawn_timer = 0
SPAWN_DELAY = 30

score = 0

def spawn_enemy(players, current_wave):
    max_attempts = 50
    for _ in range(max_attempts):
        x = random.choice([0, WIDTH])
        y = random.randint(0, HEIGHT)
        size = boss_size if (current_wave % 5 == 0) else zombie_size
        new_rect = pygame.Rect(x, y, size, size)

        collides_wall = any(tile.solid and tile.rect.colliderect(new_rect) for tile in map_engine.map_tiles)
        collides_player = any(pygame.Rect(*player.pos, player.size, player.size).colliderect(new_rect) for player in players)

        if not collides_wall and not collides_player:
            if current_wave % 5 == 0:
                # Solo agregar jefe si no hay ya uno
                if not any(isinstance(z, Boss) for z in zombies):
                    zombies.append(Boss(x, y))
                    return
            else:
                zombies.append(Zombie(x, y))
                return

def draw(players, two_players):
    WIN.blit(fondo_actual, (0,0))
    font = pygame.font.SysFont(None, 30)

    for tile in map_engine.map_tiles:
        tile.draw(WIN)

    for player in players:
        pygame.draw.rect(WIN, player.color, (*player.pos, player.size, player.size))

    for player, bullets in zip(players, [bullets_p1, bullets_p2]):
        draw_bullets(WIN, bullets)

    score_text = font.render(f"Puntaje: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (10, 10))

    font = pygame.font.SysFont(None, 24)
    for i, player in enumerate(players):
        arma_nombre = ARMAS[player.arma_index].name
        arma = font.render(f"Jugador {i + 1}: {arma_nombre}", True, (255, 255, 255))
        WIN.blit(arma, (10, 40 + i * 20))

    for z in zombies:
        z.draw(WIN)

    wave_text = font.render(f"Oleada: {wave}", True, (255, 255, 255))
    WIN.blit(wave_text, (WIDTH - 150, 10))

    pygame.display.update()

def main(two_players=False, fondo_actual=None):
    global score, zombies_remaining, zombies_alive, wave, spawn_timer, SPAWN_DELAY
    players = []

    # Crear jugador 1
    p1_keys = {
        "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
        "shoot": pygame.K_p, "change": pygame.K_o
    }
    player1 = Player(WIDTH // 2, 350, (0, 255, 0), p1_keys)
    players.append(player1)

    if two_players:
        # Crear jugador 2
        p2_keys = {
            "up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d,
            "shoot": pygame.K_SPACE, "change": pygame.K_c
        }
        player2 = Player(WIDTH // 2, 450, (0, 0, 255), p2_keys)
        players.append(player2)

    shoot_cooldowns = [0, 0]
    spawn_timer = 0
    running = True
    tiempo = [30, 45, 10]

    while running:
        clock.tick(60)
        spawn_timer += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            should_continue = pause_menu()
            if not should_continue:
                zombies.clear()
                score = 0
                wave = 0
                zombies_alive = 0
                zombies_remaining = 0
                return 

        for i in range(len(players)):
            shoot_cooldowns[i] += 1

        if zombies_remaining > 0:
            spawn_timer += 1
            if spawn_timer >= SPAWN_DELAY:
                spawn_enemy(players, wave)
                zombies_remaining -= 1
                zombies_alive += 1
                spawn_timer = 0

        if zombies_alive <= 0 and zombies_remaining <= 0:
            wave += 1
            if wave % 5 == 0:
                zombies_remaining = 1
            else:
                zombies_remaining = 2**wave
            print(f"¡Oleada {wave}!")

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                for i, p in enumerate(players):
                    if event.key == p.keys["change"]:
                        p.arma_index = (p.arma_index + 1) % len(ARMAS)

        for p in players:
            p.move(keys)
            p.update_shoot_dir(keys)

        # Disparo
        for i, p in enumerate(players):
            if keys[p.keys["shoot"]] and shoot_cooldowns[i] >= ARMAS[p.arma_index].cooldown:
                arma = ARMAS[p.arma_index]
                bullets = bullets_p1 if i == 0 else bullets_p2
                bullets.extend(arma.shoot(p.pos, p.size, p.shoot_dir))
                shoot_cooldowns[i] = 0

        move_bullets(bullets_p1, WIDTH, HEIGHT)
        move_bullets(bullets_p2, WIDTH, HEIGHT)


        for z in zombies[:]:
            if two_players:
                d1 = math.hypot(player1.pos[0] - z.rect.x, player1.pos[1] - z.rect.y)
                d2 = math.hypot(players[1].pos[0] - z.rect.x, players[1].pos[1] - z.rect.y)
            else:
                d1 = math.hypot(player1.pos[0] - z.rect.x, player1.pos[1] - z.rect.y)
                d2 = float('inf')

            target = player1 if d1 < d2 else players[1] if two_players else player1
            z.move_towards(*target.pos)

            player_rect = pygame.Rect(*target.pos, target.size, target.size)
            if z.rect.colliderect(player_rect):
                player_index = players.index(target) + 1
                death_screen(player_index)
                zombies.clear()
                score = 0
                wave = 0
                zombies_alive = 0
                zombies_remaining = 0
                return 

        for bullet_list in [bullets_p1, bullets_p2]:
            for bullet, dir in bullet_list[:]:
                hit_wall = False
                for tile in map_engine.map_tiles:
                    if tile.solid and tile.rect.colliderect(bullet):
                        bullet_list.remove((bullet, dir))
                        hit_wall = True
                        break

                if hit_wall:
                    continue

                for z in zombies[:]:
                    if bullet.colliderect(z):
                        bullet_list.remove((bullet, dir))
                        if z.hit(1):
                            zombies.remove(z)
                            zombies_alive -= 1
                            if isinstance(z, Boss):
                                score += 100
                            else:
                                score += 10
                        break

        draw(players, two_players)

if __name__ == "__main__":
    while True:
        is_two_players = menu() 
        mapa_seleccionado, select = select_map()
        map_engine.generate_map(mapa_seleccionado)
        imagen = mapa_carga(select)
        fondo_actual = pygame.transform.scale(imagen, (WIDTH, HEIGHT))
        main(is_two_players)