import random, math

class Construction:
    def __init__(self, in_method, in_item):
        self.method = in_method # The method of consturction
        self.item = in_item # The items we used in construction
        self.result = (self.method.apply)(self.item)
    def generate(self):
        pass

class Method:
    def __init__(self, in_name, in_gen_type):
        self.name = in_name # Name of the method
        self.gen_type = in_gen_type # Type of the generated object
    def generate(self, in_fun, in_check, in_errorinfo): 
        self.apply = lambda in_item: Geom_object(in_item[0], self.gen_type, self, in_item) # The function apply to generate a geom_object
        self.fun = in_fun # The numerical function to give out coordinate or equation coefficients
        self.check = in_check # The numerical boolean check function
        self.errorinfo = in_errorinfo # The error info output function

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

point_plane = Method("Point on a Plane", "Point")
point_plane_check = lambda in_item: True
point_plane_errorinfo = lambda errorinfo: ""
point_plane_fun = lambda in_item: (random.gauss(0, 1), random.gauss(0, 1))
point_plane.generate(point_plane_fun, point_plane_check, point_plane_errorinfo)

line_point_point = Method("Line by Two Points", "Line")
line_point_point_check = lambda in_item: (abs(in_item[1].c[0] - in_item[2].c[0]) > ERROR) and (abs(in_item[1].c[1] - in_item[2].c[1]) > ERROR)
line_point_point_errorinfo = lambda in_item: in_item[1].name + " and Point " + in_item[2].name + " coincide" if not(line_point_point_check(in_item)) else ""
line_point_point_fun = lambda in_item: (in_item[1].c[1] - in_item[2].c[1], in_item[2].c[0] - in_item[1].c[0], in_item[1].c[0] * in_item[2].c[1] - in_item[2].c[0] * in_item[1].c[1])
line_point_point.generate(line_point_point_fun, line_point_point_check, line_point_point_errorinfo)

point_line = Method("Point on a Line", "Point")
point_line_check = lambda in_item: True
point_line_errorinfo = lambda errorinfo: ""
def point_line_fun (in_item):
    if abs(in_item[1].c[0]) < ERROR:
        return (random.gauss(0, 1), -in_item[1].c[2] / in_item[1].c[1])
    if abs(in_item[1].c[1]) < ERROR:
        return (-in_item[1].c[2] / in_item[1].c[0], random.gauss(0, 1))
    r = random.gauss(0.5, 1)
    return (r * (-in_item[1].c[2] / in_item[1].c[0]), (1 - r) * (-in_item[1].c[2] / in_item[1].c[1]))

circle_center_point = Method("Circle by Center and a Point", "Circle")
circle_center_point_check = lambda in_item: True
circle_center_point_errorinfo = lambda errorinfo: ""
circle_center_point_fun = lambda in_item: (in_item[1].c[0], in_item[1].c[1], ((in_item[1].c[0] - in_item[2].c[0]) * (in_item[1].c[0] - in_item[2].c[0]) + (in_item[1].c[1] - in_item[2].c[1]) * (in_item[1].c[1] - in_item[2].c[1]))**(1/2))
circle_center_point.generate(circle_center_point_fun, circle_center_point_check, circle_center_point_errorinfo)

point_circle = Method("Point on a Circle", "Point")
point_circle_check = lambda in_item: True
point_circle_errorinfo = lambda errorinfo: ""
def point_circle_fun (in_item):
    ang = random.uniform(-math.pi, math.pi)
    return (math.cos(ang) * in_item[1].c[2] + in_item[1].c[0], math.sin(ang) * in_item[1].c[2] + in_item[1].c[0])
point_circle.generate(point_circle_fun, point_circle_check, point_circle_errorinfo)

midpoint_point_point = Method("Midpoint of Two Points", "Point")

class Geom_construction:
    def __init__(self): 
        pass



def addone(n):
    return n + 1

def res(a, b):
    return (a)(b)

print(res(addone, 1))


