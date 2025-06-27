import pygame

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1300, 680 #65-34
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jueguito de supervivencia")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Velocidad y tamaño
PLAYER_SIZE = 40
PLAYER_SPEED = 5
BULLET_SPEED = 50

# Armas
ARMAS = ["Pistola", "Escopeta", "Automatica"]