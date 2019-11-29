import pygame

from .game_controller import GameController
from .menu_controller import MenuController
from .settings import Settings
from . import utils

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game:
    """
    Class to initialise pygame and contain the main game loop.
    Initialises the game surface and the :class:`pygame.time.Clock`.
    """

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Missile Defence")

        self.settings = Settings()

        self.states = ["START", "PLAYING", "RESTART", "QUIT"]
        self.state = self.states.pop(0)

        # Create a display with the dimensions specified by the constants
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.restart = False
        self.clock = pygame.time.Clock()
        # Create the background surface and fill it with a solid colour (black)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(pygame.Color("#000000"))

        stars = utils.load_image("source.images", "stars.png").convert_alpha()
        stars = pygame.transform.scale(stars, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.blit(stars, (0, 0))

        self.controllers = {
            "START": MenuController(
                self.screen,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                self.settings,
                self.advance_state,
            ),
            "PLAYING": GameController(
                self.screen,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                self.settings,
                self.advance_state,
            ),
            "RESTART": None,
            "QUIT": None,
        }

    @staticmethod
    def quit() -> None:
        """
        Quit out of pygame. Method can be static as it does not require access
        to any attributes defined in self.

        :return: `None`
        """
        pygame.quit()

    def advance_state(self) -> None:
        """
        Move the game into the next state.

        :return: `None`
        """
        self.state = self.states.pop(0)

    def run(self) -> None:
        """
        Runs the game. Instantiates a :class:`source.controller.Controller` object then creates the
        game loop. Handles passing of events to the controller as well
        as flipping the display each frame.

        :return: `None`
        """
        # Create the main game loop, broken out of when the user quits
        while self.running:
            controller = self.controllers[self.state]

            self.screen.blit(self.background, (0, 0))
            self.clock.tick(60)

            # Get all events occuring at a specific frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Pass the event to the controller to relay instructions
                # to the other parts of the game if required
                controller.process_event(event)

                if self.state == "RESTART":
                    self.running = False
                    self.restart = True
                    return
                elif self.state == "QUIT":
                    self.running = False
                    self.restart = False
                    return

            # Update all instances required to be updated in any specific frame
            controller.update_all()

            # Clear the display at the end of each frame
            pygame.display.flip()


def main() -> None:
    """
    Creates a while loop to instantiate a new :class:`source.game.Game` object each time the user
    restarts, or quits out of the program when prompted.

    :return: `None`
    """
    while True:
        # Create a new instance of Game each loop to slightly increase memory
        # efficiency and performance; prevents a backup of thousands of references
        # that never get thrown away, preventing crippling of a weaker computer
        game = Game()
        game.run()
        # If the user chooses to quit rather than restart, quit the game and break
        # out of the overseer loop
        if not game.restart:
            game.quit()
            return


if __name__ == "__main__":
    main()
