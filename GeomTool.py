import random, math

'''
A temporory naming choice. Please rewrite this once dependency is finished.
'''

name_counter = 100
def default_name (Type : str) : 
    global name_counter 
    name_counter = name_counter + 1
    if Type == "Point":
        return "p"+str(name_counter)
    if Type == "Line":
        return "l"+str(name_counter)
    if Type == "Circle":
        return "c"+str(name_counter)
    else:
        return "NoName"
    
ERROR = 1e-13
def numberform(realnum):
    # String a number in a relatively short form
    if abs(realnum) < ERROR:
        return "0.000"
    if abs(realnum) < 1e-2 or abs(realnum) > 1e3:
        return "{:.3e}".format(realnum)
    else:
        return "{:.3f}".format(realnum)


class GeomObj:
    def __init__(self, in_name, in_type, in_method, in_item, in_visible = True, in_movable = False, in_tree = None):
        if in_name == None:
            self.name = default_name(in_type)
        else:
            self.name = in_name # Name of the object
        self.type = in_type # Type of the object
        self.method = in_method # The method used to generate the object
        self.item = in_item # The items used to generate the object
        self.hasc = False
        self.affect_item = []  #The items using this object to generate object
        for parent_item in in_item:
            parent_item.affect_item += [ self ]
        global current_tree
        if in_tree == None:
            self.tree = current_tree
        else:
            self.tree = in_tree
        self.tree.obj_list += [self]
        self.visible = in_visible
        self.movable = in_movable
        print("init_run", self.name)
        
    def __str__(self):
        addstr = ''
        if self.hasc:
            addstr = ', c = ' + str(self.c)
        return self.type + ' ' + self.name + ', method = ' + self.method.name + addstr

    def getc(self, in_tuple):
        self.c = in_tuple # The coordinate or the equation coefficients of the object
        self.hasc = True

    def calcc(self):
        for parent_item in self.item:
            if parent_item.type != "Others" and (not parent_item.hasc):
                parent_item.calcc()
        self.c = self.method.fun(self) # Calculate the coordinate without error check and errorinfo print
        # only BasicMethod provides calc method
        self.hasc = True

    def basic_check(self): # only after all depending objects hasc, this method would be safe. Do NOT use this function alone! 
        if len(self.item) != len(self.method.item_type):
            return False
        for item_num in range(len(self.item)):
            if self.method.item_type[item_num] != "Others" and self.item[item_num].type != self.method.item_type[item_num]:
                return False
            if str(type(self.method.item_type[item_num])) == "<class '__main__.GeomObj'>" and not self.method.item_type[item_num].hasc:
                return False
        return self.method.check(self)
        
    def check_and_calcc(self): # recursively check and calc, return False when any depending obj check fails, return true and calc c for all depending obj. This may cause some depending objs being calculated while self is not.
        for parent_item in self.item:
            parent_item_check = parent_item.check_and_calcc()
            if not parent_item_check:
                return False
        if self.basic_check():
            if self.hasc == False: #only calc when current obj is not already calculated
                self.c = self.method.fun(self)
                self.hasc = True
            return True
        else:
            return False
    
    def errorinfo(self):
        if len(self.item) != len(self.method.item_type):
            return "Method supposed to use " + str(len(self.method.item_type)) + " Items but got " + str(len(self.item))
        for item_num in range(len(self.item)):
            if self.method.item_type[item_num ] != "Others" and self.item[item_num].type != self.method.item_type[item_num ]:
                return "Item " + str(item_num) + " supposed to be Type " + self.method.item_type[item_num ] + " but got " + self.item[item_num].type
            if not self.method.item_type[item_num].hasc:
                return "Item " + str(item_num) + " not computed"
        return self.method.errorinfo(self)
    
    
    """
    The followings are StupidUpdate
    """
    
    def update_not_hasc(self):
        for obj in self.affect_item:
            obj.hasc = False
            obj.update_not_hasc()
    
    def calcc0(self):
        allhasc = True
        for parent_item in self.item:
            if parent_item.type != "Others" and (not parent_item.hasc):
                allhasc = False
        if allhasc and self.method.check(self):
            if not self.hasc :
                self.c = self.method.fun(self) # Calculate the coordinate without error check and errorinfo print
                self.hasc = True
    
    def update(self):
        for obj in self.affect_item:
            obj.calcc0()
        for obj in self.affect_item:
            obj.update()
    
    def stupid_update(self):
        self.update_not_hasc()
        self.update()
    
    def move(self, in_c):
        if self.movable and self.method.name == "free_pt":
            self.c = in_c
            self.stupid_update()
            
            
    
