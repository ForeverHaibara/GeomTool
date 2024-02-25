import random, math

class Construction:
    def __init__(self, in_method, in_item):
        self.method = in_method # The method of consturction
        self.item = in_item # The items we used in construction
        self.result = (self.method.apply)(self.item)
    def generate(self):
        pass

class Method:
    def __init__(self, in_name, in_gen_type, in_item_type):
        self.name = in_name # Name of the method
        self.gen_type = in_gen_type # Type of the generated object
        self.item_type = in_item_type # Type of the used items
    def generate(self, in_fun, in_check, in_errorinfo): 
        self.apply = lambda in_item: Geom_object(in_item[0], self.gen_type, self, in_item) # The function apply to generate a geom_object
        self.fun = in_fun # The numerical function to give out coordinate or equation coefficients
        self.check = in_check # The numerical boolean check function
        self.errorinfo = in_errorinfo # The error info output function
    def generate_check_triv(self, in_fun):
        self.apply = lambda in_item: Geom_object(in_item[0], self.gen_type, self, in_item) # The function apply to generate a geom_object with trivial nondegenerate condition
        self.fun = in_fun
        self.check = lambda in_item: True # Trivial check
        self.errorinfo = lambda errorinfo: "" # The error info output function

"""
Type: Point, Segment, Ray, Line, Circle, AngleValue2pi(mod 2pi), Length, Vector, Triangle, 
"""
class Geom_object:
    def __init__(self, in_name, in_type, in_method, in_item):
        self.name = in_name # Name of the object
        self.type = in_type # Type of the object
        self.method = in_method # The method used to generate the object
        self.item = in_item # The items used to generate the object
    def getc(self, in_tuple):
        self.c = in_tuple # The coordinate or the equation coefficients of the object

ERROR = 1e-12

free_pt = Method("free_pt", "Point", ())
free_pt_fun = lambda in_item: (random.gauss(0, 1), random.gauss(0, 1))
free_pt.generate_check_triv(free_pt_fun)

line = Method("line", "Line", ("Point", "Point"))
line_check = lambda in_item: (abs(in_item[1].c[0] - in_item[2].c[0]) > ERROR) and (abs(in_item[1].c[1] - in_item[2].c[1]) > ERROR)
line_errorinfo = lambda in_item: in_item[1].name + " and Point " + in_item[2].name + " coincide" if not(line_check(in_item)) else ""
line_fun = lambda in_item: (in_item[1].c[1] - in_item[2].c[1], in_item[2].c[0] - in_item[1].c[0], in_item[1].c[0] * in_item[2].c[1] - in_item[2].c[0] * in_item[1].c[1])
line.generate(line_fun, line_check, line_errorinfo)

on_line = Method("on_line", "Point", ("Line"))
def on_line_fun (in_item):
    if abs(in_item[1].c[0]) < ERROR:
        return (random.gauss(0, 1), -in_item[1].c[2] / in_item[1].c[1])
    if abs(in_item[1].c[1]) < ERROR:
        return (-in_item[1].c[2] / in_item[1].c[0], random.gauss(0, 1))
    r = random.gauss(0.5, 1)
    return (r * (-in_item[1].c[2] / in_item[1].c[0]), (1 - r) * (-in_item[1].c[2] / in_item[1].c[1]))
on_line.generate_check_triv(on_line_fun)

circ = Method("circ", "Circle", ("Point", "Point"))
circ_fun = lambda in_item: (in_item[1].c[0], in_item[1].c[1], ((in_item[1].c[0] - in_item[2].c[0]) * (in_item[1].c[0] - in_item[2].c[0]) + (in_item[1].c[1] - in_item[2].c[1]) * (in_item[1].c[1] - in_item[2].c[1]))**(1/2))
circ.generate_check_triv(circ_fun)

on_circ = Method("on_circ", "Point", ("Circle"))
def on_circ_fun (in_item):
    ang = random.uniform(-math.pi, math.pi)
    return (math.cos(ang) * in_item[1].c[2] + in_item[1].c[0], math.sin(ang) * in_item[1].c[2] + in_item[1].c[0])
on_circ.generate_check_triv(on_circ_fun)

mid_pt = Method("mid_pt", "Point", ("Point", "Point"))
mid_pt_fun = lambda in_item: ((in_item[1].c[0] + in_item[2].c[0]) / 2, (in_item[1].c[1] + in_item[2].c[1]) / 2)
mid_pt.generate_check_triv(mid_pt_fun)

para_line = Method("para_line", "Line", ("Point", "Line"))
para_line_fun = lambda in_item: (in_item[2].c[0], in_item[2].c[1], -in_item[2].c[0] * in_item[1].c[0] - in_item[2].c[1] * in_item[1].c[1])
para_line.generate_check_triv(para_line_fun)

perp_line = Method("perp_line")

class Geom_construction:
    def __init__(self): 
        pass


