import time
import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
DRAW_WIDTH = 600
DRAW_HEIGHT = 600

BUTTON_COLOR_LIGHT = (170,170,170) 
BUTTON_COLOR_DARK = (100,100,100) 


class GeomUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Geometry Plot')
        self.screen.fill(BACKGROUND_COLOR)
        
    def run(self):
        num = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if the mouse is clicked on the 
                # button the game is terminated 
                if SCREEN_WIDTH/2 <= mouse[0] <= SCREEN_WIDTH/2 + 100 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2 + 30: 
                    num += 1
                    print(num)
            mouse = pygame.mouse.get_pos() 
            if SCREEN_WIDTH/2 <= mouse[0] <= SCREEN_WIDTH/2 + 100 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2 + 30: 
                pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, [SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 100, 30]) 
                  
            else: 
                pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 100, 30]) 
              
            # superimposing the text onto our button 
            self.screen.blit(pygame.font.SysFont('Corbel', 25).render("Button" , True , (255, 255, 255)), (SCREEN_WIDTH/2 + 10, SCREEN_HEIGHT/2 + 5))
                    
            pygame.display.update()

    def draw_line(self):
        pygame.draw.rect(self.screen, (0, 0, 255), [100, 200, 4000, 8000], 1)
        # pygame.display.update()
        
test = GeomUI()
test.draw_line()
test.run()
