from bullet import create_bullet
from utils import rotate_direction

class Weapon:
    def __init__(self, name, cooldown):
        self.name = name
        self.cooldown = cooldown

    def shoot(self, pos, size, direction):
        if self.name == "Pistola":
            return [create_bullet(pos, size, direction)]
        elif self.name == "Escopeta":
            angles = [-6, -3, 0, 3, 6]
            return [create_bullet(pos, size, rotate_direction(direction, angle)) for angle in angles]
        elif self.name == "Automatica":
            return [create_bullet(pos, size, direction)]
        return []