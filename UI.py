import pygame
import GeomTool

"""
KEY_ESCAPE: Exit
KEY_r: Reset Zoom
KEY_MINUS: Zoom Out
KEY_EQUALS / KEY_PLUS: Zoom In
KEY_CONTROL: Start CMD
KEY_ALT: Print TAG
"""

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (244, 244, 244)
DRAW_WIDTH = 800
DRAW_HEIGHT = 800

FIGURE_COLOR = (0, 0, 0)
PICKED_FIGURE_COLOR = (131, 251, 128)
CHOSEN_FIGURE_COLOR = (249, 176, 79)

BUTTON_COLOR_MID = (205, 228, 252)
BUTTON_COLOR_LIGHT = (220, 237, 254)
BUTTON_COLOR_DARK = (100, 164, 230)

TAG_COLOR = (237, 56, 115)

GEOM_PICK_DIST = 8

# Geometry setting
ERROR = 1e-13

def choose_order_of_object(in_type):
    if in_type == "Line":
        return 1
    if in_type == "Circle":
        return 2
    if in_type == "Point":
        return 3

def numberform(realnum):
    # String a number in a relatively short form
    if abs(realnum) < 1e-2 or abs(realnum) > 1e3:
        return "{:.3e}".format(realnum)
    else:
        return "{:.3f}".format(realnum)

def fig_intersection(fig1, fig2):
    if fig1.type == "Line":
        if fig2.type == "Line":
            if abs(fig1.c[1] * fig2.c[0] - fig1.c[0] * fig2.c[1]) > ERROR:
                return [((fig1.c[2] * fig2.c[1] - fig1.c[1] * fig2.c[2])/(fig1.c[1] * fig2.c[0] - fig1.c[0] * fig2.c[1]), (-fig1.c[2] * fig2.c[0] + fig1.c[0] * fig2.c[2])/(fig1.c[1] * fig2.c[0] - fig1.c[0] * fig2.c[1]))]
            else:
                return []
        if fig2.type == "Circle":
            Disc = (-(fig1.c[2] + fig1.c[0] * fig2.c[0] + fig1.c[1] * fig2.c[1])**2 + (fig1.c[0]**2 + fig1.c[1]**2) * fig2.c[2]**2)
            if  Disc >= 0:
                Delta = fig1.c[1]**2 * (-(fig1.c[2] + fig1.c[0] * fig2.c[0] + fig1.c[1] * fig2.c[1])**2 + (fig1.c[0]**2 + fig1.c[1]**2) * fig2.c[2]**2)
                x1 = -((-fig1.c[1]**2 * fig2.c[0] + fig1.c[0] * (fig1.c[2] + fig1.c[1] * fig2.c[1]) + Delta ** (1/2))/(fig1.c[0]**2 + fig1.c[1]**2))
                x2 = -((-fig1.c[1]**2 * fig2.c[0] + fig1.c[0] * (fig1.c[2] + fig1.c[1] * fig2.c[1]) - Delta ** (1/2))/(fig1.c[0]**2 + fig1.c[1]**2))
                Delta = fig1.c[0]**2 * (-(fig1.c[2] + fig1.c[1] * fig2.c[1] + fig1.c[0] * fig2.c[0])**2 + (fig1.c[1]**2 + fig1.c[0]**2) * fig2.c[2]**2)
                y1 = -((-fig1.c[0]**2 * fig2.c[1] + fig1.c[1] * (fig1.c[2] + fig1.c[0] * fig2.c[0]) + Delta ** (1/2))/(fig1.c[1]**2 + fig1.c[0]**2))
                y2 = -((-fig1.c[0]**2 * fig2.c[1] + fig1.c[1] * (fig1.c[2] + fig1.c[0] * fig2.c[0]) - Delta ** (1/2))/(fig1.c[1]**2 + fig1.c[0]**2))
                if Disc >= ERROR:
                    if abs(fig1.c[0] * x1 + fig1.c[1] * y1 + fig1.c[2]) < ERROR:
                        return [(x1, y1), (x2, y2)]
                    else:
                        return [(x1, y2), (x2, y1)]
                else:
                    return [(x1, y1)]
    if fig1.type == "Circle":
        if fig2.type == "Line":
            return fig_intersection(fig2, fig1)
        if fig2.type == "Circle":
            if abs(fig1.c[0] - fig2.c[0]) > ERROR or abs(fig1.c[1] - fig2.c[1]) > ERROR:
                fig3 = GeomTool.Geom_object("fig3", "Line", None, None)
                fig3.c = (2 * (fig2.c[0] - fig1.c[0]), 2 * (fig2.c[1] - fig1.c[1]), (fig1.c[0]**2 + fig1.c[1]**2 - fig1.c[2]**2) - (fig2.c[0]**2 + fig2.c[1]**2 - fig2.c[2]**2))
                return fig_intersection(fig3, fig1)
    return []

