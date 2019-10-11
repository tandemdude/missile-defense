import pygame

SPRITE_WIDTH = 20
SPRITE_HEIGHT = 20


class Tower(pygame.sprite.Sprite):
    """
    Class to represent a tower, intended to target and shoot at enemies automatically.
    Aims to decrease the difficulty of the game

    :param game_surface: The :class:`pygame.Surface` to draw the tower onto
    :param screen_width: Int width of the screen in pixels
    :param screen_height: Int height of the
    """

    def __init__(self, game_surface, screen_width, screen_height, get_enemies_func):
        super().__init__()

        self.game_surface = game_surface
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.get_enemies_func = get_enemies_func

        self.range = 100
        self.fire_rate = 10
        self.projectile_speed = 5
        self.all_enemies = None

        self.x = self.screen_width / 4
        self.y = self.screen_height - 50

        self.image = pygame.Surface(
            (SPRITE_WIDTH, SPRITE_HEIGHT), pygame.SRCALPHA
        )
        self.image.fill(pygame.Color("#FFFFFF"))

    def update(self):
        self.game_surface.blit(
            self.image, (self.x, self.y)
        )
