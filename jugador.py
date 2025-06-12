from settings import PLAYER_SIZE, PLAYER_SPEED, ARMAS

class Player:
    def __init__(self, x, y, color, keys):
        self.pos = [x, y]
        self.color = color
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.shoot_dir = (0, 1)
        self.arma_index = 0
        self.last_shoot = 0
        self.keys = keys  # dict con keys para moverse y disparar

    def move(self, keys_pressed):
        if keys_pressed[self.keys["left"]]:
            self.pos[0] -= self.speed
        if keys_pressed[self.keys["right"]]:
            self.pos[0] += self.speed
        if keys_pressed[self.keys["up"]]:
            self.pos[1] -= self.speed
        if keys_pressed[self.keys["down"]]:
            self.pos[1] += self.speed

    def update_shoot_dir(self, keys_pressed):
        if keys_pressed[self.keys["up"]]:
            self.shoot_dir = (0, -1)
        elif keys_pressed[self.keys["down"]]:
            self.shoot_dir = (0, 1)
        elif keys_pressed[self.keys["left"]]:
            self.shoot_dir = (-1, 0)
        elif keys_pressed[self.keys["right"]]:
            self.shoot_dir = (1, 0)