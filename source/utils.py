import math
import pygame
import typing
import os
import importlib_resources as resources


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
    :return: :class:`tuple` x, y velocity vector
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
    :param offset: :class:`int` angle amount in degrees to offset the output by
    :return: :class:`float` angle in degrees
    """
    radius, angle = pygame.math.Vector2(end_x - x, end_y - y).as_polar()
    return -angle - offset


def load_image(package, path) -> pygame.Surface:
    """
    Calculates the angle between any set of two x, y coordinates.

    :param package: Package path to resource
    :param path: Filename of resource
    :return: :class:`pygame.Surface` containing loaded resource
    """
    with resources.path(package, path) as image_path:
        image_path = os.path.relpath(image_path)
    return pygame.image.load(image_path)


def load_font(package, path, size) -> pygame.font.Font:
    """
    Calculates the angle between any set of two x, y coordinates.

    :param package: Package path to resource
    :param path: Filename of resource
    :return: :class:`pygame.font.Font` for the loaded font
    """
    with resources.path(package, path) as font_path:
        font_path = os.path.relpath(font_path)
    return pygame.font.Font(font_path, size)
