import pygame, tkinter
import GeomTool
import Explainer

"""
KEY_ESCAPE: Exit
KEY_r: Reset Zoom
KEY_MINUS: Zoom Out
KEY_EQUALS / KEY_PLUS: Zoom In
KEY_CONTROL: Start CMD
KEY_ALT: Print TAG
KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT: Move Screen
KEY_TAB: Full Screen

!!!
Test Choose Code involved
!!!

in CMD mode KEY_BACKSPACE: Backspace
in CMD mode KEY_SHIFT + KEY_BACKSPACE: Clearline

"""

ORIGINAL_SCREEN_WIDTH = 800
ORIGINAL_SCREEN_HEIGHT = 400
ORIGINAL_DRAW_WIDTH = 650
ORIGINAL_DRAW_HEIGHT = 400


BACKGROUND_COLOR = (244, 244, 244)

FIGURE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
PICKED_FIGURE_COLOR = (131, 251, 128)
CHOSEN_FIGURE_COLOR = (249, 176, 79)

BUTTON_COLOR_MID = (205, 228, 252)
BUTTON_COLOR_LIGHT = (220, 237, 254)
BUTTON_COLOR_DARK = (100, 164, 230)

TAG_COLOR = (237, 56, 115)

GEOM_PICK_DIST = 9.4
QUICK_CHOOSE_DIST = 4

# Geometry setting
ERROR = 1e-13

CMD_LINE_HEIGHT = 25

