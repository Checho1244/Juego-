import math

def rotate_direction(direction, angle_degrees):
    angle_rad = math.radians(angle_degrees)
    dx, dy = direction
    new_dx = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    new_dy = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
    length = math.hypot(new_dx, new_dy)
    return (new_dx / length, new_dy / length) if length != 0 else (0, 1)