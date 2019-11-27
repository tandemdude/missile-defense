import pygame


class ControlScheme:
    """
	Class to contain the current keybindings for
	any actions that occur during gameplay.
	"""

    def __init__(self) -> None:
        self.up = pygame.K_w
        self.down = pygame.K_s
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.fire = pygame.K_SPACE


class Settings:
    def __init__(self):
        self.control_scheme = ControlScheme()
        self.difficulty = "NORMAL"

    def change_keybind(self, direction, key):
        if direction == "up":
            self.control_scheme.up = key
        elif direction == "down":
            self.control_scheme.down = key
        elif direction == "left":
            self.control_scheme.left = key
        elif direction == "right":
            self.control_scheme.right = key
        elif direction == "fire":
            self.control_scheme.fire = key

    def set_difficulty_easy(self):
        self.difficulty = "EASY"

    def set_difficulty_normal(self):
        self.difficulty = "NORMAL"

    def set_difficulty_hard(self):
        self.difficulty = "HARD"
