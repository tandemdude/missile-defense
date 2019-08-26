import pygame
from controller import Controller

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.restart = False
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(pygame.Color("#000000"))

    def quit(self):
        pygame.quit()

    def run(self):
        controller = Controller(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        while self.running:
            self.screen.blit(self.background, (0, 0))
            self.clock.tick(60)

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

                controller.process_event(event)
            controller.update_all()

            pygame.display.flip()


def main():
    while True:
        game = Game()
        game.run()
        if not game.restart:
            game.quit()
            break


if __name__ == "__main__":
    main()
