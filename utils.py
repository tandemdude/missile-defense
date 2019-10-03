import math
import pygame
import typing


def vector_from_positions(
    x: typing.Union[int, float],
    y: typing.Union[int, float],
    end_x: typing.Union[int, float],
    end_y: typing.Union[int, float],
    constant: typing.Union[int, float],
) -> tuple:
    velocity_x = (
        constant * (end_x - x) / math.sqrt(((end_y - y) ** 2) + ((end_x - x) ** 2))
    )
    velocity_y = (
        constant * (end_y - y) / math.sqrt(((end_y - y) ** 2) + ((end_x - x) ** 2))
    )
    return (velocity_x, velocity_y)


def get_angle_positions(
    x: typing.Union[int, float],
    y: typing.Union[int, float],
    end_x: typing.Union[int, float],
    end_y: typing.Union[int, float],
    offset: int,
) -> float:
    radius, angle = pygame.math.Vector2(end_x - x, end_y - y).as_polar()
    return -angle - offset
