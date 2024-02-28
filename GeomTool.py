import random, math

'''
class Construction:
    def __init__(self, in_method, in_item):
        self.method = in_method # The method of consturction
        self.item = in_item # The items we used in construction
        self.result = self.method.apply(self.item)
    def generate(self):
        pass
'''

class Method:
    def __init__(self, in_name, in_gen_type, in_item_type):
        self.name = in_name # Name of the method
        self.gen_type = in_gen_type # Type of the generated object
        self.item_type = in_item_type # Type of the used items
    def generate(self, in_fun, in_check, in_errorinfo): 
        self.apply = lambda in_name: lambda in_item: Geom_object(in_name, self.gen_type, self, in_item) # The function apply to generate a geom_object
        self.fun = in_fun # The numerical function to give out coordinate or equation coefficients
        self.check = in_check # The numerical boolean check function
        self.errorinfo = in_errorinfo # The error info output function
    def generate_check_triv(self, in_fun):
        self.apply = lambda in_name: lambda in_item: Geom_object(in_name, self.gen_type, self, in_item) # The function apply to generate a geom_object with trivial nondegenerate condition
        self.fun = in_fun
        self.check = lambda in_name: lambda in_item: True # Trivial check
        self.errorinfo = lambda in_name: lambda in_item: "" # Trivial errorinfo

"""
Type: Point, Segment, Ray, Line, Circle, Angle, Length, Vector, Triangle, Others
"""
## Objects in type `Others` will not be drawn

class Geom_object:
    def __init__(self, in_name, in_type, in_method, in_item):
        self.name = in_name # Name of the object --in
        self.type = in_type # Type of the object --in
        self.method = in_method # The method used to generate the object --in
        self.item = in_item # The items used to generate the object -- out 
        self.hasc = False
    def getc(self, in_tuple):
        self.c = in_tuple # The coordinate or the equation coefficients of the object
        self.hasc = True
    def calcc(self):
        for item_num in range(len(self.item)):
            if self.method.item_type[item_num] != "Others" and (not self.item[item_num].hasc):
                self.item[item_num].calcc()
        self.c = self.method.fun(self.item) # Calculate the coordinate without error check and errorinfo print
        self.hasc = True
    def check(self):
        if len(self.item) != len(self.method.item_type):
            return False
        for item_num in range(len(self.item)):
            if self.method.item_type[item_num] != "Others" and self.item[item_num].type != self.method.item_type[item_num]:
                return False
            if not self.method.item_type[item_num].hasc:
                return False
        return self.method.check(self.name, self.item)
    def errorinfo(self):
        if len(self.item) != len(self.method.item_type):
            return "Method supposed to use " + str(len(self.method.item_type)) + " Items but got " + str(len(self.item))
        for item_num in range(len(self.item)):
            if self.method.item_type[item_num ] != "Others" and self.item[item_num].type != self.method.item_type[item_num ]:
                return "Item " + str(item_num) + " supposed to be Type " + self.method.item_type[item_num ] + " but got " + self.item[item_num].type
            if not self.method.item_type[item_num].hasc:
                return "Item " + str(item_num) + " not computed"
        return self.method.errorinfo(self.name, self.item)

# predefined check functions


# Geometric Methods

ERROR = 1e-13

create_empty = Method ("empty", "Others", ()) 
create_empty_fun = lambda in_name, in_item : None
create_empty.generate_check_triv(create_empty_fun)

free_pt = Method("free_pt", "Point", ())
free_pt_fun = lambda in_name, in_item : (random.gauss(0, 1), random.gauss(0, 1))
free_pt.generate_check_triv(free_pt_fun)

line = Method("line", "Line", ("Point", "Point"))
line_check = lambda in_name, in_item : (abs(in_item[0].c[0] - in_item[1].c[0]) > ERROR) and (abs(in_item[0].c[1] - in_item[1].c[1]) > ERROR)
line_errorinfo = lambda in_name, in_item: "Point " + in_item[0].name + " and Point " + in_item[1].name + " coincide" if not(line_check(in_item)) else ""
line_fun = lambda in_name, in_item: (in_item[0].c[1] - in_item[1].c[1], in_item[1].c[0] - in_item[0].c[0], in_item[0].c[0] * in_item[1].c[1] - in_item[1].c[0] * in_item[0].c[1])
line.generate(line_fun, line_check, line_errorinfo)