def choose_order_of_object(in_type):
    if in_type == "Line":
        return 1
    if in_type == "Circle":
        return 2
    if in_type == "Point":
        return 3
    return 0

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
            if  Disc >= -ERROR:
                Delta = fig1.c[1]**2 * (-(fig1.c[2] + fig1.c[0] * fig2.c[0] + fig1.c[1] * fig2.c[1])**2 + (fig1.c[0]**2 + fig1.c[1]**2) * fig2.c[2]**2)
                Delta = max(0, Delta)
                x1 = -((-fig1.c[1]**2 * fig2.c[0] + fig1.c[0] * (fig1.c[2] + fig1.c[1] * fig2.c[1]) + Delta ** (1/2))/(fig1.c[0]**2 + fig1.c[1]**2))
                x2 = -((-fig1.c[1]**2 * fig2.c[0] + fig1.c[0] * (fig1.c[2] + fig1.c[1] * fig2.c[1]) - Delta ** (1/2))/(fig1.c[0]**2 + fig1.c[1]**2))
                Delta = fig1.c[0]**2 * (-(fig1.c[2] + fig1.c[1] * fig2.c[1] + fig1.c[0] * fig2.c[0])**2 + (fig1.c[1]**2 + fig1.c[0]**2) * fig2.c[2]**2)
                Delta = max(0, Delta)
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
        
        root = tkinter.Tk()
        self.FULLWIDTH = root.winfo_screenwidth()
        self.FULLHEIGHT = root.winfo_screenheight()
        root.destroy()
        
        pygame.init()
        
        self.SCREEN_WIDTH = ORIGINAL_SCREEN_WIDTH
        self.SCREEN_HEIGHT = ORIGINAL_SCREEN_HEIGHT
        self.DRAW_WIDTH = ORIGINAL_DRAW_WIDTH
        self.DRAW_HEIGHT = ORIGINAL_DRAW_HEIGHT
        
        # self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((ORIGINAL_SCREEN_WIDTH, ORIGINAL_SCREEN_HEIGHT))
        pygame.display.set_caption('GeomUI')
        
        self.button_range = [(30, 100), (30, 150), (30, 200), (30, 250)]
        self.button_draw_fun = [self.draw_mouse_button, self.draw_point_button, self.draw_line_button, self.draw_circle_button]
        self.sub_button_range = []
        self.sub_button_draw_fun = []
        self.yn_button_range = [(30, 400), (30, 450), (30, 500)]
        self.yn_button_draw_fun = [self.draw_cmd_button, self.draw_tag_button, self.draw_fullscreen_button]
        self.yn_button_pressed = [-1, 1, -1]
        self.draw_choose = 0
        self.sub_draw_choose = -1
        
        self.cx = self.DRAW_WIDTH / 2 + 0.01919810114514
        self.cy = self.DRAW_HEIGHT / 2 + 0.01145141919810
        self.r = (self.DRAW_WIDTH + self.DRAW_HEIGHT) / 9 + 0.114514 + 0.1919810 + ERROR
        
        self.geom_list = in_geom_list # All geom objects
        self.geom_show = [_ for _ in range(len(in_geom_list))] # A True False sequence that show a geom object or not
        self.geom_chosen = [] # Chosen geom objects 0, >0
        self.geom_picked_list = []
        
        self.cmdlines = ["GeomToolKernel Version 1.0", "All rights reserved to Euclid", ""]
        self.cmdline_from = [0, 0, 1]
        self.CMD_SHOW_LINE = int((self.DRAW_HEIGHT - 80)/CMD_LINE_HEIGHT)
        self.CMD_LINE_CHAR = int((self.SCREEN_WIDTH - self.DRAW_WIDTH - 30) / 12)
    
    def choose_fig_list(self, mouse, allows = ("Point", "Line", "Circle")):
        # Choose a fig in geom_list that has geom_show
        out_fig_list = []
        for fig_num in range(len(self.geom_list)):
            if (fig_num in self.geom_show) and self.geom_list[fig_num].hasc and (self.geom_list[fig_num].type in allows):
                dist = self.geomdist(mouse, self.geom_list[fig_num].type, self.geom_list[fig_num].c)
                if dist < GEOM_PICK_DIST:
                    out_fig_list.append((fig_num, -choose_order_of_object(self.geom_list[fig_num].type) + dist/(2 * GEOM_PICK_DIST)))
        out_fig_list.sort(key = lambda x: x[1])
        return list(_[0] for _ in out_fig_list)
    
    def choose_fig1(self, mouse, allows = ("Point", "Line", "Circle")):
        # Choose a fig in geom_list that has geom_show
        lst = self.choose_fig_list(mouse, allows=allows)
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
                    outlst.append((_, self.geomdist(mouse, "Point", _[2]), _[2]))
            outlst.sort(key = lambda x: x[1])
            if len(outlst) > 0:
                self.geom_picked_list = [lst[outlst[0][0][0]], lst[outlst[0][0][1]]]
                if self.geom_list[lst[outlst[0][0][0]]].type != "Line" or self.geom_list[lst[outlst[0][0][1]]].type != "Line":
                    return outlst[0][2]
                else:
                    return None
            else:
                self.geom_picked_list = [lst[0]]
                return None
    
    def draw_fig(self):
        
        for fig_num in range(len(self.geom_list)):
            if (fig_num in self.geom_show) and self.geom_list[fig_num].hasc and self.geom_list[fig_num].type == 'Line':
                if (fig_num not in self.geom_chosen) and (fig_num not in self.geom_picked_list):
                    self.draw_line(self.geom_list[fig_num].c, FIGURE_COLOR, 2)
                if (fig_num in self.geom_chosen) and (fig_num not in self.geom_picked_list):
                    self.draw_line(self.geom_list[fig_num].c, CHOSEN_FIGURE_COLOR, 3)
                if (fig_num in self.geom_picked_list):
                    self.draw_line(self.geom_list[fig_num].c, PICKED_FIGURE_COLOR, 3)
        
        for fig_num in range(len(self.geom_list)):
            if (fig_num in self.geom_show) and self.geom_list[fig_num].hasc and self.geom_list[fig_num].type == 'Circle':
                if (fig_num not in self.geom_chosen) and (fig_num not in self.geom_picked_list):
                    self.draw_circle(self.geom_list[fig_num].c, FIGURE_COLOR, 2)
                if (fig_num in self.geom_chosen) and (fig_num not in self.geom_picked_list):
                    self.draw_circle(self.geom_list[fig_num].c, CHOSEN_FIGURE_COLOR, 3)
                if (fig_num in self.geom_picked_list):
                    self.draw_circle(self.geom_list[fig_num].c, PICKED_FIGURE_COLOR, 3)
                    
        for fig_num in range(len(self.geom_list)):
            if (fig_num in self.geom_show) and self.geom_list[fig_num].hasc and self.geom_list[fig_num].type == 'Point':
                if (fig_num not in self.geom_chosen) and (fig_num not in self.geom_picked_list):
                    self.draw_point(self.geom_list[fig_num].c, FIGURE_COLOR, 4)
                if (fig_num in self.geom_chosen) and (fig_num not in self.geom_picked_list):
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
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(2 + self.DRAW_WIDTH, 2, self.SCREEN_WIDTH - self.DRAW_WIDTH - 5, self.DRAW_HEIGHT - 5))
            pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [2 + self.DRAW_WIDTH, 2, self.SCREEN_WIDTH - self.DRAW_WIDTH - 5, self.DRAW_HEIGHT - 5], 1)
            textlist = []
            for line_num in range(len(self.cmdlines)):
                linetext = ('>>> ' if self.cmdline_from[line_num] == 1 else 'GT: ') + self.cmdlines[line_num] + ('|' if line_num == len(self.cmdlines) - 1 else '')
                newline = True
                while len(linetext) > 0:
                    textlist.append(('    ' if (not newline) else '') + (linetext[:self.CMD_LINE_CHAR - 4]) if (not newline) else linetext[:self.CMD_LINE_CHAR])
                    linetext = (linetext[self.CMD_LINE_CHAR - 4:]) if (not newline) else linetext[self.CMD_LINE_CHAR:]
                    newline = False
            line_num = 0
            for linetext in textlist[-self.CMD_SHOW_LINE:]:
                self.screen.blit(pygame.font.SysFont('Consolas', 20, bold=False).render(linetext , True , TEXT_COLOR), (12 + self.DRAW_WIDTH, line_num * CMD_LINE_HEIGHT + 12))
                line_num += 1


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
        
    def draw_abis_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-10, height-5), (width+10, height-5), width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-10, height-5), (width+10, height-10), width=2)
        pygame.draw.line(self.screen, BUTTON_COLOR_DARK, (width-10, height-5), (width+10, height-16), width=2)
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("abis" , True , BUTTON_COLOR_DARK), (width-15, height))
    
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
        
    def draw_fullscreen_button(self, width, height, pressed):
        # pressed = -1, 0, 1
        if pressed == 1:
            pygame.draw.rect(self.screen, BUTTON_COLOR_MID, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == -1:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(width - 20, height - 20, 40, 40))
        if pressed == 0:
            pygame.draw.rect(self.screen, BUTTON_COLOR_LIGHT, pygame.Rect(width - 20, height - 20, 40, 40))
        pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [width - 20, height - 20, 40, 40], 1)
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("full" , True , BUTTON_COLOR_DARK), (width-13, height-15))
        self.screen.blit(pygame.font.SysFont('Corbel', 18, bold=True).render("scrn" , True , BUTTON_COLOR_DARK), (width-15, height))
    
    # Functions to draw Geometric Figures
    
    def draw_point(self, c, color, width):
        realc = self.cc(c)
        pygame.draw.circle(self.screen, color, center=realc, radius=width, width=width)
        
    def draw_line(self, c, color, width):
        if abs(c[0]) < ERROR:
            ht = self.cc((0, -c[2]/c[1]))[1]
            point1 = (0, ht)
            point2 = (self.SCREEN_WIDTH, ht)
        else:
            if abs(c[1]) < ERROR:
                wd = self.cc((-c[2]/c[0], 0))[0]
                point1 = (wd, 0)
                point2 = (wd, self.SCREEN_HEIGHT)
            else:
                lf = self.cc2((0, 0))[0]
                rt = self.cc2((self.SCREEN_WIDTH, 0))[0]
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
        
    def cmd_clearline(self, line_num):
        self.cmdlines[line_num] = ''
        self.load_chosen_and_mode_from_cmdline(line_num)
        
    def load_chosen_and_mode_from_cmdline(self, line_num):
        exp = Explainer.ExplainLine(self.cmdlines[line_num], self.geom_list)
        self.geom_chosen = exp.geom_appear
        self.cmd_modechange(exp.mode_appear)
        self.draw_init()
        
    def cmd_modenamechangeline(self, line_num, mode_name, mode_list = ["mdpt", "pt", "line", "para", "perp", "pbis", "abis", "circ"]):
        if mode_name in mode_list:
            self.cmdlines[line_num] = mode_name + ' '
        else:
            self.cmdlines[line_num] = ''
        self.load_chosen_and_mode_from_cmdline(line_num)
        
        '''
        success = False
        for change_name in mode_list:
            if change_name + " " in self.cmdlines[line_num]:
                self.cmdlines[line_num] = self.cmdlines[line_num].replace(change_name + " ", mode_name + " " if mode_name != "" else "")
                success = True
                break
        if not success:
            self.cmdlines[line_num] += mode_name + " " if mode_name != "" else ""
        '''
    
    def cmd_modechange(self, mode_name):
        if mode_name == "pt":
            self.draw_choose = 1
            self.sub_draw_choose = -1
        elif mode_name == "mdpt":
            self.draw_choose = 1
            self.sub_draw_choose = 0
        elif mode_name == "line":
            self.draw_choose = 2
            self.sub_draw_choose = -1
        elif mode_name == "para":
            self.draw_choose = 2
            self.sub_draw_choose = 0
        elif mode_name == "perp":
            self.draw_choose = 2
            self.sub_draw_choose = 1
        elif mode_name == "pbis":
            self.draw_choose = 2
            self.sub_draw_choose = 2
        elif mode_name == "abis":
            self.draw_choose = 2
            self.sub_draw_choose = 3
        elif mode_name == "circ":
            self.draw_choose = 3
            self.sub_draw_choose = -1
        else:
            self.draw_choose = 0
            self.sub_draw_choose = -1
            
        # update buttons
        if self.draw_choose == 0:
            self.sub_button_range = []
            self.sub_button_draw_fun = []
        
        if self.draw_choose == 1:
            self.sub_button_range = [(80, 100)]
            self.sub_button_draw_fun = [self.draw_mdpt_button]
            
        if self.draw_choose == 2:
            self.sub_button_range = [(80, 100), (80, 150), (80, 200), (80, 250)]
            self.sub_button_draw_fun = [self.draw_para_button, self.draw_perp_button, self.draw_pbis_button, self.draw_abis_button]
            
        if self.draw_choose == 3:
            self.sub_button_range = []
            self.sub_button_draw_fun = []

    def get_eventlist(self):
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
            if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_RETURN) or (event.key == pygame.K_KP_ENTER)):
                eventlist.append("K_ENTER")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_BACKSPACE):
                eventlist.append("K_BACKSPACE")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_TAB):
                eventlist.append("K_TAB")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                eventlist.append("K_ ")
            if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_MINUS) or (event.key == pygame.K_KP_MINUS)):
                eventlist.append("K_-")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_EQUALS):
                eventlist.append("K_=")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP_PLUS):
                eventlist.append("K_+")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_a):
                eventlist.append("K_a")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_b):
                eventlist.append("K_b")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_c):
                eventlist.append("K_c")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_d):
                eventlist.append("K_d")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_e):
                eventlist.append("K_e")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_f):
                eventlist.append("K_f")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_g):
                eventlist.append("K_g")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_h):
                eventlist.append("K_h")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_i):
                eventlist.append("K_i")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_j):
                eventlist.append("K_j")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_k):
                eventlist.append("K_k")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_l):
                eventlist.append("K_l")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m):
                eventlist.append("K_m")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_n):
                eventlist.append("K_n")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_o):
                eventlist.append("K_o")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_p):
                eventlist.append("K_p")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_q):
                eventlist.append("K_q")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
                eventlist.append("K_r")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_s):
                eventlist.append("K_s")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_t):
                eventlist.append("K_t")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_u):
                eventlist.append("K_u")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_v):
                eventlist.append("K_v")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_w):
                eventlist.append("K_w")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_x):
                eventlist.append("K_x")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_y):
                eventlist.append("K_y")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_z):
                eventlist.append("K_z")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_1):
                eventlist.append("K_1")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_2):
                eventlist.append("K_2")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_3):
                eventlist.append("K_3")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_4):
                eventlist.append("K_4")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_5):
                eventlist.append("K_5")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_6):
                eventlist.append("K_6")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_7):
                eventlist.append("K_7")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_8):
                eventlist.append("K_8")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_9):
                eventlist.append("K_9")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_0):
                eventlist.append("K_0")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP1):
                eventlist.append("K_1")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP2):
                eventlist.append("K_2")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP3):
                eventlist.append("K_3")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP4):
                eventlist.append("K_4")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP5):
                eventlist.append("K_5")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP6):
                eventlist.append("K_6")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP7):
                eventlist.append("K_7")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP8):
                eventlist.append("K_8")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP9):
                eventlist.append("K_9")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP0):
                eventlist.append("K_0")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_PERIOD):
                eventlist.append("K_.")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP_PERIOD):
                eventlist.append("K_.")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_COMMA):
                eventlist.append("K_,")
            if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_LCTRL) or (event.key == pygame.K_RCTRL)):
                eventlist.append("K_CTRL")
            if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_LALT) or (event.key == pygame.K_RALT)):
                eventlist.append("K_ALT")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_UP):
                eventlist.append("K_UP")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_DOWN):
                eventlist.append("K_DOWN")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT):
                eventlist.append("K_LEFT")
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT):
                eventlist.append("K_RIGHT")
            if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_LSHIFT) or (event.key == pygame.K_RSHIFT)):
                self.shifted = True
            if (event.type == pygame.KEYUP) and ((event.key == pygame.K_LSHIFT) or (event.key == pygame.K_RSHIFT)):
                self.shifted = False
        
        if self.shifted and ("K_BACKSPACE" in eventlist):
            eventlist.remove("K_BACKSPACE")
            eventlist.append("CLEARCMDLINE")
        if self.shifted and ("K_1" in eventlist):
            eventlist.remove("K_1")
            eventlist.append("K_!")
        if self.shifted and ("K_2" in eventlist):
            eventlist.remove("K_2")
            eventlist.append("K_@")
        if self.shifted and ("K_3" in eventlist):
            eventlist.remove("K_3")
            eventlist.append("K_#")
        if self.shifted and ("K_4" in eventlist):
            eventlist.remove("K_4")
            eventlist.append("K_$")
        if self.shifted and ("K_5" in eventlist):
            eventlist.remove("K_5")
            eventlist.append("K_%")
        if self.shifted and ("K_6" in eventlist):
            eventlist.remove("K_6")
            eventlist.append("K_^")
        if self.shifted and ("K_7" in eventlist):
            eventlist.remove("K_7")
            eventlist.append("K_&")
        if self.shifted and ("K_8" in eventlist):
            eventlist.remove("K_8")
            eventlist.append("K_*")
        if self.shifted and ("K_9" in eventlist):
            eventlist.remove("K_9")
            eventlist.append("K_(")
        if self.shifted and ("K_0" in eventlist):
            eventlist.remove("K_0")
            eventlist.append("K_)")
        if self.shifted and ("K_-" in eventlist):
            eventlist.remove("K_-")
            eventlist.append("K__")
        if self.shifted and ("K_=" in eventlist):
            eventlist.remove("K_=")
            eventlist.append("K_+")
        if self.shifted and ("K_," in eventlist):
            eventlist.remove("K_,")
            eventlist.append("K_<")
        if self.shifted and ("K_." in eventlist):
            eventlist.remove("K_.")
            eventlist.append("K_>")
        if self.shifted and ("K_a" in eventlist):
            eventlist.remove("K_a")
            eventlist.append("K_A")
        if self.shifted and ("K_b" in eventlist):
            eventlist.remove("K_b")
            eventlist.append("K_B")
        if self.shifted and ("K_c" in eventlist):
            eventlist.remove("K_c")
            eventlist.append("K_C")
        if self.shifted and ("K_d" in eventlist):
            eventlist.remove("K_d")
            eventlist.append("K_D")
        if self.shifted and ("K_e" in eventlist):
            eventlist.remove("K_e")
            eventlist.append("K_E")
        if self.shifted and ("K_f" in eventlist):
            eventlist.remove("K_f")
            eventlist.append("K_F")
        if self.shifted and ("K_g" in eventlist):
            eventlist.remove("K_g")
            eventlist.append("K_G")
        if self.shifted and ("K_h" in eventlist):
            eventlist.remove("K_h")
            eventlist.append("K_H")
        if self.shifted and ("K_i" in eventlist):
            eventlist.remove("K_i")
            eventlist.append("K_I")
        if self.shifted and ("K_j" in eventlist):
            eventlist.remove("K_j")
            eventlist.append("K_J")
        if self.shifted and ("K_k" in eventlist):
            eventlist.remove("K_k")
            eventlist.append("K_K")
        if self.shifted and ("K_l" in eventlist):
            eventlist.remove("K_l")
            eventlist.append("K_L")
        if self.shifted and ("K_m" in eventlist):
            eventlist.remove("K_m")
            eventlist.append("K_M")
        if self.shifted and ("K_n" in eventlist):
            eventlist.remove("K_n")
            eventlist.append("K_N")
        if self.shifted and ("K_o" in eventlist):
            eventlist.remove("K_o")
            eventlist.append("K_O")
        if self.shifted and ("K_p" in eventlist):
            eventlist.remove("K_p")
            eventlist.append("K_P")
        if self.shifted and ("K_q" in eventlist):
            eventlist.remove("K_q")
            eventlist.append("K_Q")
        if self.shifted and ("K_r" in eventlist):
            eventlist.remove("K_r")
            eventlist.append("K_R")
        if self.shifted and ("K_s" in eventlist):
            eventlist.remove("K_s")
            eventlist.append("K_S")
        if self.shifted and ("K_t" in eventlist):
            eventlist.remove("K_t")
            eventlist.append("K_T")
        if self.shifted and ("K_u" in eventlist):
            eventlist.remove("K_u")
            eventlist.append("K_U")
        if self.shifted and ("K_v" in eventlist):
            eventlist.remove("K_v")
            eventlist.append("K_V")
        if self.shifted and ("K_w" in eventlist):
            eventlist.remove("K_w")
            eventlist.append("K_W")
        if self.shifted and ("K_x" in eventlist):
            eventlist.remove("K_x")
            eventlist.append("K_X")
        if self.shifted and ("K_y" in eventlist):
            eventlist.remove("K_y")
            eventlist.append("K_Y")
        if self.shifted and ("K_z" in eventlist):
            eventlist.remove("K_z")
            eventlist.append("K_Z")
            
        return eventlist
        
        # print(eventlist)


    def run(self):
        self.draw_init()
        last_mouse_in = -1
        last_eventlist = []
        moving_background = False
        last_moving_background = False
        self.shifted = False
        cvalue = None
        
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
                
                # Picking Geometric Figures but depend on the draw_choose mode
                if self.draw_choose == 1:
                    cvalue = self.choose_fig2(mouse)
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
                        
                        
                '''-----------------------------------------------------------------
                
                                  Item Picking announcement:                        
                
                
                This is only a choose Test! Only Testing Circle and Line picks      
                In later versions, these chooses depend on cmdlines   !!!!!!!!!!!!!!
                
                -----------------------------------------------------------------'''
                
                if self.draw_choose == 2:
                    self.choose_fig1(mouse, "Line")
                    if len(self.geom_picked_list) == 0:
                        mouse_in = -1
                    else:
                        mouse_in = self.geom_picked_list[0] + 100
                if self.draw_choose == 3:
                    self.choose_fig1(mouse, "Circle")
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
            
            eventlist = self.get_eventlist()
                    
            
            if ("K_ESCAPE" in eventlist) or ("QUIT" in eventlist):
                # Quit UI
                pygame.quit()
            
            if ("MOUSEBUTTONDOWN" in eventlist) and ("MOUSEBUTTONDOWN" not in last_eventlist):
                # The moment when the mouse is clicked on the button
                if mouse_in >= 0 and mouse_in < 10:
                    self.draw_choose = mouse_in
                    self.sub_draw_choose = -1
                    
                    if mouse_in == 0:
                        self.cmd_modenamechangeline(-1, "")
                    
                    if mouse_in == 1:
                        self.cmd_modenamechangeline(-1, "pt")
                        
                    if mouse_in == 2:
                        self.cmd_modenamechangeline(-1, "line")
                        
                    if mouse_in == 3:
                        self.cmd_modenamechangeline(-1, "circ")
                    
                    
                    
                    '''
                    --- Test Choose Code ---
                    '''
                    self.load_chosen_and_mode_from_cmdline(-1)
                    
                    
                    
                    self.draw_init()
                    
                if mouse_in >= 10 and mouse_in < 20:
                    self.sub_draw_choose = mouse_in - 10
                    
                    if self.draw_choose == 1 and mouse_in == 10:
                        self.cmd_modenamechangeline(-1, "mdpt")
                    if self.draw_choose == 2 and mouse_in == 10:
                        self.cmd_modenamechangeline(-1, "para")
                    if self.draw_choose == 2 and mouse_in == 11:
                        self.cmd_modenamechangeline(-1, "perp")
                    if self.draw_choose == 2 and mouse_in == 12:
                        self.cmd_modenamechangeline(-1, "pbis")
                    if self.draw_choose == 2 and mouse_in == 13:
                        self.cmd_modenamechangeline(-1, "abis")
                    
                    self.draw_init()
                    
                if mouse_in >= 20 and mouse_in < 30:
                    self.yn_button_pressed[mouse_in - 20] = -self.yn_button_pressed[mouse_in - 20]
                    
                    if mouse_in - 20 == 2 and self.yn_button_pressed[2] == 1:
                        self.SCREEN_WIDTH = self.FULLWIDTH
                        self.SCREEN_HEIGHT = self.FULLHEIGHT
                        self.CMD_SHOW_LINE = int((self.DRAW_HEIGHT - 60)/CMD_LINE_HEIGHT)
                        self.CMD_LINE_CHAR = int((self.SCREEN_WIDTH - self.DRAW_WIDTH - 30) / 12)
                        pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
                    if mouse_in - 20 == 2 and self.yn_button_pressed[2] == -1:
                        self.SCREEN_WIDTH = ORIGINAL_SCREEN_WIDTH
                        self.SCREEN_HEIGHT = ORIGINAL_SCREEN_HEIGHT
                        self.CMD_SHOW_LINE = int((self.DRAW_HEIGHT - 60)/CMD_LINE_HEIGHT)
                        self.CMD_LINE_CHAR = int((self.SCREEN_WIDTH - self.DRAW_WIDTH - 30) / 12)
                        pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                    
                    self.draw_init()
                    
                if mouse_in == -1 and self.draw_choose == 0:
                    moving_background = True
                    moving_background_start = mouse
                    moving_background_start_cx = self.cx
                    moving_background_start_cy = self.cy
                    
                    
                
                
                
                '''
                --- Test Choose Code ---
                '''
                if 100 <= mouse_in < 1000:
                    self.cmdlines[-1] += self.geom_list[mouse_in - 100].name + ' '
                    self.load_chosen_and_mode_from_cmdline(-1)
                if mouse_in > 1000:
                    fig1 = (mouse_in % 1000)
                    fig2 = round((mouse_in - fig1) / 1000)
                    self.cmdlines[-1] += self.geom_list[fig1 - 100].name + ' '
                    self.cmdlines[-1] += self.geom_list[fig2 - 100].name + ' '
                    if cvalue != None:
                        self.cmdlines[-1] += str(cvalue[0]) + ' ' + str(cvalue[1]) + ' '
                    self.load_chosen_and_mode_from_cmdline(-1)
                
            
            
            if moving_background:
                self.cx = mouse[0] - moving_background_start[0] + moving_background_start_cx
                self.cy = mouse[1] - moving_background_start[1] + moving_background_start_cy
                self.draw_init()
            
            
            
            '''
            --- Test Choose Code ---
            '''
            if last_moving_background and (not moving_background) and (mouse[0] - moving_background_start[0])**2 + (mouse[1] - moving_background_start[1])**2 < QUICK_CHOOSE_DIST**2:
                self.cmd_clearline(-1)
            last_moving_background = moving_background
            
            
            
            if ("MOUSEMOTION" in eventlist):
                # Moving Mouse
                mouse_coordxprt = 'x = ' + numberform(self.cc2(mouse)[0])
                mouse_coordyprt = 'y = ' + numberform(self.cc2(mouse)[1])
                if len(self.geom_picked_list) == 0:
                    pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(2, 2, 138, 42))
                    pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [2, 2, 138, 42], 1)
                    self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(mouse_coordxprt , True , TEXT_COLOR), (5, 5))
                    self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(mouse_coordyprt , True , TEXT_COLOR), (5, 25))
                if len(self.geom_picked_list) > 0:
                    pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(2, 2, 138, 62))
                    pygame.draw.rect(self.screen, BUTTON_COLOR_DARK, [2, 2, 138, 62], 1)
                    self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(mouse_coordxprt , True , TEXT_COLOR), (5, 5))
                    self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(mouse_coordyprt , True , TEXT_COLOR), (5, 25))
                    self.screen.blit(pygame.font.SysFont('Consolas', 15, bold=False).render(", ".join([self.geom_list[_].name for _ in self.geom_picked_list]) , True , TEXT_COLOR), (5, 45))
            
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
            if ("K_TAB" in eventlist) and ("K_TAB" not in last_eventlist):
                self.yn_button_pressed[2] = -self.yn_button_pressed[2]
                if self.yn_button_pressed[2] == 1:
                    self.SCREEN_WIDTH = self.FULLWIDTH
                    self.SCREEN_HEIGHT = self.FULLHEIGHT
                    self.CMD_SHOW_LINE = int((self.DRAW_HEIGHT - 60)/CMD_LINE_HEIGHT)
                    self.CMD_LINE_CHAR = int((self.SCREEN_WIDTH - self.DRAW_WIDTH - 30) / 12)
                    pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
                if self.yn_button_pressed[2] == -1:
                    self.SCREEN_WIDTH = ORIGINAL_SCREEN_WIDTH
                    self.SCREEN_HEIGHT = ORIGINAL_SCREEN_HEIGHT
                    self.CMD_SHOW_LINE = int((self.DRAW_HEIGHT - 60)/CMD_LINE_HEIGHT)
                    self.CMD_LINE_CHAR = int((self.SCREEN_WIDTH - self.DRAW_WIDTH - 30) / 12)
                    pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                self.draw_init()
            
            
            
            if ("KEYDOWN" in eventlist) and ("KEYDOWN" not in last_eventlist) and (self.yn_button_pressed[0] == 1):
                for event in eventlist:
                    if len(event) == 3:
                        self.cmdlines[-1] += event[-1]
                        self.load_chosen_and_mode_from_cmdline(-1)
                    if event == "K_BACKSPACE":
                        self.cmdlines[-1] = self.cmdlines[-1][:-1]
                        self.load_chosen_and_mode_from_cmdline(-1)
                    if event == "CLEARCMDLINE":
                        self.cmd_clearline(-1)
                    if event == "K_ENTER":
                        self.cmdlines.append("")
                        
                        '''
                        Need to wait for Kernel Corespond !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        '''
                        
                        self.cmdline_from.append(1)
                        self.cmd_clearline(-1)
                        
            
                
            if ("KEYDOWN" in eventlist) and ("KEYDOWN" not in last_eventlist) and (self.yn_button_pressed[0] == -1):
                
                if ("K_-" in eventlist) and ("K_-" not in last_eventlist):
                    # The moment when K_MINUS is pressed
                    RATIO = 5 / 6
                    self.r *= RATIO
                    self.cx = self.DRAW_WIDTH/2 + (self.cx - self.DRAW_WIDTH/2) * RATIO
                    self.cy = self.DRAW_HEIGHT/2 + (self.cy - self.DRAW_HEIGHT/2) * RATIO
                    self.draw_init()
                    
                if ("K_=" in eventlist) and ("K_=" not in last_eventlist):
                    # The moment when K_EQUALS is pressed
                    RATIO = 6 / 5
                    self.r *= RATIO
                    self.cx = self.DRAW_WIDTH/2 + (self.cx - self.DRAW_WIDTH/2) * RATIO
                    self.cy = self.DRAW_HEIGHT/2 + (self.cy - self.DRAW_HEIGHT/2) * RATIO
                    self.draw_init()
                
                if ("K_+" in eventlist) and ("K_+" not in last_eventlist):
                    # The moment when K_EQUALS is pressed
                    RATIO = 6 / 5
                    self.r *= RATIO
                    self.cx = self.DRAW_WIDTH/2 + (self.cx - self.DRAW_WIDTH/2) * RATIO
                    self.cy = self.DRAW_HEIGHT/2 + (self.cy - self.DRAW_HEIGHT/2) * RATIO
                    self.draw_init()
                
                if ("K_r" in eventlist) and ("K_r" not in last_eventlist):
                    # The moment when K_r is pressed
                    self.cx = self.DRAW_WIDTH / 2 + 0.01919810114514
                    self.cy = self.DRAW_HEIGHT / 2 + 0.01145141919810
                    self.r = (self.DRAW_WIDTH + self.DRAW_HEIGHT) / 9 + 0.114514 + 0.1919810 + ERROR
                    self.draw_init()
                    
                if ("K_RIGHT" in eventlist) and ("K_RIGHT" not in last_eventlist):
                    RATIO = 1/7
                    self.cx -= self.DRAW_WIDTH * RATIO
                    self.draw_init()
                if ("K_LEFT" in eventlist) and ("K_LEFT" not in last_eventlist):
                    RATIO = 1/7
                    self.cx += self.DRAW_WIDTH * RATIO
                    self.draw_init()
                if ("K_UP" in eventlist) and ("K_UP" not in last_eventlist):
                    RATIO = 1/7
                    self.cy += self.DRAW_HEIGHT * RATIO
                    self.draw_init()
                if ("K_DOWN" in eventlist) and ("K_DOWN" not in last_eventlist):
                    RATIO = 1/7
                    self.cy -= self.DRAW_HEIGHT * RATIO
                    self.draw_init()
            
            last_eventlist = eventlist
            
            pygame.display.update()
        
