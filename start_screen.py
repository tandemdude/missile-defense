import pygame


class StartScreen:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_size = 24
        self.exited = False

    def update(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        welcome_surface = font.render(
            "Welcome to Missile Defense", True, pygame.Color("#ffffff")
        )
        welcome_rect = welcome_surface.get_rect()
        welcome_rect.center = surface.get_rect().center
        surface.blit(welcome_surface, welcome_rect)
        start_msg_surface = font.render(
            "Press [Y] to start or [N] to quit", True, pygame.Color("#ffffff")
        )
        start_msg_rect = start_msg_surface.get_rect()
        start_msg_rect.center = (
            welcome_rect.center[0],
            welcome_rect.center[1] + self.font_size,
        )
        surface.blit(start_msg_surface, start_msg_rect)
