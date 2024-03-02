import GeomTool

'''
eqinfo: eq points, lines, circles
colinfo: colinear
cycinfo: cyclic

length_ratio_info: |AB|/|CD| and 1/4, 1/3, 2/5, 1/2, 1/sqrt(3), 3/5, 2/3, 1/sqrt(2), 3/4, 1, 4/3, sqrt(2), 3/2, 5/3, sqrt(3), 2, 5/2, 3, 4
angle_eq_info: arccos<AB, CD> and 0, ±15, ±22.5, ±30, ±45, ±60, ±67.5, ±75, 90
simtri: complex_number((C-A)/(B-A)) and conjugate


'''

CHECK_ERROR = 10

def rnd(x):
    return round(x, CHECK_ERROR)

def objchecklist(in_list, fun):
    outdict = dict()
    for obj in in_list:
        key = fun(obj)
        if key in outdict:
            outdict[key].append(obj)
        else:
            outdict[key] = [obj]
    return list(outdict.values())


def printchecklist(in_list, fun=lambda x: x.name):
    outstr = ""
    for sublst in in_list:
        if len(sublst) > 1:
            for obj in sublst:
                outstr += fun(obj) + " = "
            outstr = outstr[:-3] + ", "
    if outstr != '':
        return outstr[:-2]
    else:
        return "None"

def difflist(in_list):
    return [_[0] for _ in in_list]

def stdlinec(in_c):
    c0 = (rnd(in_c[0] / (in_c[0] **2 + in_c[1] **2) **(1/2)), rnd(in_c[1] / (in_c[0] **2 + in_c[1] **2) **(1/2)), rnd(in_c[2] / (in_c[0] **2 + in_c[1] **2) **(1/2)))
    if abs(c0[0]) < 10 ** -CHECK_ERROR:
        if c0[1] > 0:
            return c0
        else:
            return (rnd(-c0[0]), rnd(-c0[1]), rnd(-c0[2]))
    elif c0[0] > 0:
        return c0
    else:
        return (rnd(-c0[0]), rnd(-c0[1]), rnd(-c0[2]))

class GeomInformation:
    # Get Geometric Informations from c
    def __init__(self, in_graph_tree):
        self.tree = in_graph_tree
        self.visible_list = in_graph_tree.get_visible()
        points = []
        lines = []
        circles = []
        for obj in self.visible_list:
            if obj.type == "Point" and obj.hasc:
                points.append(obj)
            if obj.type == "Line" and obj.hasc:
                lines.append(obj)
            if obj.type == "Circle" and obj.hasc:
                circles.append(obj)
                
        self.points_checklist = objchecklist(points, lambda obj: (rnd(obj.c[0]), rnd(obj.c[1])))
        self.lines_checklist = objchecklist(lines, lambda obj: stdlinec(obj.c))
        self.circles_checklist = objchecklist(circles, lambda obj: (rnd(obj.c[0]), rnd(obj.c[1]), rnd(obj.c[2])))
        self.points = difflist(self.points_checklist)
        self.lines = difflist(self.lines_checklist)
        self.circles = difflist(self.circles_checklist)
        
    def eqinfo(self):
        return "Points: " + printchecklist(self.points_checklist) + "; Lines: " + printchecklist(self.lines_checklist) + "; Circles: " + printchecklist(self.circles_checklist)
    
    def dist_info(self):
        dist_dict = dict()
        for pt_num1 in range(len(self.points)):
            for pt_num2 in range(pt_num1 + 1, len(self.points)):
                pt1 = self.points[pt_num1]
                pt2 = self.points[pt_num2]
                d0 = rnd(((pt1.c[0] - pt2.c[0]) ** 2 + (pt1.c[1] - pt2.c[1]) ** 2) **(1/2))
                if d0 in dist_dict:
                    dist_dict[d0].append((pt_num1, pt_num2))
                else:
                    dist_dict[d0] = [(pt_num1, pt_num2)]
        self.dist_dict = dist_dict
        return printchecklist(self.dist_dict.values(), lambda x: "|" + self.points[x[0]].name + " " + self.points[x[1]].name + "|")
        
    
    def colinfo(self):
        colinear_dict = dict()
        for pt_num1 in range(len(self.points)):
            for pt_num2 in range(pt_num1 + 1, len(self.points)):
                pt1 = self.points[pt_num1]
                pt2 = self.points[pt_num2]
                c0 = stdlinec((pt1.c[1] - pt2.c[1], pt2.c[0] - pt1.c[0], pt1.c[0] * pt2.c[1] - pt2.c[0] * pt1.c[1]))
                if c0 in colinear_dict:
                    colinear_dict[c0] = colinear_dict[c0].union({pt_num1, pt_num2})
                else:
                    colinear_dict[c0] = {pt_num1, pt_num2}
        self.colinear_list = [[self.points[num] for num in st] for st in colinear_dict.values()]
        outstr = ''
        for sublst in self.colinear_list:
            if len(sublst) > 2:
                outstr += "line "
                for obj in sublst:
                    outstr += obj.name + " "
                outstr = outstr[:-1] + ", "
        if outstr != '':
            return outstr[:-2]
        else:
            return "None"