if __name__ == "__main__":
    c1 = GeomTool.Geom_object("c1", "Circle", None, None)
    c1.getc((0,0,1))
    c2 = GeomTool.Geom_object("c2", "Circle", None, None)
    c2.getc((3,3,3.24))
    c3 = GeomTool.Geom_object("c3", "Circle", None, None)
    c3.getc((0.7,0.7,0.3))
    c4 = GeomTool.Geom_object("c4", "Circle", None, None)
    c4.getc((-0.8,-0.4,2.3))
    l1 = GeomTool.Geom_object("l1", "Line", None, None)
    l1.getc((-1,0,0))
    l2 = GeomTool.Geom_object("l2", "Line", None, None)
    l2.getc((0,-1,0))
    l3 = GeomTool.Geom_object("l3", "Line", None, None)
    l3.getc((2,3,2.5))
    l4 = GeomTool.Geom_object("l4", "Line", None, None)
    l4.getc((-1,1,0.3))
    l5 = GeomTool.Geom_object("l5", "Line", None, None)
    l5.getc((-1,0.1,0.5))
    l6 = GeomTool.Geom_object("l6", "Line", None, None)
    l6.getc((0.6,0.8,1))
    l7 = GeomTool.Geom_object("l7", "Line", None, None)
    l7.getc((-1,0,1))
    l8 = GeomTool.Geom_object("l8", "Line", None, None)
    l8.getc((0,-1,1))
    p1 = GeomTool.Geom_object("p1", "Point", None, None)
    p1.getc((0,0))
    p2 = GeomTool.Geom_object("p2", "Point", None, None)
    p2.getc((1,1))
    p3 = GeomTool.Geom_object("p3", "Point", None, None)
    p3.getc((0.7,0.5))
    p4 = GeomTool.Geom_object("p4", "Point", None, None)
    p4.getc((0.6,0.8))

    geom_list = [c1, c2, c3, c4, l1, l2, l3, l4, l5, l6, l7, l8, p1, p2, p3, p4]
    test = GeomUI(geom_list)
    test.run()


