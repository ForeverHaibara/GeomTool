import time
import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)

class GeomUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Geometry Plot')
        self.screen.fill(BACKGROUND_COLOR)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()

    def draw_test(self):
        pygame.draw.rect(self.screen, (0, 0, 255), [100, 100, 400, 100], 1)
        pygame.display.update()

if __name__ == '__main__':
    test = GeomUI()
    test.draw_test()
    test.run()