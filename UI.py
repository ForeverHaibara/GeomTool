import pygame
import sys

"""
KEY_ESCAPE: Exit
KEY_r: Reset Zoom
KEY_MINUS: Zoom Out
KEY_EQUALS: Zoom In
"""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (255, 255, 255)
DRAW_WIDTH = 800
DRAW_HEIGHT = 800

FIGURE_COLOR = (0, 0, 0)
PICKED_FIGURE_COLOR = (249, 176, 79)

BUTTON_COLOR_MID = (205, 228, 252)
BUTTON_COLOR_LIGHT = (220, 237, 254)
BUTTON_COLOR_DARK = (100, 164, 230)

GEOM_PICK_DIST = 8

# Geometry setting
ERROR = 1e-13

def numberform(realnum):
    if abs(realnum) < 1e-2 or abs(realnum) > 1e3:
        return "{:.3e}".format(realnum)
    else:
        return "{:.3f}".format(realnum)


class GeomUI:
    def __init__(self, fig = []):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Geometry Plot')
        
        self.button_range = [(30, 100), (30, 150), (30, 200), (30, 250)]
        self.button_draw_fun = [self.draw_mouse_button, self.draw_point_button, self.draw_line_button, self.draw_circle_button]
        self.sub_button_range = []
        self.sub_button_draw_fun = []
        self.draw_choose = 0
        self.sub_draw_choose = -1
        
        self.cx = DRAW_WIDTH / 2 + 0.01919810114514
        self.cy = DRAW_HEIGHT / 2 + 0.01145141919810
        self.r = (DRAW_WIDTH + DRAW_HEIGHT) / 9 + 0.114514 + 0.1919810 + ERROR
        
        self.figure_list = fig
    
    def draw_init(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        for fig in self.figure_list:
            if fig[0] == 'Point':
                self.draw_point(fig[1], fig[2], fig[3])
            if fig[0] == 'Line':
                self.draw_line(fig[1], fig[2], fig[3])
            if fig[0] == 'Circle':
                self.draw_circle(fig[1], fig[2], fig[3])
        
        for button_num in range(len(self.button_range)):
            self.button_draw_fun[button_num](self.button_range[button_num][0], self.button_range[button_num][1], 1 if self.draw_choose == button_num else -1)
        for button_num in range(len(self.sub_button_range)):
            self.sub_button_draw_fun[button_num](self.sub_button_range[button_num][0], self.sub_button_range[button_num][1], 1 if self.sub_draw_choose == button_num else -1)
    
    # coordinate change function
    def cc(self, in_c):
        return (self.cx + in_c[0] * self.r, self.cy - in_c[1] * self.r)
    def cc2(self, in_c):
        return ((in_c[0] - self.cx) / self.r, (self.cy - in_c[1]) / self.r)
    
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
        
    def draw_mdpt_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width, height-8), radius=3, width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-2, height-9), (width-12, height-9), width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-12, height-12), (width-12, height-6), width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width+2, height-9), (width+10, height-9), width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width+10, height-12), (width+10, height-6), width=2)
        self.screen.blit(pygame.font.SysFont('Corbel', 15, bold=True).render("mdpt" , True , BUTTON_COLOR_DARK), (width-17, height+1))
        
    def draw_para_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-10, height-4), (width, height-14), width=3)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width, height-4), (width+10, height-14), width=3)
        self.screen.blit(pygame.font.SysFont('Corbel', 17, bold=True).render("para" , True , BUTTON_COLOR_DARK), (width-16, height+1))
        
    def draw_perp_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width, height-4), (width, height-14), width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-12, height-4), (width+12, height-4), width=2)
        self.screen.blit(pygame.font.SysFont('Corbel', 17, bold=True).render("perp" , True , BUTTON_COLOR_DARK), (width-16, height+1))
        
    def draw_pbis_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-2, height-13), (width-2, height-3), width=2)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width-10, height-8), radius=3, width=2)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width+8, height-8), radius=3, width=2)
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("pbis" , True , BUTTON_COLOR_DARK), (width-15, height))

    def draw_point(self, c, color, width):
        realc = self.cc(c)
        pygame.draw.circle(self.screen, color, center=realc, radius=width, width=width)
        
    def draw_line(self, c, color, width):
        if abs(c[0]) < ERROR:
            ht = self.cc((0, -c[2]/c[1]))[1]
            p1 = (0, ht)
            p2 = (SCREEN_WIDTH, ht)
        else:
            if abs(c[1]) < ERROR:
                wd = self.cc((-c[2]/c[0], 0))[0]
                p1 = (wd, 0)
                p2 = (wd, SCREEN_HEIGHT)
            else:
                lf = self.cc2((0, 0))[0]
                rt = self.cc2((SCREEN_WIDTH, 0))[0]
                p1 = self.cc((lf, (-c[2]-c[0]*lf)/c[1]))
                p2 = self.cc((rt, (-c[2]-c[0]*rt)/c[1]))
        pygame.draw.line(self.screen, color, p1, p2, width=width)
        
    def draw_circle(self, c, color, width):
        realc = self.cc((c[0], c[1]))
        pygame.draw.circle(self.screen, color, center=realc, radius=c[2]*self.r, width=width)

    def geomdist(self, mouse, geomtype, c):
        if geomtype == "Point":
            c0 = self.cc2(mouse)
            return self.r * ((c0[0] - c[0]) * (c0[0] - c[0]) + (c0[1] - c[1]) * (c0[1] - c[1])) ** (1/2)
        if geomtype == "Line":
            c0 = self.cc2(mouse)
            return self.r * abs(c0[0] * c[0] + c0[1] * c[1] + c[2]) / ((c[0] * c[0] + c[1] * c[1]) ** (1/2))
        if geomtype == "Circle":
            c0 = self.cc2(mouse)
            return self.r * abs(c[2] - ((c0[0] - c[0]) * (c0[0] - c[0]) + (c0[1] - c[1]) * (c0[1] - c[1])) ** (1/2))

    def run(self):
        self.draw_init()
        last_mouse_in = -1
        last_eventlist = []
        moving_background = False
        
        while True:
            
            mouse = pygame.mouse.get_pos()
            mouse_in = -1
            
            for button_num in range(len(self.button_range)):
                bt = self.button_range[button_num]
                if bt[0]-20 <= mouse[0] <= bt[0]+20 and bt[1]-20 <= mouse[1] <= bt[1]+20:
                    mouse_in = button_num
                    
            for button_num in range(len(self.sub_button_range)):
                bt = self.sub_button_range[button_num]
                if bt[0]-20 <= mouse[0] <= bt[0]+20 and bt[1]-20 <= mouse[1] <= bt[1]+20:
                    mouse_in = button_num + 10
            
            if mouse_in == -1:
                min_dist = 1e10
                min_num = 0
                geom_picked = ""
                for fig_num in range(len(self.figure_list)):
                    dist = self.geomdist(mouse, self.figure_list[fig_num][0], self.figure_list[fig_num][1])
                    if self.figure_list[fig_num][0] == "Point":
                        if dist < GEOM_PICK_DIST:
                            geom_picked = "Point"
                            min_dist = dist
                            min_num = fig_num
                    if self.figure_list[fig_num][0] == "Circle":
                        if dist < GEOM_PICK_DIST and geom_picked not in ("0", "Point"):
                            geom_picked = "Circle"
                            min_dist = dist
                            min_num = fig_num
                    if self.figure_list[fig_num][0] == "Line":
                        if dist < GEOM_PICK_DIST and geom_picked not in ("Point", "Circle"):
                            geom_picked = "Line"
                            min_dist = dist
                            min_num = fig_num
                if geom_picked != "":
                    mouse_in = min_num + 100
                    
            
            if mouse_in != last_mouse_in:
                # Update buttons
                
                if last_mouse_in >= 100 and last_mouse_in < 2000:
                    self.figure_list[last_mouse_in - 100][2] = FIGURE_COLOR
                    self.figure_list[last_mouse_in - 100][3] -= 1
                    self.draw_init()
                if mouse_in >= 100 and mouse_in < 2000:
                    self.figure_list[mouse_in - 100][2] = PICKED_FIGURE_COLOR
                    self.figure_list[mouse_in - 100][3] += 1
                    self.draw_init()
                
                if last_mouse_in >= 0 and last_mouse_in < 10:
                    if self.draw_choose == last_mouse_in:
                        self.button_draw_fun[last_mouse_in](self.button_range[last_mouse_in][0], self.button_range[last_mouse_in][1], 1)
                    else:
                        self.button_draw_fun[last_mouse_in](self.button_range[last_mouse_in][0], self.button_range[last_mouse_in][1], -1)
                if mouse_in >= 0 and mouse_in < 10:
                    self.button_draw_fun[mouse_in](self.button_range[mouse_in][0], self.button_range[mouse_in][1], 0)
                    
                if last_mouse_in >= 10 and last_mouse_in < 20:
                    if self.sub_draw_choose == last_mouse_in - 10:
                        self.sub_button_draw_fun[last_mouse_in - 10](self.sub_button_range[last_mouse_in - 10][0], self.sub_button_range[last_mouse_in - 10][1], 1)
                    else:
                        self.sub_button_draw_fun[last_mouse_in - 10](self.sub_button_range[last_mouse_in - 10][0], self.sub_button_range[last_mouse_in - 10][1], -1)
                if mouse_in >= 10 and mouse_in < 20:
                    self.sub_button_draw_fun[mouse_in - 10](self.sub_button_range[mouse_in - 10][0], self.sub_button_range[mouse_in - 10][1], 0)
                    
            last_mouse_in = mouse_in
            
            eventlist = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    eventlist.append("QUIT")
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    eventlist.append("MOUSEBUTTONDOWN")
                if (event.type == pygame.MOUSEMOTION):
                    eventlist.append("MOUSEMOTION")
                if (event.type == pygame.MOUSEBUTTONUP):
                    eventlist.append("MOUSEBUTTONUP")
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    eventlist.append("K_ESCAPE")
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_MINUS):
                    eventlist.append("K_MINUS")
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_EQUALS):
                    eventlist.append("K_EQUALS")
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
                    eventlist.append("K_r")
            
            
            if ("K_ESCAPE" in eventlist) or ("QUIT" in eventlist):
                    pygame.quit()
            
            if ("MOUSEBUTTONDOWN" in eventlist) and ("MOUSEBUTTONDOWN" not in last_eventlist):
                # the moment when the mouse is clicked on the button
                if mouse_in >= 0 and mouse_in < 10:
                    self.draw_choose = mouse_in
                    self.sub_draw_choose = -1
                    
                    if mouse_in == 0:
                        self.sub_button_range = []
                        self.sub_button_draw_fun = []
                    
                    if mouse_in == 1:
                        self.sub_button_range = [(80, 100)]
                        self.sub_button_draw_fun = [self.draw_mdpt_button]
                        
                    if mouse_in == 2:
                        self.sub_button_range = [(80, 100), (80, 150), (80, 200)]
                        self.sub_button_draw_fun = [self.draw_para_button, self.draw_perp_button, self.draw_pbis_button]
                        
                    if mouse_in == 3:
                        self.sub_button_range = []
                        self.sub_button_draw_fun = []
                    
                    self.draw_init()
                    
                if mouse_in >= 10 and mouse_in < 20:
                    self.sub_draw_choose = mouse_in - 10
                    self.draw_init()
                    
                if mouse_in == -1 and self.draw_choose == 0:
                    moving_background = True
                    moving_background_start = mouse
                    moving_background_start_cx = self.cx
                    moving_background_start_cy = self.cy
            
            if moving_background:
                self.cx = mouse[0] - moving_background_start[0] + moving_background_start_cx
                self.cy = mouse[1] - moving_background_start[1] + moving_background_start_cy
                self.draw_init()
            
            if ("MOUSEMOTION" in eventlist):
                mouse_coordxprt = 'x = ' + numberform(self.cc2(mouse)[0])
                mouse_coordyprt = 'y = ' + numberform(self.cc2(mouse)[1])
                pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(2, 2, 122, 42))
                pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [2, 2, 122, 42], 1)
                self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(mouse_coordxprt , True , FIGURE_COLOR), (5, 5))
                self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(mouse_coordyprt , True , FIGURE_COLOR), (5, 25))
            
            if ("MOUSEBUTTONUP" in eventlist) and ("MOUSEBUTTONUP" not in last_eventlist):
                # the moment when the mouse is unclicked
                if moving_background:
                    moving_background = False
                    
            if ("K_MINUS" in eventlist) and ("K_MINUS" not in last_eventlist):
                center_coord = self.cc2((DRAW_WIDTH/2, DRAW_HEIGHT/2))
                RATIO = 5 / 6
                self.r *= RATIO
                self.cx = DRAW_WIDTH/2 + (self.cx - DRAW_WIDTH/2) * RATIO
                self.cy = DRAW_HEIGHT/2 + (self.cy - DRAW_HEIGHT/2) * RATIO
                self.draw_init()
                
            if ("K_EQUALS" in eventlist) and ("K_EQUALS" not in last_eventlist):
                center_coord = self.cc2((DRAW_WIDTH/2, DRAW_HEIGHT/2))
                RATIO = 6 / 5
                self.r *= RATIO
                self.cx = DRAW_WIDTH/2 + (self.cx - DRAW_WIDTH/2) * RATIO
                self.cy = DRAW_HEIGHT/2 + (self.cy - DRAW_HEIGHT/2) * RATIO
                self.draw_init()
            
            if ("K_r" in eventlist) and ("K_r" not in last_eventlist):
                self.cx = DRAW_WIDTH / 2 + 0.01919810114514
                self.cy = DRAW_HEIGHT / 2 + 0.01145141919810
                self.r = (DRAW_WIDTH + DRAW_HEIGHT) / 9 + 0.114514 + 0.1919810 + ERROR
                self.draw_init()
            
            
            last_event_type = event.type
            
            pygame.display.update()
        
        
test = GeomUI([["Circle", (0,0,1), FIGURE_COLOR, 1],["Line", (-1,0,0), FIGURE_COLOR, 1],["Line", (0,-1,0), FIGURE_COLOR, 1],["Line", (2,3,4), FIGURE_COLOR, 1],["Point", (0,0), FIGURE_COLOR, 4]])
test.run()
