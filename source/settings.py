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
    """
    Class to contain a player's gameplay settings.
    Contains the control scheme and game difficulty.
    """
    def __init__(self):
        self.control_scheme = ControlScheme()
        self.difficulty = "NORMAL"

    def change_keybind(self, direction: str, key: int) -> None:
        """
        Procedure to change the control scheme key binding for
        a specific direction.

        :param direction: :class:`str` direction of the key to change
        :param key: :class:`int` pygame constant representing a key
        :return: `None`
        """
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

    def set_difficulty_easy(self) -> None:
        """
        Procedure to set the game difficulty to easy

        :return: `None`
        """
        self.difficulty = "EASY"

    def set_difficulty_normal(self) -> None:
        """
        Procedure to set the game difficulty to normal

        :return: `None`
        """
        self.difficulty = "NORMAL"

    def set_difficulty_hard(self) -> None:
        """
        Procedure to set the game difficulty to hard

        :return: `None`
        """
        self.difficulty = "HARD"
