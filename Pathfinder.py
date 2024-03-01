import GeomTool

CHECK_ERROR = 9

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

def printchecklist(in_list):
    outstr = ""
    for sublst in in_list:
        if len(sublst) > 1:
            for obj in sublst:
                outstr += obj.name + " = "
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
            return (-c0[0], -c0[1], -c0[2])
    elif c0[0] > 0:
        return c0
    else:
        return (-c0[0], -c0[1], -c0[2])

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
