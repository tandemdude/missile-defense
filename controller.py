import pygame
from enemy import Enemy
from reticle import Reticle
from missile import Missile
from wave import Wave
from score import Score

MAX_MISSILES = 5
INITIAL_ENEMIES = 5
ENEMY_CONSTANT = 0.5
TIME_BETWEEN_WAVES = 1
FRAME_RATE = 60


def calculate_enemies_for_wave(initial_enemies, wave_number, constant):
    return round(initial_enemies + (wave_number**2 * constant))


class ControlScheme:

    def __init__(self):
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.fire = pygame.K_SPACE

        """
        self.events = {pygame.KEYDOWN: {self.up: ,
                                        self.down: ,
                                        self.left: ,
                                        self.right: ,
                                        self.fire: 
                                       }
                       pygame.KEYUP: {self.up: ,
                                      self.down: ,
                                      self.left: ,
                                      self.right: 
                                     }
                       }
        """


class Controller:
    
    def __init__(self, game_surface, screen_width, screen_height):
        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.control_scheme = ControlScheme()
        self.reticle = Reticle(self.game_surface, self.screen_width, self.screen_height)
        #self.enemies = [Enemy(self.game_surface, self.screen_width, self.screen_height) for _ in range(6)]
        self.missiles = []

        self.wave_number = 0
        self.current_wave = None
        self.frames_to_next_wave = 0

        self.score = Score(self.game_surface, self.screen_width, self.screen_height)

    def create_new_wave(self):
        number_of_enemies = calculate_enemies_for_wave(INITIAL_ENEMIES, self.wave_number, ENEMY_CONSTANT)
        self.current_wave = Wave(number_of_enemies, None, self.game_surface, self.screen_width, self.screen_height)
        self.wave_number += 1

    def trigger_fire_missile(self, aim_point):
        if len(self.missiles) < MAX_MISSILES:
            self.missiles.append(Missile(self.game_surface, self.screen_width, self.screen_height, self.reticle.x, self.reticle.y))
        print(f"{len(self.missiles)} active missiles")

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
                self.trigger_fire_missile(self.reticle.current_position())

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
            missile_rect = missile.image.get_rect()
            missile_rect.x, missile_rect.y = missile.x, missile.y
            if self.current_wave is not None:
                for enemy in self.current_wave.enemies:
                    if not enemy.visible:
                        continue
                    else:
                        enemy_rect = enemy.image.get_rect()
                        enemy_rect.x, enemy_rect.y = enemy.x, enemy.y
                        if missile_rect.colliderect(enemy_rect):
                            self.score.increment(enemy.value)
                            enemy.visible = False
                            hit_enemy = True
                if hit_enemy:
                    self.missiles.remove(missile)
            if 0 > missile.x or missile.x > self.screen_width or missile.y < 0:
                self.missiles.remove(missile)

    def get_what_needs_to_be_updated(self):
        to_be_updated = self.missiles + [self.reticle, self.score]
        if self.current_wave is not None:
            to_be_updated += [self.current_wave]
            return to_be_updated
        else:
            return to_be_updated

    def update_all(self):
        if self.frames_to_next_wave > 0:
            self.frames_to_next_wave -= 1
        else:
            self.counting_down = False

        if self.current_wave is None and self.frames_to_next_wave == 0:
            self.create_new_wave()

        to_be_updated = self.get_what_needs_to_be_updated()

        for instance in to_be_updated:
            instance.update()

        self.check_collisions()

        if self.current_wave is None or self.current_wave.finished:
            self.current_wave = None
            if not self.counting_down:
                self.frames_to_next_wave = TIME_BETWEEN_WAVES * FRAME_RATE
                self.counting_down = True

