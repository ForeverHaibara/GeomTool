'''
eqinfo: eq points, lines, circles
colinfo: colinear
cycinfo: cyclic

length_ratio_info: |AB|/|CD| and 1/4, 1/3, 1/2, 1/sqrt(3), 2/3, 1/sqrt(2), 3/4, sqrt(2/3), 1, sqrt(3/2), 4/3, sqrt(2), 3/2, sqrt(3), 2, 3, 4
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


def printchecklist(in_list, fun=lambda x: x.name, midsymbol="=", midsymbol2=", "):
    outstr = ""
    for sublst in in_list:
        if len(sublst) > 1:
            for obj in sublst:
                outstr += fun(obj) + " " + midsymbol + " "
            outstr = outstr[:-3] + midsymbol2
    if outstr != '':
        return outstr[:-len(midsymbol2)]
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

def complexdiv(x1, y1, x2, y2):
    sq = x2 ** 2 + y2 ** 2
    return ((x1 * x2 + y1 * y2) / sq, (x2 * y1 - x1 * y2) / sq)

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
        
    def eq(self):
        return "Points: " + printchecklist(self.points_checklist) + "\nLines: " + printchecklist(self.lines_checklist) + "\nCircles: " + printchecklist(self.circles_checklist)
    
    def deq(self):
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
        return printchecklist(self.dist_dict.values(), lambda x: "|" + self.points[x[0]].name + " " + self.points[x[1]].name + "|", midsymbol2='\n')
    
    def col(self):
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
        self.colinear_dict = colinear_dict
        self.colinear_list = [[self.points[num] for num in st] for st in colinear_dict.values()]
        outstr = ''
        for sublst in self.colinear_list:
            if len(sublst) > 2:
                outstr += "Line "
                for obj in sublst:
                    outstr += obj.name + " "
                outstr = outstr[:-1] + ", "
        if outstr != '':
            return outstr[:-2]
        else:
            return "None"
        
        
    def cyc(self):
        cyclic_dict = dict()
        for pt_num1 in range(len(self.points)):
            for pt_num2 in range(pt_num1 + 1, len(self.points)):
                for pt_num3 in range(pt_num2 + 1, len(self.points)):
                    x1 = self.points[pt_num1].c[0]
                    x2 = self.points[pt_num2].c[0]
                    x3 = self.points[pt_num3].c[0]
                    y1 = self.points[pt_num1].c[1]
                    y2 = self.points[pt_num2].c[1]
                    y3 = self.points[pt_num3].c[1]
                    d0 = (x2 * y1 - x3 * y1 - x1 * y2 + x3 * y2 + x1 * y3 - x2 * y3)
                    if abs(d0) >= 10 ** -CHECK_ERROR:
                        x0 = (x2**2 * y1 - x3**2 * y1 - x1**2 * y2 + x3**2 * y2 - y1**2 * y2 + y1 * y2**2 + x1**2 * y3 - x2**2 * y3 + y1**2 * y3 - y2**2 * y3 - y1 * y3**2 + y2 * y3**2)/(2 * d0)
                        y0 = (x1**2 * x2 - x1 * x2**2 - x1**2 * x3 + x2**2 * x3 + x1 * x3**2 - x2 * x3**2 + x2 * y1**2 - x3 * y1**2 - x1 * y2**2 + x3 * y2**2 + x1 * y3**2 - x2 * y3**2)/(2 * d0)
                        r0 = (((x1 - x2)**2 + (y1 - y2)**2) * ((x1 - x3)**2 + (y1 - y3)**2) * ((x2 - x3)**2 + (y2 - y3)**2))** (1/2) / abs(2 * d0)
                        c0 = (rnd(x0), rnd(y0), rnd(r0))
                        if c0 in cyclic_dict:
                            cyclic_dict[c0] = cyclic_dict[c0].union({pt_num1, pt_num2, pt_num3})
                        else:
                            cyclic_dict[c0] = {pt_num1, pt_num2, pt_num3}
        self.cyclic_list = [[self.points[num] for num in st] for st in cyclic_dict.values()]
        outstr = ''
        for sublst in self.cyclic_list:
            if len(sublst) > 3:
                outstr += "Circle "
                for obj in sublst:
                    outstr += obj.name + " "
                outstr = outstr[:-1] + ", "
        if outstr != '':
            return outstr[:-2]
        else:
            return "None"
    
    def simtri(self):
        simtri_dict = dict()
        for pt_num1 in range(len(self.points)):
            for pt_num2 in range(pt_num1 + 1, len(self.points)):
                for pt_num3 in range(pt_num2 + 1, len(self.points)):
                    re, im = complexdiv(self.points[pt_num2].c[0] - self.points[pt_num1].c[0], self.points[pt_num2].c[1] - self.points[pt_num1].c[1], self.points[pt_num3].c[0] - self.points[pt_num1].c[0], self.points[pt_num3].c[1] - self.points[pt_num1].c[1])
                    re2 = re**2 - re - im**2
                    im2 = 2*re*im - im
                    re3 = re2**2 - im2**2
                    im3 = 2 * im2 * re2
                    re4 = 1 - 3*im2**2 + 3*re2 - 3*im2**2*re2 + 3*re2**2 + re2**3
                    im4 = 3*im2 - im2**3 + 6*im2*re2 + 3*im2*re2**2
                    c0 = complexdiv(re3, im3, re4, im4)
                    if abs(c0[1]) > 10 ** -CHECK_ERROR:
                        c0 = (rnd(c0[0]), abs(rnd(c0[1])))
                        if c0 in simtri_dict:
                            simtri_dict[c0].append((pt_num1, pt_num2, pt_num3))
                        else:
                            simtri_dict[c0] = [(pt_num1, pt_num2, pt_num3)]
        self.simtri_dict = simtri_dict
        return printchecklist(self.simtri_dict.values(), lambda x: "Δ(" + self.points[x[0]].name + " " + self.points[x[1]].name + " " + self.points[x[2]].name + ")", midsymbol="~", midsymbol2="\n")
    
    def dratio(self):
        preplist = [()]