class Method:
    def __init__(self, in_name, in_gen_type : list, in_item_type : list, in_cmd_name : str):
        self.name = in_name # Name of the method
        self.gen_type = in_gen_type # Type of the generated object(s), still a list even when generate a single object
        self.item_type = in_item_type # Type of the used items
        self.implemented = False # turn True once apply and calculation method is provided
        self.apply = None
        self.cmd_name = in_cmd_name
        global MethodDict
        MethodDict[in_name] = [self.cmd_name, self, self.item_type, self.gen_type]


class BasicMethod(Method):
    '''
    Basic Geometic construction methods class. Creates only one object. Stores dependency information.
    '''
    def __init__(self, in_name, in_gen_type: list, in_item_type: list, in_cmd_name : str, in_movable = False):
        super().__init__(in_name, in_gen_type, in_item_type, in_cmd_name)
        if len(in_gen_type) != 1:
            print("Error during init " + in_name + " method, Basic method must create exactly one object!")
        self.fun = None
        self.check = None
        self.errorinfo = None
        self.movable = in_movable

    def implement(self, in_fun, in_check, in_errorinfo): # fill more information needed
        self.apply = lambda in_name, in_item, in_visible = True, aux_visible = False : GeomObj(in_name, self.gen_type[0], self, in_item, in_visible = in_visible, in_movable = self.movable) # The function apply to generate a geom_object
        #aux_visible is not needed in BasicMethod, keeps for aligning with ComplexMethod
        self.fun = in_fun # The numerical function to give out coordinate or equation coefficients, input self
        self.check = in_check # The numerical boolean check function, input self
        self.errorinfo = in_errorinfo # The error info output function, input self
        self.implemented = True

    def implement_check_triv(self, in_fun):
        self.implement(in_fun, lambda self: True, lambda self: "")
        
    
class ComplexMethod(Method):

    def construct_in_item (in_item : list, m_item : list, indicator_list : list, i : int):
        item_list = []
        for j in indicator_list[i]:
            if j[0] == "i":
                item_list += [in_item[j[1]]]
            if j[0] == "m":
                item_list += [m_item[j[1]]]
        return item_list

    def recursively_apply (final_name : str, in_item, method_list : list, indicator_list : list, in_visible = True, aux_visible = False):
        m_item = []
        for i in range(len(method_list)):
            item_list = ComplexMethod.construct_in_item(in_item, m_item, indicator_list, i) 
            if i == len(method_list) - 1:
                return method_list[i].apply(final_name, item_list, in_visible = in_visible, aux_visible = aux_visible) ## return the last object
            else:
                m_item += [method_list[i].apply(None, item_list, in_visible = aux_visible, aux_visible = aux_visible)]

    '''
    Class of complex methods, recursively create all needed geometric constructions.
    use apply to create all objects recursively, use calc to calc all coordinates of dependending objects recursively
    '''
    def __init__(self, in_name, in_gen_type: list, in_item_type: list, in_cmd_name : str):
        super().__init__(in_name, in_gen_type, in_item_type, in_cmd_name)
        
    def implement(self, in_method_list, in_indicator_list):
        for i in in_method_list:
            if not i.implemented :
                print("Error during implement " + self.name + " method, method " + i.name + " is used but not implemented!")
        if (len(in_method_list) != len(self.gen_type)) or (len(in_indicator_list) != len(self.gen_type)):
            print("Error during implement " + self.name + " method, length of method list, gen type, indicator list do NOT match !")
        for i in range(len(in_method_list)):
            if in_method_list[i].gen_type[-1] != self.gen_type[i] :
                print("Error during implement " + self.name + " method, type of step " + str(i) + " construction do NOT match type of method!")

        self.method_list = in_method_list
        self.indicator_list = in_indicator_list
        self.apply = lambda in_name, in_item, in_visible = True, aux_visible = False: ComplexMethod.recursively_apply(in_name, in_item, self.method_list, self.indicator_list, in_visible = in_visible, aux_visible = aux_visible)
        self.implemented = True

        
        ##self.fun = in_fun # The numerical function to give out coordinate or equation coefficients, input self
        ##self.check = in_check # The numerical boolean check function, input self
        ##self.errorinfo = in_errorinfo # The error info output function, input self


## in_item : b c,    
## a = f b c
## d = g a b
## indicator_list : [("i",0), ("i",1)], [("m",0), ("i",0)]
## method_list : ["f", "g"]


