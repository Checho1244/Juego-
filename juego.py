import pygame
import sys
import random
import math
from settings import WIDTH, HEIGHT, WIN, PLAYER_SIZE, ARMAS
from jugador import Player
from bullet import create_bullet, move_bullets, draw_bullets
from zombie import Zombie
from ui import menu
from utils import rotate_direction

pygame.init()
clock = pygame.time.Clock()

# Listas globales
zombies = []
bullets_p1 = []
bullets_p2 = []

# Variables de oleadas
wave = 1
zombies_remaining = wave * 5
zombies_alive = 0
spawn_timer = 0
SPAWN_DELAY = 30

score = 0

def spawn_zombie():
    x = random.choice([0, WIDTH])
    y = random.randint(0, HEIGHT)
    zombies.append(Zombie(x, y))

def draw(players, two_players):
    WIN.fill((30, 30, 30))
    font = pygame.font.SysFont(None, 30)

    for player in players:
        pygame.draw.rect(WIN, player.color, (*player.pos, player.size, player.size))

    for player, bullets in zip(players, [bullets_p1, bullets_p2]):
        draw_bullets(WIN, bullets)

    score_text = font.render(f"Puntaje: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (10, 10))

    font = pygame.font.SysFont(None, 24)
    for i, player in enumerate(players):
        arma = font.render(f"Jugador {i + 1}: {ARMAS[player.arma_index]}", True, (255, 255, 255))
        WIN.blit(arma, (10, 40 + i * 20))

    for z in zombies:
        z.draw(WIN)

    wave_text = font.render(f"Oleada: {wave}", True, (255, 255, 255))
    WIN.blit(wave_text, (WIDTH - 150, 10))

    pygame.display.update()

def main(two_players=False):
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

        for i in range(len(players)):
            shoot_cooldowns[i] += 1

        # Sistema de oleadas
        if zombies_remaining > 0:
            spawn_timer += 1
            if spawn_timer >= SPAWN_DELAY:
                spawn_zombie()
                zombies_remaining -= 1
                zombies_alive += 1
                spawn_timer = 0

        # Avanzar de oleada
        if zombies_alive <= 0 and zombies_remaining <= 0:
            wave += 1
            zombies_remaining = wave * 5
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
            if keys[p.keys["shoot"]] and shoot_cooldowns[i] >= tiempo[p.arma_index]:
                arma = ARMAS[p.arma_index]
                bullets = bullets_p1 if i == 0 else bullets_p2
                if arma == "Pistola":
                    bullets.append(create_bullet(p.pos, p.size, p.shoot_dir))
                elif arma == "Escopeta":
                    for angle in [-15, 0, 15]:
                        dir = rotate_direction(p.shoot_dir, angle)
                        bullets.append(create_bullet(p.pos, p.size, dir))
                elif arma == "Automatica":
                    bullets.append(create_bullet(p.pos, p.size, p.shoot_dir))
                shoot_cooldowns[i] = 0

        move_bullets(bullets_p1, WIDTH, HEIGHT)
        move_bullets(bullets_p2, WIDTH, HEIGHT)

        # Movimiento y colisión de zombis
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
                print(f"¡{target.color} atrapado!")
                pygame.quit()
                sys.exit()

        # Colisión de balas
        for bullet_list in [bullets_p1, bullets_p2]:
            for bullet, _ in bullet_list[:]:
                for z in zombies[:]:
                    if bullet.colliderect(z):
                        bullet_list.remove((bullet, _))
                        if z.hit(1):
                            zombies.remove(z)
                            zombies_alive -= 1
                            score += 10
                        break

        draw(players, two_players)

if __name__ == "__main__":
    is_two_players = menu()  # Llama al menú principal
    main(is_two_players)