import pygame
import random
import unittest

SPRITE_WIDTH = 20
SPRITE_HEIGHT = 20


class Enemy(pygame.sprite.Sprite):

    def __init__(self, game_surface, screen_width, screen_height):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_surface = game_surface
        self.generate_positions_and_velocities()
        self.visible = True
        self.respawn = False
        self.image = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        self.image.fill(pygame.Color("#ffffff"))
        self.value = 150

        pygame.draw.rect(self.image, pygame.Color("#ff00ff"), (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT))

    def random_start_position(self):
        return (random.randint(0, self.screen_width - SPRITE_WIDTH), 0)

    def random_aim_position(self):
        return (random.randint(0, self.screen_width - SPRITE_WIDTH), self.screen_height - SPRITE_HEIGHT)

    def vector_from_positions(self):
        velocity_x = (self.end_x - self.x) / (self.end_y - self.y)
        return (velocity_x, 1)

    def generate_positions_and_velocities(self):
        self.x, self.y = self.random_start_position()
        self.end_x, self.end_y = self.random_aim_position()
        self.velocity_x, self.velocity_y = self.vector_from_positions()

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def update(self):
        if self.y >= self.screen_height-SPRITE_HEIGHT:
            self.velocity_y = 0
            self.visible = False

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
        self.assertEqual(y_vel, 1)

    def test_velocity_from_positions_positive_x_difference(self):
        e = Enemy(None, 200, 100)
        e.x, e.y = (0, 0)
        e.end_x, e.end_y = (100, 10)
        x_vel, y_vel = e.vector_from_positions()
        self.assertEqual(x_vel, 10)
        self.assertEqual(y_vel, 1)

    def test_velocity_from_positions_negative_x_difference(self):
        e = Enemy(None, 200, 100)
        e.x, e.y = (100, 0)
        e.end_x, e.end_y = (0, 10)
        x_vel, y_vel = e.vector_from_positions()
        self.assertEqual(x_vel, -10)
        self.assertEqual(y_vel, 1)


if __name__ == '__main__':
    unittest.main()