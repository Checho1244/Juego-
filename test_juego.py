import pytest
import pygame
import random
from juego import spawn_zombie, zombies
from settings import WIDTH, HEIGHT, WIN, PLAYER_SIZE, ARMAS
from jugador import Player
from bullet import create_bullet, move_bullets, draw_bullets
from zombie import Zombie
from ui import menu
from utils import rotate_direction
from armas import Weapon

def test_personaje():
	p1_keys = { 
		"up": pygame.K_UP, 
		"down": pygame.K_DOWN, 
		"left": pygame.K_LEFT, 
		"right": pygame.K_RIGHT, 
		"shoot": pygame.K_p, 
		"change": pygame.K_o }
	jugador = Player(WIDTH // 2, 350, (0, 255, 0), p1_keys)

	assert isinstance(jugador, Player)

def test_enemigo():
	x = random.choice([0, 0])
	y = random.randint(0, 0)
	enemigo = Zombie(x,y)

	assert isinstance(enemigo, Zombie)

def test_arma():
	arma = Weapon("Pistola", 15)
	assert isinstance(arma, Weapon)

def test_enemigo_daño():
	x = random.choice([0, 0])
	y = random.randint(0, 0)
	enemigo = Zombie(x,y)

	enemigo.hit(1)
	assert enemigo.hp == 2

	enemigo.hit(2)
	assert enemigo.hp == 0

def test_crear_bala():

	a,b = create_bullet((0,0), 10, (0,1))

	assert b == (0,1)

def test_spawn_zombie_agrega_un_zombie():
    lista = [10]
    lista[0] = spawn_zombie()

    assert len(lista) == 1

def test_bala_mata_zombi():
    bullet = (pygame.Rect(100, 100, 5, 5), None)
    z = Zombie(100, 100)
    zombies.clear()
    zombies.append(z)
    bullets = [bullet]

    for b, _ in bullets[:]:
        for z in zombies[:]:
            if b.colliderect(z.rect):
                bullets.remove((b, _))
                if z.hit(3):
                    zombies.remove(z)

    assert len(zombies) == 0
    assert len(bullets) == 0

