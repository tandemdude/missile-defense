import pygame
import os
from source.controller import Controller
from source.start_screen import StartScreen

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game:
    """
    Class to initialise pygame and contain the main game loop.
    Initialises the game surface and the pygame Clock.
    """
    def __init__(self, start_screen) -> None:
        """
        :param start_screen: Instance of the StartScreen class to display when game begins
        """
        pygame.init()
        pygame.display.set_caption("Missile Defense")
        # Create a display with the dimensions specified by the constants
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_screen = start_screen
        self.running = True
        self.restart = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(os.path.join("fonts", "fixedsys.ttf"), 24)
        # Create the background surface and fill it with a solid colour (black)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(pygame.Color("#000000"))

    @staticmethod
    def quit() -> None:
        """
        Quit out of pygame. Method can be static as it does not require access
        to any attributes defined in self.

        :return: None
        """
        pygame.quit()

    def run(self) -> None:
        """
        Runs the game. Instantiates a Controller object then creates the
        game loop. Handles passing of events to the controller as well
        as flipping the display each frame.

        :return: None
        """
        # Initialise an instance of the Controller class, which manages communication
        # between all other instances used during the running of the game
        controller = Controller(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the main game loop, broken out of when the user quits
        while self.running:
            self.screen.blit(self.background, (0, 0))
            self.clock.tick(60)

            # Get all events occuring at a specific frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and (
                    controller.game_over or not self.start_screen.exited
                ):
                    if event.key == pygame.K_y:
                        self.restart = True
                        self.running = False
                        self.start_screen.exited = True
                    elif event.key == pygame.K_n and (
                        controller.game_over or not self.start_screen.exited
                    ):
                        self.restart = False
                        self.running = False

                # Pass the event to the controller to relay instructions
                # to the other parts of the game if required
                controller.process_event(event)
            # Update all instances required to be updated in any specific frame
            controller.update_all()

            if not self.start_screen.exited:
                self.start_screen.update(self.screen, self.font)
                pygame.display.flip()
                continue
            else:
                controller.running = True

            # Clear the display at the end of each frame
            pygame.display.flip()


def main() -> None:
    """
    Creates a while loop to instantiate a new Game object each time the user
    restarts, or quits out of the program when prompted.

    :return: None
    """
    start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

    while True:
        # Create a new instance of Game each loop to slightly increase memory
        # efficiency and performance; prevents a backup of thousands of references
        # that never get thrown away, preventing crippling of a weaker computer
        game = Game(start_screen)
        game.run()
        # If the user chooses to quit rather than restart, quit the game and break
        # out of the overseer loop
        if not game.restart:
            game.quit()
            return


if __name__ == "__main__":
    main()
