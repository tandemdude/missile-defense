import pygame
from controller import Controller

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Missile Defense")
        # Create a display with the resolution specified by the constants
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.restart = False
        self.clock = pygame.time.Clock()
        # Create the background surface and fill it with a solid colour (black)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(pygame.Color("#000000"))

    @staticmethod
    def quit():
        # Quit out of pygame. Method can be static as it does not require access
        # to any attributes defined in self
        pygame.quit()        

    def run(self):
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
                if event.type == pygame.KEYDOWN and controller.game_over:
                    if event.key == pygame.K_y:
                        self.restart = True
                        self.running = False
                    elif event.key == pygame.K_n and controller.game_over:
                        self.restart = False
                        self.running = False

                # Pass the event to the controller which relays instructions
                # to the other parts of the game if required
                controller.process_event(event)
            # Update all instances required to be updated in any specific frame
            controller.update_all()

            # Clear the display at the end of each frame
            pygame.display.flip()


def main():
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
            break


if __name__ == "__main__":
    main()
