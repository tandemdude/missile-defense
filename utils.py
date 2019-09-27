import math
import pygame


def vector_from_positions(x, y, end_x, end_y, constant) -> tuple:
    velocity_x = (
        constant * (end_x - x) / math.sqrt(((end_y - y) ** 2) + ((end_x - x) ** 2))
    )
    velocity_y = (
        constant * (end_y - y) / math.sqrt(((end_y - y) ** 2) + ((end_x - x) ** 2))
    )
    return (velocity_x, velocity_y)


def get_angle_positions(x, y, end_x, end_y, offset) -> float:
    radius, angle = pygame.math.Vector2(end_x - x, end_y - y).as_polar()
    return -angle - offset