on_line = Method("on_line", "Point", ("Line"))
def on_line_fun (in_name, in_item):
    if abs(in_item[0].c[0]) < ERROR:
        return (random.gauss(0, 1), -in_item[0].c[2] / in_item[0].c[1])
    if abs(in_item[0].c[1]) < ERROR:
        return (-in_item[0].c[2] / in_item[0].c[0], random.gauss(0, 1))
    r = random.gauss(0.5, 1)
    return (r * (-in_item[0].c[2] / in_item[0].c[0]), (1 - r) * (-in_item[0].c[2] / in_item[0].c[1]))
on_line.generate_check_triv(on_line_fun)

circ = Method("circ", "Circle", ("Point", "Point"))
circ_fun = lambda in_name, in_item : (in_item[0].c[0], in_item[0].c[1], ((in_item[0].c[0] - in_item[1].c[0]) * (in_item[0].c[0] - in_item[1].c[0]) + (in_item[0].c[1] - in_item[1].c[1]) * (in_item[0].c[1] - in_item[1].c[1]))**(1/2))
circ.generate_check_triv(circ_fun)

on_circ = Method("on_circ", "Point", ("Circle"))
def on_circ_fun (in_name, in_item):
    ang = random.uniform(-math.pi, math.pi)
    return (math.cos(ang) * in_item[0].c[2] + in_item[0].c[0], math.sin(ang) * in_item[0].c[2] + in_item[0].c[0])
on_circ.generate_check_triv(on_circ_fun)

mid_pt = Method("mid_pt", "Point", ("Point", "Point"))
mid_pt_fun = lambda in_name, in_item: ((in_item[0].c[0] + in_item[1].c[0]) / 2, (in_item[0].c[1] + in_item[1].c[1]) / 2)
mid_pt.generate_check_triv(mid_pt_fun)

para_line = Method("para_line", "Line", ("Point", "Line"))
para_line_fun = lambda in_name, in_item: (in_item[1].c[0], in_item[1].c[1], -in_item[1].c[0] * in_item[0].c[0] - in_item[1].c[1] * in_item[0].c[1])
para_line.generate_check_triv(para_line_fun)

para_line2 = Method("para_line2", "Line", ("Point", "Point", "Point"))
para_line2_check = lambda in_name, in_item: line_check(in_name, ["", in_item[1], in_item[2]])
para_line2_errorinfo = lambda in_name, in_item: line_errorinfo(in_name, ["", in_item[1], in_item[2]])
def para_line2_fun(in_name, in_item):
    line1 = line.apply(in_name, ["", in_item[1], in_item[2]])
    line2 = para_line.apply(in_name, ["", in_item[0], line1])
    line2.calcc()
    return line2.c
para_line2.generate(para_line2_fun, para_line2_check, para_line2_errorinfo)

perp_line = Method("perp_line", "Line", ("Point", "Line"))
perp_line_fun = lambda in_name, in_item: (in_item[1].c[1], -in_item[1].c[0], -in_item[1].c[1] * in_item[0].c[0] + in_item[1].c[0] * in_item[0].c[1])
perp_line.generate_check_triv(perp_line_fun)

perp_line2 = Method("perp_line2", "Line", ("Point", "Point", "Point"))
perp_line2_check = lambda in_name, in_item: line_check(in_name, ["", in_item[1], in_item[2]])
perp_line2_errorinfo = lambda in_name, in_item: line_errorinfo(in_name, ["", in_item[1], in_item[2]])
def perp_line2_fun(in_name, in_item):
    line1 = line.apply(in_name, ["", in_item[1], in_item[2]])
    line2 = perp_line.apply(in_name, ["", in_item[0], line1])
    line2.calcc()
    return line2.c
perp_line2.generate(perp_line2_fun, perp_line2_check, perp_line2_errorinfo)

perp_bis = Method("perp_bis", "Line", ("Point", "Point"))
perp_bis_check = line_check
perp_bis_errorinfo = line_errorinfo
def perp_bis_fun(in_name, in_item):
    point1 = mid_pt.apply(in_name, ["", in_item[0], in_item[1]])
    line1 = line.apply(in_name, ["", in_item[0], in_item[1]])
    line2 = perp_line.apply(in_name, ["", point1, line1])
    line2.calcc()
    return line2.c
