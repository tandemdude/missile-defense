import pygame
import random
import unittest
import os

SPRITE_WIDTH = 25
SPRITE_HEIGHT = 30
VERTICAL_VELOCITY = 2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game_surface, screen_width, screen_height):
        super().__init__()

        self.asset = pygame.image.load(
            os.path.join("images", "enemy.png")
        ).convert_alpha()
        self.asset_width, self.asset_height = (
            self.asset.get_width(),
            self.asset.get_height(),
        )

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_surface = game_surface
        self.generate_positions_and_velocities()
        self.visible = True
        self.respawn = False
        self.hit_ground = False
        self.image = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        self.image.fill(pygame.Color("#ffffff"))
        self.value = 150

        self.image = pygame.Surface(
            (self.asset_width, self.asset_height), pygame.SRCALPHA
        )
        self.image.blit(self.asset, (0, 0))
        self.image = pygame.transform.scale(self.image, (SPRITE_WIDTH, SPRITE_HEIGHT))

        self.image = pygame.transform.rotate(self.image, self.get_angle_positions())

    def get_angle_positions(self):
        radius, angle = pygame.math.Vector2(
            self.end_x - self.x, self.end_y - self.y
        ).as_polar()
        return -angle - 270

    def random_start_position(self):
        return (random.randint(0, self.screen_width - SPRITE_WIDTH), 0)

    def random_aim_position(self):
        return (
            random.randint(0, self.screen_width - SPRITE_WIDTH),
            self.screen_height - SPRITE_HEIGHT,
        )

    def vector_from_positions(self):
        velocity_x = (self.end_x - self.x) / (self.end_y - self.y)
        return (velocity_x, VERTICAL_VELOCITY)

    def generate_positions_and_velocities(self):
        self.x, self.y = self.random_start_position()
        self.end_x, self.end_y = self.random_aim_position()
        self.velocity_x, self.velocity_y = self.vector_from_positions()

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def update(self):
        if self.y >= self.screen_height - SPRITE_HEIGHT:
            self.velocity_y = 0
            self.hit_ground = True

        if self.visible:
            self.move()
            self.game_surface.blit(self.image, (self.x, self.y))
        elif self.respawn:
            self.generate_positions_and_velocities()
            self.visible = True


class EnemyTests(unittest.TestCase):
    def test_velocity_from_positions_no_x_difference(self):
        e = Enemy(None, 200, 100)
        e.x, e.y = (10, 0)
        e.end_x, e.end_y = (10, 10)
        x_vel, y_vel = e.vector_from_positions()
        self.assertEqual(x_vel, 0)
        self.assertEqual(y_vel, VERTICAL_VELOCITY)

    def test_velocity_from_positions_positive_x_difference(self):
        e = Enemy(None, 200, 100)
        e.x, e.y = (0, 0)
        e.end_x, e.end_y = (100, 10)
        x_vel, y_vel = e.vector_from_positions()
        self.assertEqual(x_vel, 10)
        self.assertEqual(y_vel, VERTICAL_VELOCITY)

    def test_velocity_from_positions_negative_x_difference(self):
        e = Enemy(None, 200, 100)
        e.x, e.y = (100, 0)
        e.end_x, e.end_y = (0, 10)
        x_vel, y_vel = e.vector_from_positions()
        self.assertEqual(x_vel, -10)
        self.assertEqual(y_vel, VERTICAL_VELOCITY)


if __name__ == "__main__":
    unittest.main()
