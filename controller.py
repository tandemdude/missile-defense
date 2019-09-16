import pygame
import os
from reticle import Reticle
from missile import Missile
from wave import Wave
from score import Score
from lives import Lives
from game_over import GameOver

MAX_MISSILES = 5
INITIAL_ENEMIES = 5
ENEMY_CONSTANT = 0.5
TIME_BETWEEN_WAVES = 1
FRAME_RATE = 60
LIVES = 3
FONT_SIZE = 24


def calculate_enemies_for_wave(initial_enemies, wave_number, constant):
    return round(initial_enemies + (wave_number ** 2 * constant))


def get_rect_of_instance(instance):
    rect = instance.image.get_rect()
    rect.x, rect.y = instance.x, instance.y
    return rect


def is_colliding(rect1, rect2):
    return rect1.colliderect(rect2)


class ControlScheme:
    def __init__(self):
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.fire = pygame.K_SPACE


class Controller:
    def __init__(self, game_surface, screen_width, screen_height):
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.control_scheme = ControlScheme()
        self.reticle = Reticle(self.game_surface, self.screen_width, self.screen_height)
        self.missiles = []

        self.wave_number = 0
        self.current_wave = None
        self.frames_to_next_wave = 0
        self.counting_down = False

        self.lives = Lives(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE, LIVES
        )
        self.game_over_screen = GameOver(
            self.game_surface, self.screen_width, self.screen_height, FONT_SIZE
        )
        self.decrement_lives = self.lives.decrement
        self.game_over = False

        self.score = Score(self.game_surface, self.screen_width, self.screen_height)
        self.font = pygame.font.Font(
            os.path.join("fonts", "SevenSegment.ttf"), FONT_SIZE
        )

    def enemy_hit_ground(self):
        self.lives.decrement()

    def create_new_wave(self):
        number_of_enemies = calculate_enemies_for_wave(
            INITIAL_ENEMIES, self.wave_number, ENEMY_CONSTANT
        )
        self.current_wave = Wave(
            number_of_enemies,
            None,
            self.game_surface,
            self.screen_width,
            self.screen_height,
            self.enemy_hit_ground,
        )

        self.wave_number += 1

    def trigger_fire_missile(self):
        if len(self.missiles) < MAX_MISSILES:
            self.missiles.append(
                Missile(
                    self.game_surface,
                    self.screen_width,
                    self.screen_height,
                    self.reticle.x,
                    self.reticle.y,
                )
            )

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.control_scheme.left:
                self.reticle.left()
            elif event.key == self.control_scheme.right:
                self.reticle.right()
            elif event.key == self.control_scheme.up:
                self.reticle.up()
            elif event.key == self.control_scheme.down:
                self.reticle.down()
            elif event.key == self.control_scheme.fire:
                self.trigger_fire_missile()

        elif event.type == pygame.KEYUP:
            if event.key == self.control_scheme.left:
                self.reticle.left(False)
            elif event.key == self.control_scheme.right:
                self.reticle.right(False)
            elif event.key == self.control_scheme.up:
                self.reticle.up(False)
            elif event.key == self.control_scheme.down:
                self.reticle.down(False)

    def check_collisions(self):
        for missile in self.missiles[:]:
            hit_enemy = False
            missile_rect = get_rect_of_instance(missile)
            if self.current_wave is not None:
                for enemy in self.current_wave.enemies:
                    if enemy.visible and is_colliding(
                        missile_rect, get_rect_of_instance(enemy)
                    ):
                        self.score.increment(enemy.value)
                        enemy.visible = False
                        hit_enemy = True
                if hit_enemy:
                    self.missiles.remove(missile)
            if 0 > missile.x or missile.x > self.screen_width or missile.y < 0:
                self.missiles.remove(missile)

    def get_what_needs_to_be_updated(self):
        if self.game_over:
            to_be_updated = [self.score, self.lives, self.game_over_screen]
        else:
            to_be_updated = self.missiles + [self.reticle, self.score, self.lives]
            if self.current_wave is not None:
                to_be_updated += [self.current_wave]
        return to_be_updated

    def create_new_wave_if_required(self):
        if self.frames_to_next_wave > 0:
            self.frames_to_next_wave -= 1
        else:
            self.counting_down = False

        if self.current_wave is None and self.frames_to_next_wave == 0:
            self.create_new_wave()

    def check_if_wave_finished(self):
        if self.current_wave is None or self.current_wave.finished:
            self.current_wave = None
            if not self.counting_down:
                self.frames_to_next_wave = TIME_BETWEEN_WAVES * FRAME_RATE
                self.counting_down = True

    def update_all(self):
        if self.lives == 0:
            self.game_over = True
        else:
            self.create_new_wave_if_required()
            self.check_collisions()
            self.check_if_wave_finished()

        to_be_updated = self.get_what_needs_to_be_updated()
        for instance in to_be_updated:
            instance.update()
