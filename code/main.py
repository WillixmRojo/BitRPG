import pygame, sys
from settings import *
from level import Level
from debug import debug

class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            try:
                icon = pygame.image.load('C:/Users/willi/Py Projects/zeldaproject/triforce.png')
            except pygame.error as e:
                print('Error loading image', e)

            new_size = (50,50)
            icon_resized = pygame.transform.scale(icon, new_size)

            self.screen.fill('black')
            self.level.run()
            #debug(icon_resized)
            pygame.display.set_caption('Zelda Project - FPS: ' + str(int(self.clock.tick())))
            pygame.display.set_icon(icon_resized)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()