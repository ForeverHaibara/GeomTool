import time
import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
DRAW_WIDTH = 600
DRAW_HEIGHT = 600

BUTTON_COLOR_MID = (205, 228, 252)
BUTTON_COLOR_LIGHT = (220, 237, 254)
BUTTON_COLOR_DARK = (100, 164, 230)


class GeomUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Geometry Plot')
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_mouse_button(30, 100, 1)
        self.draw_point_button(30, 150, -1)
        self.draw_line_button(30, 200, -1)
        self.draw_circle_button(30, 250, -1)
    
    def draw_mouse_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        
        width -= 3
        height -= 2
        pts = [(width+7, height-10), (width-7, height+4), (width-1, height+5), (width-4, height+11), (width+2, height+12), (width+5, height+6), (width+11, height+7)]
        pygame.draw.lines(self.screen, BUTTON_COLOR_DARK, closed=True, points=pts, width=3)
        
        
    def draw_point_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width, height-8), radius=3, width=2)
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("pt" , True , BUTTON_COLOR_DARK), (width-8, height))
        
    def draw_line_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-14, height-9), (width-10, height-9), width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-6, height-9), (width+6, height-9), width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width+10, height-9), (width+14, height-9), width=2)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width-8, height-8), radius=3, width=2)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width+8, height-8), radius=3, width=2)
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("line" , True , BUTTON_COLOR_DARK), (width-12, height))
        
    def draw_circle_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width, height-8), radius=3, width=2)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width, height-8), radius=9, width=2)
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("circ" , True , BUTTON_COLOR_DARK), (width-12, height))
        
    def run(self):
        last_mouse_in = -1
        last_event_type = None
        draw_choose = 0
        while True:
            
            mouse = pygame.mouse.get_pos()
            mouse_in = -1
            button_range = [(30, 100), (30, 150), (30, 200), (30, 250)]
            button_draw_fun = [self.draw_mouse_button, self.draw_point_button, self.draw_line_button, self.draw_circle_button]
            for button_num in range(len(button_range)):
                bt = button_range[button_num]
                if bt[0]-20 <= mouse[0] <= bt[0]+20 and bt[1]-20 <= mouse[1] <= bt[1]+20:
                    mouse_in = button_num
            if mouse_in != last_mouse_in:
                if last_mouse_in >= 0:
                    if draw_choose == last_mouse_in:
                        button_draw_fun[last_mouse_in](button_range[last_mouse_in][0], button_range[last_mouse_in][1], 1)
                    else:
                        button_draw_fun[last_mouse_in](button_range[last_mouse_in][0], button_range[last_mouse_in][1], -1)
                if mouse_in >= 0:
                    button_draw_fun[mouse_in](button_range[mouse_in][0], button_range[mouse_in][1], 0)
            last_mouse_in = mouse_in
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            if (event.type == pygame.MOUSEBUTTONDOWN) and (last_event_type != pygame.MOUSEBUTTONDOWN):
                #if the mouse is clicked on the 
                # button the game is terminated 
                if mouse_in >= 0:
                    button_draw_fun[draw_choose](button_range[draw_choose][0], button_range[draw_choose][1], -1)
                    button_draw_fun[mouse_in](button_range[mouse_in][0], button_range[mouse_in][1], 1)
                    draw_choose = mouse_in
            last_event_type = event.type
            
            pygame.display.update()
        
    def draw_line(self):
        for _ in range(300):
            pygame.draw.rect(self.screen, (0, 0, 255), [100, 100 + _ * 0.5, 4000, 8000], 1)
        # pygame.display.update()
        
test = GeomUI()
test.run()