class GraphTree:
    def __init__(self):
        self.obj_list = []
    
    def get_totally_free(self):
        r = []
        for obj in self.obj_list:
            if obj.item == []:
                r += [obj]
        return r
    
    def get_has_free(self):
        NotImplemented
    
    def get_visible(self):
        r = []
        for obj in self.obj_list:
            if obj.visible:
                r += [obj]
        return r


    def get_invisible(self):
        r = []
        for obj in self.obj_list:
            if not obj.visible:
                r += [obj]
        return r

    def get_movable(self):
        r = []
        for obj in self.obj_list:
            if obj.movable:
                r += [obj]
        return r


####################
##    Methods     ##
####################

# The Global Dict used in other programs
MethodDict = {}

free_pt = BasicMethod("free_pt", ["Point"], [], "pt", in_movable=True)
free_pt_fun = lambda self : (random.gauss(0, 1), random.gauss(0, 1))
free_pt.implement_check_triv(free_pt_fun)

line = BasicMethod("line", ["Line"], ["Point", "Point"], "line")
line_check = lambda self : (abs(self.item[0].c[0] - self.item[1].c[0]) > ERROR) or (abs(self.item[0].c[1] - self.item[1].c[1]) > ERROR)
line_errorinfo = lambda self: "Point " + self.item[0].name + " and Point " + self.item[1].name + " coincide" if not(line_check(self.in_name, self.item)) else ""
line_fun = lambda self: (self.item[0].c[1] - self.item[1].c[1], self.item[1].c[0] - self.item[0].c[0], self.item[0].c[0] * self.item[1].c[1] - self.item[1].c[0] * self.item[0].c[1])
line.implement(line_fun, line_check, line_errorinfo)

circle = BasicMethod("circle", ["Circle"], ["Point", "Point"], "circ")
circle_fun = lambda self: (self.item[0].c[0], self.item[0].c[1], ((self.item[0].c[0] - self.item[1].c[0])**2 + (self.item[0].c[1] - self.item[1].c[1])**2)**(1/2))
circle.implement_check_triv(circle_fun)

circle_center = BasicMethod("circle_center", ["Point"], ["Circle"], "mdpt")
circle_center_fun = lambda self: (self.item[0].c[0], self.item[0].c[1])
circle_center.implement_check_triv(circle_center_fun)

inx_line_line = BasicMethod("inx_line_line", ["Point"], ["Line", "Line"], "pt")
inx_line_line_check = lambda self: abs(self.item[0].c[0] * self.item[1].c[1] - self.item[0].c[1] * self.item[1].c[0]) > ERROR
inx_line_line_errorinfo = lambda self: "Line " + self.item[0].name + " and Line " + self.item[1].name + " are parallel" if not(inx_line_line_check(self)) else ""
inx_line_line_fun = lambda self: ((self.item[0].c[1] * self.item[1].c[2] - self.item[0].c[2] * self.item[1].c[1]) / (self.item[0].c[0] * self.item[1].c[1] - self.item[0].c[1] * self.item[1].c[0]), (self.item[0].c[2] * self.item[1].c[0] - self.item[0].c[0] * self.item[1].c[2]) / (self.item[0].c[0] * self.item[1].c[1] - self.item[0].c[1] * self.item[1].c[0]))
inx_line_line.implement(inx_line_line_fun, inx_line_line_check, inx_line_line_errorinfo)

mid_pt = BasicMethod("mid_pt", ["Point"], ["Point", "Point"], "mdpt")
mid_pt_fun = lambda self: ((self.item[0].c[0] + self.item[1].c[0]) / 2, (self.item[0].c[1] + self.item[1].c[1]) / 2)
mid_pt.implement_check_triv(mid_pt_fun)

para_line = BasicMethod("para_line", ["Line"], ["Point", "Line"], "para")
para_line_fun = lambda self: (self.item[1].c[0], self.item[1].c[1], -self.item[1].c[0] * self.item[0].c[0] - self.item[1].c[1] * self.item[0].c[1])
para_line.implement_check_triv(para_line_fun)

perp_line = BasicMethod("perp_line", ["Line"], ["Point", "Line"], "perp")
perp_line_fun = lambda self: (self.item[1].c[1], -self.item[1].c[0], -self.item[1].c[1] * self.item[0].c[0] + self.item[1].c[0] * self.item[0].c[1])
perp_line.implement_check_triv(perp_line_fun)

