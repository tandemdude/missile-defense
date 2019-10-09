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
    """
    Calculates the vector required to navigate from an x, y coordinate to
    a different x, y coordinate.

    :param x: Start x coordinate
    :param y: Start y coordinate
    :param end_x: Final x coordinate
    :param end_y: Final y coordinate
    :param constant: Velocity constant
    :return: Tuple x, y velocity vector
    """
    velocity_x = (
        constant * (end_x - x) / math.sqrt(((end_y - y) ** 2) + ((end_x - x) ** 2))
    )
    velocity_y = (
        constant * (end_y - y) / math.sqrt(((end_y - y) ** 2) + ((end_x - x) ** 2))
    )
    return velocity_x, velocity_y


def get_angle_positions(
    x: typing.Union[int, float],
    y: typing.Union[int, float],
    end_x: typing.Union[int, float],
    end_y: typing.Union[int, float],
    offset: int,
) -> float:
    """
    Calculates the angle between any set of two x, y coordinates.

    :param x: Start x coordinate
    :param y: Start y coordinate
    :param end_x: Final x coordinate
    :param end_y: Final y coordinate
    :param offset: An angle amount in degrees to offset the output by
    :return: Angle in degrees
    """
    radius, angle = pygame.math.Vector2(end_x - x, end_y - y).as_polar()
    return -angle - offset