perp_bis.generate(perp_bis_fun, perp_bis_check, perp_bis_errorinfo)

inx_line_line = Method("inx_line_line", "Point", ("Line", "Line"))
inx_line_line_check = lambda in_name, in_item: abs(in_item[0].c[0] * in_item[1].c[1] - in_item[0].c[1] * in_item[1].c[0]) > ERROR
inx_line_line_errorinfo = lambda in_name, in_item: "Line " + in_item[0].name + " and Line " + in_item[1].name + " are parallel" if not(inx_line_line_check(in_item)) else ""
inx_line_line_fun = lambda in_name, in_item: ((in_item[0].c[1] * in_item[1].c[2] - in_item[0].c[2] * in_item[1].c[1]) / (in_item[0].c[0] * in_item[1].c[1] - in_item[0].c[1] * in_item[1].c[0]), (in_item[0].c[2] * in_item[1].c[0] - in_item[0].c[0] * in_item[1].c[2]) / (in_item[0].c[0] * in_item[1].c[1] - in_item[0].c[1] * in_item[1].c[0]))
inx_line_line.generate(inx_line_line_fun, inx_line_line_check, inx_line_line_errorinfo)

inx_line_line2 = Method("inx_line_line2", "Point", ("Point", "Point", "Point", "Point"))
def inx_line_line2_check(in_name, in_item):
    if not (line_check(in_name, ["", in_item[0], in_item[1]]) and line_check(["", in_item[2], in_item[3]])):
        return False
    line1 = line.apply(in_name, ["", in_item[0], in_item[1]])
    line2 = line.apply(in_name, ["", in_item[2], in_item[3]])
    return inx_line_line_check(["", line1, line2])
def inx_line_line2_errorinfo(in_name, in_item):
    if not line_check(in_name, ["", in_item[0], in_item[1]]):
        return line_errorinfo(["", in_item[0], in_item[1]])
    if not line_check(in_name, ["", in_item[2], in_item[3]]):
        return line_errorinfo(["", in_item[2], in_item[3]])
    line1 = line.apply(in_name, ["", in_item[0], in_item[1]])
    line2 = line.apply(in_name, ["", in_item[2], in_item[3]])
    return inx_line_line_check(["", line1, line2])
def inx_line_line2_fun(in_name, in_item):
    line1 = line.apply(in_name, ["", in_item[0], in_item[1]])
    line2 = line.apply(in_name, ["", in_item[2], in_item[3]])
    point1 = inx_line_line.apply(in_name, ["", line1, line2])
    point1.calcc()
    return point1.c
inx_line_line2.generate(inx_line_line2_fun, inx_line_line2_check, inx_line_line2_errorinfo)

perp_foot = Method("perp_foot", "Point", ("Point", "Line"))
def perp_foot_fun(in_name, in_item):
    line1 = perp_line.apply(in_name, ["", in_item[0], in_item[1]])
    line1.calcc()
    point1 = inx_line_line.apply(in_name, ["", in_item[1], line1])
    point1.calcc()
    return point1.c
perp_foot.generate_check_triv(perp_foot_fun)

perp_foot2 = Method("perp_foot2", "Point", ("Point", "Point", "Point"))
perp_foot2_check = lambda in_name, in_item: line_check(["", in_item[1], in_item[2]])
perp_foot2_errorinfo = lambda in_name, in_item: line_errorinfo(["", in_item[1], in_item[2]])
def perp_foot2_fun(in_name, in_item):
    line1 = line.apply(in_name, ["", in_item[1], in_item[2]])
    point1 = perp_foot.apply(in_name, ["", in_item[0], line1])
    point1.calcc()
    return point1.c
perp_foot2.generate(perp_foot2_fun, perp_foot2_check, perp_foot2_errorinfo)

tgnt_line = Method("tgnt_line", "Point", ("Point", "Point"))
bary_cent = Method("circ_cent", "Point", ("Point", "Point", "Point"))
circ_cent = Method("circ_cent", "Point", ("Point", "Point", "Point"))

class Geom_node:
    def __init__(self, obj):
        self.obj = obj
        self.parent_list = []
        self.children_list = []

class Geom_construction:
    def __init__(self):
        self.node_list = []
        self.root_list = []

# Simple test

if __name__ == '__main__':
    pass