class GeomUI:
    def __init__(self, in_geom_list):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Geometry Plot')
        
        self.button_range = [(30, 100), (30, 150), (30, 200), (30, 250)]
        self.button_draw_fun = [self.draw_mouse_button, self.draw_point_button, self.draw_line_button, self.draw_circle_button]
        self.sub_button_range = []
        self.sub_button_draw_fun = []
        self.yn_button_range = [(30, 400), (30, 450)]
        self.yn_button_draw_fun = [self.draw_cmd_button, self.draw_tag_button]
        self.yn_button_pressed = [-1, 1]
        self.draw_choose = 0
        self.sub_draw_choose = -1
        
        self.cx = DRAW_WIDTH / 2 + 0.01919810114514
        self.cy = DRAW_HEIGHT / 2 + 0.01145141919810
        self.r = (DRAW_WIDTH + DRAW_HEIGHT) / 9 + 0.114514 + 0.1919810 + ERROR
        
        self.geom_list = in_geom_list # All geom objects
        self.geom_show = [True for fig_num in range(len(in_geom_list))] # A True False sequence that show a geom object or not
        self.geom_chosen = [0 for fig_num in range(len(in_geom_list))] # Chosen geom objects 0, >0
        self.geom_picked_list = []
    
    def choose_fig_list(self, mouse, allows = ("Point", "Line", "Circle")):
        # Choose a fig in geom_list that has geom_show
        out_fig_list = []
        for fig_num in range(len(self.geom_list)):
            if self.geom_show[fig_num] and self.geom_list[fig_num].hasc and (self.geom_list[fig_num].type in allows):
                dist = self.geomdist(mouse, self.geom_list[fig_num].type, self.geom_list[fig_num].c)
                if dist < GEOM_PICK_DIST:
                    out_fig_list.append((fig_num, -choose_order_of_object(self.geom_list[fig_num].type) + dist/(2 * GEOM_PICK_DIST)))
        out_fig_list.sort(key = lambda x: x[1])
        return list(_[0] for _ in out_fig_list)
    
    def choose_fig1(self, mouse):
        # Choose a fig in geom_list that has geom_show
        lst = self.choose_fig_list(mouse)
        if len(lst) < 2:
            self.geom_picked_list = lst
        else:
            self.geom_picked_list = [lst[0]]
            
    def choose_fig2(self, mouse):
        # Choose a fig in geom_list that has geom_show
        lst = self.choose_fig_list(mouse, ("Line", "Circle"))
        inxlst = []
        outlst = []
        if len(lst) < 2:
            self.geom_picked_list = lst
        else:
            for fig_num1 in range(len(lst)):
                for fig_num2 in range(fig_num1 + 1, len(lst)):
                    inxlst += list((fig_num1, fig_num2, _) for _ in fig_intersection(self.geom_list[lst[fig_num1]], self.geom_list[lst[fig_num2]]))
            for _ in inxlst:
                if self.geomdist(mouse, "Point", _[2]) < GEOM_PICK_DIST:
                    outlst.append((_, self.geomdist(mouse, "Point", _[2])))
            outlst.sort(key = lambda x: x[1])
            if len(outlst) > 0:
                self.geom_picked_list = [lst[outlst[0][0][0]], lst[outlst[0][0][1]]]
            else:
                self.geom_picked_list = [lst[0]]
    
    def draw_fig(self):
        
        for fig_num in range(len(self.geom_list)):
            if self.geom_show[fig_num] and self.geom_list[fig_num].hasc and self.geom_list[fig_num].type == 'Line':
                if (self.geom_chosen[fig_num] == 0) and (fig_num not in self.geom_picked_list):
                    self.draw_line(self.geom_list[fig_num].c, FIGURE_COLOR, 1)
                if (self.geom_chosen[fig_num] > 0) and (fig_num not in self.geom_picked_list):
                    self.draw_line(self.geom_list[fig_num].c, CHOSEN_FIGURE_COLOR, 2)
                if (fig_num in self.geom_picked_list):
                    self.draw_line(self.geom_list[fig_num].c, PICKED_FIGURE_COLOR, 2)
        
        for fig_num in range(len(self.geom_list)):
            if self.geom_show[fig_num] and self.geom_list[fig_num].hasc and self.geom_list[fig_num].type == 'Circle':
                if (self.geom_chosen[fig_num] == 0) and (fig_num not in self.geom_picked_list):
                    self.draw_circle(self.geom_list[fig_num].c, FIGURE_COLOR, 1)
                if (self.geom_chosen[fig_num] > 0) and (fig_num not in self.geom_picked_list):
                    self.draw_circle(self.geom_list[fig_num].c, CHOSEN_FIGURE_COLOR, 2)
                if (fig_num in self.geom_picked_list):
                    self.draw_circle(self.geom_list[fig_num].c, PICKED_FIGURE_COLOR, 2)
                    
        for fig_num in range(len(self.geom_list)):
            if self.geom_show[fig_num] and self.geom_list[fig_num].hasc and self.geom_list[fig_num].type == 'Point':
                if (self.geom_chosen[fig_num] == 0) and (fig_num not in self.geom_picked_list):
                    self.draw_point(self.geom_list[fig_num].c, FIGURE_COLOR, 4)
                if (self.geom_chosen[fig_num] > 0) and (fig_num not in self.geom_picked_list):
                    self.draw_point(self.geom_list[fig_num].c, CHOSEN_FIGURE_COLOR, 5)
                if (fig_num in self.geom_picked_list):
                    self.draw_point(self.geom_list[fig_num].c, PICKED_FIGURE_COLOR, 5)
                if self.yn_button_pressed[1] == 1:
                    self.screen.blit(pygame.font.SysFont('TimesNewRoman', 20, bold=True).render(self.geom_list[fig_num].name , True , TAG_COLOR), self.cc(self.geom_list[fig_num].c))
            
    
    def draw_init(self):
        # Draw geometric objects and buttons
        
        self.screen.fill(BACKGROUND_COLOR)
        
        self.draw_fig()
        
        # Draw buttons
        
        for button_num in range(len(self.button_range)):
            self.button_draw_fun[button_num](self.button_range[button_num][0], self.button_range[button_num][1], 1 if self.draw_choose == button_num else -1)
        for button_num in range(len(self.sub_button_range)):
            self.sub_button_draw_fun[button_num](self.sub_button_range[button_num][0], self.sub_button_range[button_num][1], 1 if self.sub_draw_choose == button_num else -1)
        for button_num in range(len(self.yn_button_range)):
            self.yn_button_draw_fun[button_num](self.yn_button_range[button_num][0], self.yn_button_range[button_num][1], self.yn_button_pressed[button_num])
    
        # Draw command area
        if self.yn_button_pressed[0] == 1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(2 + DRAW_WIDTH, 2, SCREEN_WIDTH - DRAW_WIDTH - 5, SCREEN_HEIGHT - 5))
            pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [2 + DRAW_WIDTH, 2, SCREEN_WIDTH - DRAW_WIDTH - 5, SCREEN_HEIGHT - 5], 1)
        
    # Coordinate change functions
    # cc for geom_coord to screen_coord, cc2 for screen_coord to geom_coord
    def cc(self, in_c):
        return (self.cx + in_c[0] * self.r, self.cy - in_c[1] * self.r)
    def cc2(self, in_c):
        return ((in_c[0] - self.cx) / self.r, (self.cy - in_c[1]) / self.r)
    
    # Functions to draw buttons
    
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
        
    # Functions to draw sub_buttons
    
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
    
    # Functions to draw extra buttons
    
    def draw_cmd_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        self.screen.blit(pygame.font.SysFont('Corbel', 15, bold=True).render(">>>" , True , BUTTON_COLOR_DARK), (width-12, height-14))
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("cmd" , True , BUTTON_COLOR_DARK), (width-17, height))
        
    def draw_tag_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.circle(self.screen, BUTTON_COLOR_DARK, center=(width-8, height-8), radius=3, width=2)
        pts = [(width-14, height-14), (width-14, height-2), (width+6, height-2), (width+12, height-8), (width+6, height-14)]
        pygame.draw.lines(self.screen, BUTTON_COLOR_DARK, closed=True, points=pts, width=2)
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("tag" , True , BUTTON_COLOR_DARK), (width-13, height))
    
    # Functions to draw Geometric Figures
    
    def draw_point(self, c, color, width):
        realc = self.cc(c)
        pygame.draw.circle(self.screen, color, center=realc, radius=width, width=width)
        
    def draw_line(self, c, color, width):
        if abs(c[0]) < ERROR:
            ht = self.cc((0, -c[2]/c[1]))[1]
            point1 = (0, ht)
            point2 = (SCREEN_WIDTH, ht)
        else:
            if abs(c[1]) < ERROR:
                wd = self.cc((-c[2]/c[0], 0))[0]
                point1 = (wd, 0)
                point2 = (wd, SCREEN_HEIGHT)
            else:
                lf = self.cc2((0, 0))[0]
                rt = self.cc2((SCREEN_WIDTH, 0))[0]
                point1 = self.cc((lf, (-c[2]-c[0]*lf)/c[1]))
                point2 = self.cc((rt, (-c[2]-c[0]*rt)/c[1]))
        pygame.draw.line(self.screen, color, point1, point2, width=width)
        
    def draw_circle(self, c, color, width):
        realc = self.cc((c[0], c[1]))
        pygame.draw.circle(self.screen, color, center=realc, radius=c[2]*self.r, width=width)
    
    # measure the screen distance from mouse to a geom_figure
    
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
        return 1e10

    def run(self):
        self.draw_init()
        last_mouse_in = -1
        last_eventlist = []
        moving_background = False
        
        while True:
            
            #Get mouse info
            
            mouse = pygame.mouse.get_pos()
            mouse_in = -1
            
            # Picking Buttons
            
            for button_num in range(len(self.button_range)):
                bt = self.button_range[button_num]
                if bt[0]-20 <= mouse[0] <= bt[0]+20 and bt[1]-20 <= mouse[1] <= bt[1]+20:
                    mouse_in = button_num
                    
            for button_num in range(len(self.sub_button_range)):
                bt = self.sub_button_range[button_num]
                if bt[0]-20 <= mouse[0] <= bt[0]+20 and bt[1]-20 <= mouse[1] <= bt[1]+20:
                    mouse_in = button_num + 10
                    
            for button_num in range(len(self.yn_button_range)):
                bt = self.yn_button_range[button_num]
                if bt[0]-20 <= mouse[0] <= bt[0]+20 and bt[1]-20 <= mouse[1] <= bt[1]+20:
                    mouse_in = button_num + 20
            
            if mouse_in == -1:
                
                # Picking Geometric Figures
                if self.draw_choose in (1, 2, 3):
                    self.choose_fig2(mouse)
                    if len(self.geom_picked_list) == 0:
                        mouse_in = -1
                    elif len(self.geom_picked_list) == 1:
                        mouse_in = self.geom_picked_list[0] + 100
                    else:
                        mouse_in = (self.geom_picked_list[0] + 100) * 1000 + (self.geom_picked_list[1] + 100)
                if self.draw_choose == 0:
                    self.choose_fig1(mouse)
                    if len(self.geom_picked_list) == 0:
                        mouse_in = -1
                    else:
                        mouse_in = self.geom_picked_list[0] + 100
                    
            
            if mouse_in != last_mouse_in:
                
                # Update Geometric Figures
                
                if mouse_in == -1 or mouse_in >= 100:
                    self.draw_init()
                
                # Update buttons
                
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
                    
                if last_mouse_in >= 20 and last_mouse_in < 30:
                    self.yn_button_draw_fun[last_mouse_in - 20](self.yn_button_range[last_mouse_in - 20][0], self.yn_button_range[last_mouse_in - 20][1], self.yn_button_pressed[last_mouse_in - 20])
                if mouse_in >= 20 and mouse_in < 30:
                    self.yn_button_draw_fun[mouse_in - 20](self.yn_button_range[mouse_in - 20][0], self.yn_button_range[mouse_in - 20][1], 0)
                    
            last_mouse_in = mouse_in
            
            # MOUSE and KEY events
            
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
                if (event.type == pygame.KEYDOWN):
                    eventlist.append("KEYDOWN")
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    eventlist.append("K_ESCAPE")
                if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_MINUS) or (event.key == pygame.K_KP_MINUS)):
                    eventlist.append("K_MINUS")
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_EQUALS):
                    eventlist.append("K_EQUALS")
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP_PLUS):
                    eventlist.append("K_PLUS")
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
                    eventlist.append("K_r")
                if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_LCTRL) or (event.key == pygame.K_RCTRL)):
                    eventlist.append("K_CTRL")
                if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_LALT) or (event.key == pygame.K_RALT)):
                    eventlist.append("K_ALT")
            
            if ("K_ESCAPE" in eventlist) or ("QUIT" in eventlist):
                # Quit UI
                pygame.quit()
            
            if ("MOUSEBUTTONDOWN" in eventlist) and ("MOUSEBUTTONDOWN" not in last_eventlist):
                # The moment when the mouse is clicked on the button
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
                    
                if mouse_in >= 20 and mouse_in < 30:
                    self.yn_button_pressed[mouse_in - 20] = -self.yn_button_pressed[mouse_in - 20]
                    self.draw_init()
                    
                if mouse_in == -1 and self.draw_choose == 0:
                    moving_background = True
                    moving_background_start = mouse
                    moving_background_start_cx = self.cx
                    moving_background_start_cy = self.cy
                    
                if mouse_in == -1 and self.draw_choose == 1:
                    pass
            
            if moving_background:
                self.cx = mouse[0] - moving_background_start[0] + moving_background_start_cx
                self.cy = mouse[1] - moving_background_start[1] + moving_background_start_cy
                self.draw_init()
            
            if ("MOUSEMOTION" in eventlist):
                # Moving Mouse
                mouse_coordxprt = 'x = ' + numberform(self.cc2(mouse)[0])
                mouse_coordyprt = 'y = ' + numberform(self.cc2(mouse)[1])
                pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(2, 2, 122, 42))
                pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [2, 2, 122, 42], 1)
                self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(mouse_coordxprt , True , FIGURE_COLOR), (5, 5))
                self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(mouse_coordyprt , True , FIGURE_COLOR), (5, 25))
            
            if ("MOUSEBUTTONUP" in eventlist) and ("MOUSEBUTTONUP" not in last_eventlist):
                # The moment when the mouse is unclicked
                if moving_background:
                    moving_background = False
            
            if ("K_CTRL" in eventlist) and ("K_CTRL" not in last_eventlist):
                self.yn_button_pressed[0] = -self.yn_button_pressed[0]
                self.draw_init()
            if ("K_ALT" in eventlist) and ("K_ALT" not in last_eventlist):
                self.yn_button_pressed[1] = -self.yn_button_pressed[1]
                self.draw_init()
            
            if ("KEYDOWN" in eventlist) and ("KEYDOWN" not in last_eventlist) and (self.yn_button_pressed[0] == -1):
                
                if ("K_MINUS" in eventlist) and ("K_MINUS" not in last_eventlist):
                    # The moment when K_MINUS is pressed
                    RATIO = 5 / 6
                    self.r *= RATIO
                    self.cx = DRAW_WIDTH/2 + (self.cx - DRAW_WIDTH/2) * RATIO
                    self.cy = DRAW_HEIGHT/2 + (self.cy - DRAW_HEIGHT/2) * RATIO
                    self.draw_init()
                    
                if ("K_EQUALS" in eventlist) and ("K_EQUALS" not in last_eventlist):
                    # The moment when K_EQUALS is pressed
                    RATIO = 6 / 5
                    self.r *= RATIO
                    self.cx = DRAW_WIDTH/2 + (self.cx - DRAW_WIDTH/2) * RATIO
                    self.cy = DRAW_HEIGHT/2 + (self.cy - DRAW_HEIGHT/2) * RATIO
                    self.draw_init()
                
                if ("K_PLUS" in eventlist) and ("K_PLUS" not in last_eventlist):
                    # The moment when K_EQUALS is pressed
                    RATIO = 6 / 5
                    self.r *= RATIO
                    self.cx = DRAW_WIDTH/2 + (self.cx - DRAW_WIDTH/2) * RATIO
                    self.cy = DRAW_HEIGHT/2 + (self.cy - DRAW_HEIGHT/2) * RATIO
                    self.draw_init()
                
                if ("K_r" in eventlist) and ("K_r" not in last_eventlist):
                    # The moment when K_r is pressed
                    self.cx = DRAW_WIDTH / 2 + 0.01919810114514
                    self.cy = DRAW_HEIGHT / 2 + 0.01145141919810
                    self.r = (DRAW_WIDTH + DRAW_HEIGHT) / 9 + 0.114514 + 0.1919810 + ERROR
                    self.draw_init()
            
            last_eventlist = eventlist
            
            pygame.display.update()
        

c1 = GeomTool.Geom_object("c1", "Circle", None, None)
c1.getc((0,0,1))
c2 = GeomTool.Geom_object("c2", "Circle", None, None)
c2.getc((3,3,3.24))
c3 = GeomTool.Geom_object("c3", "Circle", None, None)
c3.getc((0.7,0.72,0.3))
l1 = GeomTool.Geom_object("l1", "Line", None, None)
l1.getc((-1,0,0))
l2 = GeomTool.Geom_object("l2", "Line", None, None)
l2.getc((0,-1,0))
l3 = GeomTool.Geom_object("l3", "Line", None, None)
l3.getc((2,3,2.5))
l4 = GeomTool.Geom_object("l4", "Line", None, None)
l4.getc((-1,1,0.3))
p1 = GeomTool.Geom_object("p1", "Point", None, None)
p1.getc((0,0))

geom_list = [c1, c2, c3, l1, l2, l3, l4, p1]
test = GeomUI(geom_list)
test.run()