angle_bis_pt = BasicMethod("angle_bis_pt", ["Point"], ["Point", "Point", "Point"], "abispoint")
angle_bis_pt_check = lambda self: ((abs(self.item[0].c[0] - self.item[1].c[0]) > ERROR) or (abs(self.item[0].c[1] - self.item[1].c[1]) > ERROR)) and ((abs(self.item[2].c[0] - self.item[1].c[0]) > ERROR) or (abs(self.item[2].c[1] - self.item[1].c[1]) > ERROR))
angle_bis_pt_errorinfo = lambda self: "Point " + self.item[0].name + " and Point " + self.item[1].name + " and Point " + self.item[2].name + " do not form an angle" if not(angle_bis_check(self)) else ""
def angle_bis_pt_fun(self):
    print("hi")
    deltax1 = self.item[0].c[0] - self.item[1].c[0]
    deltay1 = self.item[0].c[1] - self.item[1].c[1]
    deltax2 = self.item[2].c[0] - self.item[1].c[0]
    deltay2 = self.item[2].c[1] - self.item[1].c[1]
    returnx = self.item[1].c[0] + ((deltax1 ** 2 * deltax2 ** 2 + deltax2 ** 2 * deltay1 ** 2 + deltax1 ** 2 * deltay2 ** 2 + deltay1 ** 2 * deltay2 ** 2 + deltax1 * deltax2 * ((deltax1 ** 2 + deltay1 ** 2) * (deltax2 ** 2 + deltay2 ** 2)) ** (1/2) - deltay1 * deltay2 * ((deltax1 ** 2 + deltay1 ** 2) * (deltax2 ** 2 + deltay2 ** 2)) ** (1/2)) ** (1/2)) / ((2 * (deltax1 ** 2 + deltay1 ** 2) * (deltax2 ** 2 + deltay2 ** 2)) ** (1/2))
    returny = self.item[1].c[1] + ((deltay1 ** 2 * deltay2 ** 2 + deltay2 ** 2 * deltax1 ** 2 + deltay1 ** 2 * deltax2 ** 2 + deltax1 ** 2 * deltax2 ** 2 + deltay1 * deltay2 * ((deltay1 ** 2 + deltax1 ** 2) * (deltay2 ** 2 + deltax2 ** 2)) ** (1/2) - deltax1 * deltax2 * ((deltay1 ** 2 + deltax1 ** 2) * (deltay2 ** 2 + deltax2 ** 2)) ** (1/2)) ** (1/2)) / ((2 * (deltay1 ** 2 + deltax1 ** 2) * (deltay2 ** 2 + deltax2 ** 2)) ** (1/2))
    return (returnx, returny)
angle_bis_pt.implement(angle_bis_pt_fun, angle_bis_pt_check, angle_bis_pt_errorinfo) 

perp_bis = ComplexMethod("perp_bis", ["Point", "Line", "Line"], ["Point", "Point"], "pbis")
perp_method_list = [mid_pt, line, perp_line]
perp_indicator_list = [[("i",0), ("i",1)], [("i",0), ("i",1)], [("m",0), ("m",1)]]
perp_bis.implement(perp_method_list, perp_indicator_list)

circum_center = ComplexMethod("circum_center", ["Line", "Line", "Point"], ["Point", "Point", "Point"], "circ_cent")
circum_center_method_list = [perp_bis, perp_bis, inx_line_line]
circum_center_indicator_list = [[("i",0), ("i",1)], [("i",0), ("i",2)], [("m",0), ("m",1)]]
circum_center.implement(circum_center_method_list, circum_center_indicator_list)

angle_bis = ComplexMethod("angle_bis", ["Point", "Line"], ["Point", "Point", "Point"], "abis")
angle_bis_method_list = [angle_bis_pt, line]
angle_bis_indicator_list = [[("i",0), ("i",1), ("i",2)], [("i",1), ("m",0)]]
angle_bis.implement(angle_bis_method_list, angle_bis_indicator_list)


'''
The Dictionary of all methods. All methods should be included here. Format:
key : unique name
query : List( cmd name : str , Method itself, input_type_list, output_type_list)
'''

current_tree = GraphTree()
    
if __name__ == '__main__':
    p1 = free_pt.apply("p1",[])
    print("p1 created")
    p2 = free_pt.apply("p2",[])
    print("p2 created")
    p3 = mid_pt.apply("p3", [p1, p2])
    print("p3 created")
    p4 = free_pt.apply("p4", [])
    l1 = perp_bis.apply("l1", [p1, p2])
    print("l1 created", l1)
    l = line.apply("l", [p1, p3])
    print("l created")
    print(type (circum_center.apply))
    o = circum_center.apply("o", [p1, p2, p4])
    print("o created")
    i = angle_bis.apply("i", [p1, p2, p4])
    print("i created")
    l1.calcc()
    print("l1 calculated", l1.hasc, l1.c)
    o.calcc()
    print("o calculated", o.hasc, o.c)
    i.calcc()
    print("i calculated", i.hasc, i.c)
    print( [i.name for i in p1.affect_item] )
    