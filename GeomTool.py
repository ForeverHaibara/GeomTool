import random, math

ERROR = 1e-13

disturb_strength = 1e-4

name_initial = {
    "Point" : "p",
    "Line" : "l",
    "Circle" : "c"}

def default_name (Type : str) :
    '''
    Generate a default name for GeomObj if no name is specified.
    '''
    name_list = [obj.name for obj in current_tree.obj_list]
    name_num = 0
    if Type in name_initial.keys():
        while (name_initial[Type] + str(name_num)) in name_list:
            name_num += 1
        return (name_initial[Type] + str(name_num))
    else:
        while ("NoName" + str(name_num)) in name_list:
            name_num += 1
        return ("NoName" + str(name_num))
    

def numberform(realnum):
    '''
    String a number in a relatively short form
    '''
    if abs(realnum) < ERROR:
        return "0.000"
    if abs(realnum) < 1e-2 or abs(realnum) > 1e3:
        return "{:.3e}".format(realnum)
    else:
        return "{:.3f}".format(realnum)



def fig_intersection(fig1c, fig1type, fig2c, fig2type):
    '''
    A tool used to calculate fig_intersection, suitable Line + Line, Line + Circle, Circle + Circle.
    '''
    if fig1type == "Line":
        if fig2type == "Line":
            if abs(fig1c[1] * fig2c[0] - fig1c[0] * fig2c[1]) > ERROR:
                return [((fig1c[2] * fig2c[1] - fig1c[1] * fig2c[2])/(fig1c[1] * fig2c[0] - fig1c[0] * fig2c[1]), (-fig1c[2] * fig2c[0] + fig1c[0] * fig2c[2])/(fig1c[1] * fig2c[0] - fig1c[0] * fig2c[1]))]
            else:
                return []
        if fig2type == "Circle":
            Disc = (-(fig1c[2] + fig1c[0] * fig2c[0] + fig1c[1] * fig2c[1])**2 + (fig1c[0]**2 + fig1c[1]**2) * fig2c[2]**2)
            if  Disc >= -ERROR:
                Delta = fig1c[1]**2 * (-(fig1c[2] + fig1c[0] * fig2c[0] + fig1c[1] * fig2c[1])**2 + (fig1c[0]**2 + fig1c[1]**2) * fig2c[2]**2)
                Delta = max(0, Delta)
                x1 = -((-fig1c[1]**2 * fig2c[0] + fig1c[0] * (fig1c[2] + fig1c[1] * fig2c[1]) + Delta ** (1/2))/(fig1c[0]**2 + fig1c[1]**2))
                x2 = -((-fig1c[1]**2 * fig2c[0] + fig1c[0] * (fig1c[2] + fig1c[1] * fig2c[1]) - Delta ** (1/2))/(fig1c[0]**2 + fig1c[1]**2))
                Delta = fig1c[0]**2 * (-(fig1c[2] + fig1c[1] * fig2c[1] + fig1c[0] * fig2c[0])**2 + (fig1c[1]**2 + fig1c[0]**2) * fig2c[2]**2)
                Delta = max(0, Delta)
                y1 = -((-fig1c[0]**2 * fig2c[1] + fig1c[1] * (fig1c[2] + fig1c[0] * fig2c[0]) + Delta ** (1/2))/(fig1c[1]**2 + fig1c[0]**2))
                y2 = -((-fig1c[0]**2 * fig2c[1] + fig1c[1] * (fig1c[2] + fig1c[0] * fig2c[0]) - Delta ** (1/2))/(fig1c[1]**2 + fig1c[0]**2))
                if Disc >= ERROR:
                    if abs(fig1c[0] * x1 + fig1c[1] * y1 + fig1c[2]) < ERROR:
                        return [(x1, y1), (x2, y2)]
                    else:
                        return [(x1, y2), (x2, y1)]
                else:
                    return [(x1, y1)]
    if fig1type == "Circle":
        if fig2type == "Line":
            return fig_intersection(fig2c, "Line", fig1c, "Circle")
        if fig2type == "Circle":
            if abs(fig1c[0] - fig2c[0]) > ERROR or abs(fig1c[1] - fig2c[1]) > ERROR:
                fig3c = (2 * (fig2c[0] - fig1c[0]), 2 * (fig2c[1] - fig1c[1]), (fig1c[0]**2 + fig1c[1]**2 - fig1c[2]**2) - (fig2c[0]**2 + fig2c[1]**2 - fig2c[2]**2))
                return fig_intersection(fig3c, "Line", fig1c, "Circle")
    return []


class GeomObj:
    def __init__(self, in_name, in_type, in_method, in_item, in_visible = True, in_movable = False, in_tree = None):
        if in_name == None:
            self.name = default_name(in_type)
        else:
            self.name = in_name # Name of the object
        self.type = in_type # Type of the object
        self.method = in_method # The method used to generate the object
        self.item = in_item # The items used to generate the object
        self.hasc = False # Marker that constants needed is calcualted
        self.affect_item = []  # The items using this object to generate object
        for parent_item in in_item:
            parent_item.affect_item += [ self ]
        global current_tree 
        if in_tree == None:
            self.tree = current_tree # which tree to put this object into
        else:
            self.tree = in_tree
        self.tree.obj_list += [self]
        self.visible = in_visible # visibility
        self.movable = in_movable # mobility
        if in_method.name == "free_pt":
            self.freec = (random.gauss(0, 1), random.gauss(0, 1))
        elif in_method.name == "pt_on_line":
            self.freec = random.gauss(1/2, 1)
        elif in_method.name == "pt_on_circle":
            self.freec = random.uniform(-math.pi, math.pi)
        else:
            self.freec = None
        # print("init_run", self.name)
        
    def __str__(self):
        addstr = ''
        if self.hasc:
            addstr = ', c = ' + str(self.c)
        return self.type + ' ' + self.name + ', method = ' + self.method.name + ', visible = ' + str(self.visible) + addstr

    def getc(self, in_tuple):
        '''
        update c by an input
        '''
        self.c = in_tuple # The coordinate or the equation coefficients of the object
        self.hasc = True

    def calcc(self):
        '''
        recursively calc c of all depending objects
        '''
        for parent_item in self.item:
            if parent_item.type != "Others" and (not parent_item.hasc):
                parent_item.calcc()
        self.c = self.method.fun(self) # Calculate the coordinate without error check and errorinfo print
        # only BasicMethod provides calc method
        self.hasc = True

    def basic_check(self): # only after all depending objects hasc, this method would be safe. Do NOT use this function alone! 
        '''
        In the case of all depending objects being calculated, check if this object can be created.
        '''
        if len(self.item) != len(self.method.item_type):
            return False
        for item_num in range(len(self.item)):
            if self.method.item_type[item_num] != "Others" and self.item[item_num].type != self.method.item_type[item_num]:
                return False
            if str(type(self.method.item_type[item_num])) == "<class '__main__.GeomObj'>" and not self.method.item_type[item_num].hasc:
                return False
        return self.method.check(self)
        
    def check_and_calcc(self): 
        '''
        recursively check and calc, return False when any depending obj check fails, return true and calc c for all depending obj. 
        This may cause some depending objs being calculated while self is not when returning False.
        '''
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
            self.freec = in_c
        
        if self.movable and self.method.name == "pt_on_line":
            if abs(self.item[0].item[0].c[0] - self.item[0].item[1].c[0]) > ERROR:
                perpfootx = ((-self.item[0].c[0] * self.item[0].c[2] + self.item[0].c[1]**2 * in_c[0] - self.item[0].c[0] * self.item[0].c[1] * in_c[1])/(self.item[0].c[0]**2 + self.item[0].c[1]**2))
                self.freec = (perpfootx - self.item[0].item[0].c[0]) / (self.item[0].item[1].c[0] - self.item[0].item[0].c[0])
            else:
                perpfooty = ((-self.item[0].c[1] * self.item[0].c[2] - self.item[0].c[0] * self.item[0].c[1] * in_c[0] + self.item[0].c[0]**2 * in_c[1])/(self.item[0].c[0]**2 + self.item[0].c[1]**2))
                self.freec = (perpfooty - self.item[0].item[0].c[1]) / (self.item[0].item[1].c[1] - self.item[0].item[1].c[1])
        
        if self.movable and self.method.name == "pt_on_circle":
            delta1x = (self.item[0].item[1].c[0] - self.item[0].item[0].c[0])
            delta1y = (self.item[0].item[1].c[1] - self.item[0].item[0].c[1])
            len1 = (delta1x ** 2 + delta1y ** 2) ** (1/2)
            if abs(len1) < ERROR:
                return
            delta1x /= len1
            delta1y /= len1
            delta2x = (in_c[0] - self.item[0].item[0].c[0])
            delta2y = (in_c[1] - self.item[0].item[0].c[1])
            len2 = (delta2x ** 2 + delta2y ** 2) ** (1/2)
            if abs(len2) < ERROR:
                return
            delta2x /= len2
            delta2y /= len2
            cosval = (delta2x * delta1x + delta2y * delta1y) * (1 - ERROR)
            sinval = (delta2y * delta1x - delta2x * delta1y)
            if sinval >= 0:
                self.freec = math.acos(cosval)
            else:
                self.freec = -math.acos(cosval)
            
        self.calcc()
        self.stupid_update()
    
    def disturb(self, disturb_strength = disturb_strength):
        '''
        disturb an object. change freec into freec * (1 + e) + e'
        '''
        if (self.freec == None) or (not self.movable) :
            return
        else :
            if type(self.freec) == tuple:
                new_fc = tuple( [i * (1 + random.gauss(0, disturb_strength)) + random.gauss(0, disturb_strength) for i in self.freec] )
            else:
                new_fc = self.freec * (1 + random.gauss(0, disturb_strength)) + random.gauss(0, disturb_strength)
            self.freec = new_fc
            self.calcc()
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
        '''
        Create a BasicMethod, further information will be provide in implement function. 
        '''
        super().__init__(in_name, in_gen_type, in_item_type, in_cmd_name)
        if len(in_gen_type) != 1:
            print("Error during init " + in_name + " method, Basic method must create exactly one object!")
        self.fun = None
        self.check = None
        self.errorinfo = None
        self.movable = in_movable

    def implement(self, in_fun, in_check, in_errorinfo): 
        '''
        fill in more information needed for this method.
        '''
        self.apply = lambda in_name, in_item, in_visible = True, aux_visible = False : GeomObj(in_name, self.gen_type[0], self, in_item, in_visible = in_visible, in_movable = self.movable) # The function apply to generate a geom_object
        #aux_visible is not needed in BasicMethod, keeps for aligning with ComplexMethod
        self.fun = in_fun # The numerical function to give out coordinate or equation coefficients, input self
        self.check = in_check # The numerical boolean check function, input self
        self.errorinfo = in_errorinfo # The error info output function, input self
        self.implemented = True

    def implement_check_triv(self, in_fun):
        self.implement(in_fun, lambda self: True, lambda self: "")
        
    
class ComplexMethod(Method):
    '''
    Class of complex methods, recursively create all needed geometric constructions.
    use apply to create all objects recursively, use calcc to calc all coordinates of dependending objects recursively.
    '''

    # A complex method is a series of basic or complex methods, so all correct complex methods finally breaks down into a series of basic methods. So information directly related to the creation of construction is not needed here, they are already provided in Basic Methods.

    def construct_in_item (in_item : list, m_item : list, indicator_list : list, i : int):
        '''
        Private function used in ComplexMethod only
        '''
        item_list = []
        for j in indicator_list[i]:
            if j[0] == "i":
                item_list += [in_item[j[1]]]
            if j[0] == "m":
                item_list += [m_item[j[1]]]
        return item_list

    def recursively_apply (final_name : str, in_item, method_list : list, indicator_list : list, in_visible = True, aux_visible = False):
        '''
        Private function used in ComplexMethod only
        '''
        m_item = []
        for i in range(len(method_list)):
            item_list = ComplexMethod.construct_in_item(in_item, m_item, indicator_list, i) 
            if i == len(method_list) - 1:
                return method_list[i].apply(final_name, item_list, in_visible = in_visible, aux_visible = aux_visible) ## return the last object
            else:
                m_item += [method_list[i].apply(None, item_list, in_visible = aux_visible, aux_visible = aux_visible)]


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

    '''
    An example of indicator list and method list:
    in_item : b c,    
    a = f b c
    d = g a b
    indicator_list : [("i",0), ("i",1)], [("m",0), ("i",0)]
    method_list : ["f", "g"]
    '''

class GraphTree:
    '''
    stores all objs created
    '''
    def __init__(self):
        self.obj_list = []
    
    # def get_totally_free(self):
    #     r = []
    #     for obj in self.obj_list:
    #         if obj.item == []:
    #             r += [obj]
    #     return r
    
    def get_has_free(self):
        r = []
        for obj in self.obj_list:
            if not (obj.freec == None):
                r += [obj]
        return r
    
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
    
    def calc_all(self):
        for obj in self.obj_list:
            obj.calcc()
    
    def disturb_all(self, ds = disturb_strength):
        for obj in self.obj_list:
            obj.disturb(ds)


####################
##    Methods     ##
####################

'''
The Global Dictionary of all methods. All methods should be included here. Format:
key : unique name
query : List( cmd name : str , Method itself, input_type_list, output_type_list)

All methods will be add to this dict automatically once the are created.
'''
MethodDict = {}

free_pt = BasicMethod("free_pt", ["Point"], [], "pt", in_movable=True)
free_pt_fun = lambda self : self.freec
free_pt.implement_check_triv(free_pt_fun)

line = BasicMethod("line", ["Line"], ["Point", "Point"], "line")
line_check = lambda self : (abs(self.item[0].c[0] - self.item[1].c[0]) > ERROR) or (abs(self.item[0].c[1] - self.item[1].c[1]) > ERROR)
line_errorinfo = lambda self: "Point " + self.item[0].name + " and Point " + self.item[1].name + " coincide" if not(line_check(self.in_name, self.item)) else ""
line_fun = lambda self: (self.item[0].c[1] - self.item[1].c[1], self.item[1].c[0] - self.item[0].c[0], self.item[0].c[0] * self.item[1].c[1] - self.item[1].c[0] * self.item[0].c[1])
line.implement(line_fun, line_check, line_errorinfo)

pt_on_line = BasicMethod("pt_on_line", ["Point"], ["Line"], "pt", in_movable=True)
pt_on_line_fun = lambda self : (self.item[0].item[0].c[0] + (self.item[0].item[1].c[0] - self.item[0].item[0].c[0]) * self.freec, self.item[0].item[0].c[1] + (self.item[0].item[1].c[1] - self.item[0].item[0].c[1]) * self.freec)
pt_on_line.implement_check_triv(pt_on_line_fun)

circle = BasicMethod("circle", ["Circle"], ["Point", "Point"], "circ")
circle_fun = lambda self: (self.item[0].c[0], self.item[0].c[1], ((self.item[0].c[0] - self.item[1].c[0])**2 + (self.item[0].c[1] - self.item[1].c[1])**2)**(1/2))
circle.implement_check_triv(circle_fun)

pt_on_circle = BasicMethod("pt_on_circle", ["Point"], ["Circle"], "pt", in_movable=True)
pt_on_circle_fun = lambda self : (self.item[0].item[0].c[0] - self.item[0].item[0].c[0] * math.cos(self.freec) + self.item[0].item[1].c[0] * math.cos(self.freec) + self.item[0].item[0].c[1] * math.sin(self.freec) - self.item[0].item[1].c[1] * math.sin(self.freec), self.item[0].item[0].c[1] - self.item[0].item[0].c[1] * math.cos(self.freec) + self.item[0].item[1].c[1] * math.cos(self.freec) - self.item[0].item[0].c[0] * math.sin(self.freec) + self.item[0].item[1].c[0] * math.sin(self.freec))
pt_on_circle.implement_check_triv(pt_on_circle_fun)

circle_center = BasicMethod("circle_center", ["Point"], ["Circle"], "mdpt")
circle_center_fun = lambda self: (self.item[0].c[0], self.item[0].c[1])
circle_center.implement_check_triv(circle_center_fun)

inx_line_line = BasicMethod("inx_line_line", ["Point"], ["Line", "Line"], "pt")
inx_line_line_check = lambda self: abs(self.item[0].c[0] * self.item[1].c[1] - self.item[0].c[1] * self.item[1].c[0]) > ERROR
inx_line_line_errorinfo = lambda self: "Line " + self.item[0].name + " and Line " + self.item[1].name + " are parallel" if not(inx_line_line_check(self)) else ""
inx_line_line_fun = lambda self: ((self.item[0].c[1] * self.item[1].c[2] - self.item[0].c[2] * self.item[1].c[1]) / (self.item[0].c[0] * self.item[1].c[1] - self.item[0].c[1] * self.item[1].c[0]), (self.item[0].c[2] * self.item[1].c[0] - self.item[0].c[0] * self.item[1].c[2]) / (self.item[0].c[0] * self.item[1].c[1] - self.item[0].c[1] * self.item[1].c[0]))
inx_line_line.implement(inx_line_line_fun, inx_line_line_check, inx_line_line_errorinfo)

inx_fig_fig_check = lambda self: len(fig_intersection(self.item[0].c, self.item[0].type, self.item[1].c, self.item[1].type)) > 0
inx_fig_fig_errorinfo = lambda self: self.item[0].type + " " + self.item[0].name + " and " + self.item[1].type + " " + self.item[1].name + " do not intersect" if not(inx_fig_fig_check(self)) else ""
inx_line_circle_close = BasicMethod("inx_line_circle_close", ["Point"], ["Line", "Circle"], "pt")
def inx_line_circle_close_fun(self):
    inxptlist = fig_intersection(self.item[0].c, "Line", self.item[1].c, "Circle")
    if len(inxptlist) == 1:
        return inxptlist[0]
    else:
        if ((inxptlist[0][0] * -self.item[0].c[1] + inxptlist[0][1] * self.item[0].c[0]) > (inxptlist[1][0] * -self.item[0].c[1] + inxptlist[1][1] * self.item[0].c[0])) ^ ((self.item[0].item[0].c[0] * -self.item[0].c[1] + self.item[0].item[0].c[1] * self.item[0].c[0]) > (self.item[0].item[1].c[0] * -self.item[0].c[1] +self.item[0].item[1].c[1] * self.item[0].c[0])):
            return inxptlist[1]
        else:
            return inxptlist[0]
inx_line_circle_close.implement(inx_line_circle_close_fun, inx_fig_fig_check, inx_fig_fig_errorinfo)

inx_line_circle_far = BasicMethod("inx_line_circle_far", ["Point"], ["Line", "Circle"], "pt")
def inx_line_circle_far_fun(self):
    inxptlist = fig_intersection(self.item[0].c, "Line", self.item[1].c, "Circle")
    if len(inxptlist) == 1:
        return inxptlist[0]
    else:
        if ((inxptlist[0][0] * -self.item[0].c[1] + inxptlist[0][1] * self.item[0].c[0]) > (inxptlist[1][0] * -self.item[0].c[1] + inxptlist[1][1] * self.item[0].c[0])) ^ ((self.item[0].item[0].c[0] * -self.item[0].c[1] + self.item[0].item[0].c[1] * self.item[0].c[0]) > (self.item[0].item[1].c[0] * -self.item[0].c[1] +self.item[0].item[1].c[1] * self.item[0].c[0])):
            return inxptlist[0]
        else:
            return inxptlist[1]
inx_line_circle_far.implement(inx_line_circle_far_fun, inx_fig_fig_check, inx_fig_fig_errorinfo)

inx_circle_circle_pos = BasicMethod("inx_circle_circle_pos", ["Point"], ["Circle", "Circle"], "pt")
def inx_circle_circle_pos_fun(self):
    inxptlist = fig_intersection(self.item[0].c, "Circle", self.item[1].c, "Circle")
    if len(inxptlist) == 1:
        return inxptlist[0]
    else:
        if -inxptlist[0][1] * self.item[0].c[0] + inxptlist[0][0] * self.item[0].c[1] + inxptlist[0][1] * self.item[1].c[0] - self.item[0].c[1] * self.item[1].c[0] - inxptlist[0][0] * self.item[1].c[1] + self.item[0].c[0] * self.item[1].c[1] >= 0:
            return inxptlist[0]
        else:
            return inxptlist[1]
inx_circle_circle_pos.implement(inx_circle_circle_pos_fun, inx_fig_fig_check, inx_fig_fig_errorinfo)

mid_pt = BasicMethod("mid_pt", ["Point"], ["Point", "Point"], "mdpt")
mid_pt_fun = lambda self: ((self.item[0].c[0] + self.item[1].c[0]) / 2, (self.item[0].c[1] + self.item[1].c[1]) / 2)
mid_pt.implement_check_triv(mid_pt_fun)

para_line_pt = BasicMethod("para_line_pt", ["Point"], ["Point", "Line"], "parapt")
para_line_pt_fun = lambda self: (self.item[0].c[0] + self.item[1].item[1].c[0] - self.item[1].item[0].c[0], self.item[0].c[1] + self.item[1].item[1].c[1] - self.item[1].item[0].c[1])
para_line_pt.implement_check_triv(para_line_pt_fun)

para_line = ComplexMethod("para_line", ["Point", "Line"], ["Point", "Point"], "para")
para_line_method_list = [para_line_pt, line]
para_line_indicator_list = [[("i",0), ("i",1)], [("i",0), ("m",0)]]
para_line.implement(para_line_method_list, para_line_indicator_list)

perp_line_pt = BasicMethod("perp_line_pt", ["Point"], ["Point", "Line"], "parapt")
perp_line_pt_fun = lambda self: (self.item[0].c[0] + self.item[1].item[0].c[1] - self.item[1].item[1].c[1], self.item[0].c[1] + self.item[1].item[1].c[0] - self.item[1].item[0].c[0])
perp_line_pt.implement_check_triv(perp_line_pt_fun)

perp_line = ComplexMethod("perp_line", ["Point", "Line"], ["Point", "Point"], "para")
perp_line_method_list = [perp_line_pt, line]
perp_line_indicator_list = [[("i",0), ("i",1)], [("i",0), ("m",0)]]
perp_line.implement(perp_line_method_list, perp_line_indicator_list)

'''
# Old Versions of para and perp as Basic Methods

para_line = BasicMethod("para_line", ["Line"], ["Point", "Line"], "para")
para_line_fun = lambda self: (self.item[1].c[0], self.item[1].c[1], -self.item[1].c[0] * self.item[0].c[0] - self.item[1].c[1] * self.item[0].c[1])
para_line.implement_check_triv(para_line_fun)

perp_line = BasicMethod("perp_line", ["Line"], ["Point", "Line"], "perp")
perp_line_fun = lambda self: (self.item[1].c[1], -self.item[1].c[0], -self.item[1].c[1] * self.item[0].c[0] + self.item[1].c[0] * self.item[0].c[1])
perp_line.implement_check_triv(perp_line_fun)
'''

angle_bis_pt = BasicMethod("angle_bis_pt", ["Point"], ["Point", "Point", "Point"], "abispoint")
angle_bis_pt_check = lambda self: ((abs(self.item[0].c[0] - self.item[1].c[0]) > ERROR) or (abs(self.item[0].c[1] - self.item[1].c[1]) > ERROR)) and ((abs(self.item[2].c[0] - self.item[1].c[0]) > ERROR) or (abs(self.item[2].c[1] - self.item[1].c[1]) > ERROR))
angle_bis_pt_errorinfo = lambda self: "Point " + self.item[0].name + " and Point " + self.item[1].name + " and Point " + self.item[2].name + " do not form an angle" if not(angle_bis_pt_check(self)) else ""
def angle_bis_pt_fun(self):
    deltax1 = self.item[0].c[0] - self.item[1].c[0]
    deltay1 = self.item[0].c[1] - self.item[1].c[1]
    len1 = (deltax1 * deltax1 + deltay1 * deltay1) ** (1/2)
    deltax1 /= len1
    deltay1 /= len1
    deltax2 = self.item[2].c[0] - self.item[1].c[0]
    deltay2 = self.item[2].c[1] - self.item[1].c[1]
    len2 = (deltax2 * deltax2 + deltay2 * deltay2) ** (1/2)
    deltax2 /= len2
    deltay2 /= len2
    midx = (deltax1 + deltax2) / 2
    midy = (deltay1 + deltay2) / 2
    if (abs(midx) > ERROR) or (abs(midy) > ERROR):
        len3 = (midx * midx + midy * midy) ** (1/2)
        return (self.item[1].c[0] + midx/len3, self.item[1].c[1] + midy/len3)
    else:
        return (self.item[1].c[0] - deltay1, self.item[1].c[1] + deltax1)
angle_bis_pt.implement(angle_bis_pt_fun, angle_bis_pt_check, angle_bis_pt_errorinfo) 


angle_bis = ComplexMethod("angle_bis", ["Point", "Line"], ["Point", "Point", "Point"], "abis")
angle_bis_method_list = [angle_bis_pt, line]
angle_bis_indicator_list = [[("i",0), ("i",1), ("i",2)], [("i",1), ("m",0)]]
angle_bis.implement(angle_bis_method_list, angle_bis_indicator_list)


######################
## Methods from txt ##
######################
'''
Create methods from txt files. Example input txt:

circum_center "circ_cent" O : Point 
A B C : Point Point Point 
l1 = perp_bis A B, l2 = perp_bis A C, O = inx_line_line l1 l2 
    # this line is left for DD

will be convert to method defined as follow:

circum_center = ComplexMethod("circum_center", ["Line", "Line", "Point"], ["Point", "Point", "Point"], "circ_cent")
circum_center_method_list = [perp_bis, perp_bis, inx_line_line]
circum_center_indicator_list = [[("i",0), ("i",1)], [("i",0), ("i",2)], [("m",0), ("m",1)]]
circum_center.implement(circum_center_method_list, circum_center_indicator_list)

'''
comment_marker = "#"
cmd_marker = '"'
construction_seperator = ","
file_path = "Construction.txt"

def split_to_info( lines:list ):
    rlist = [] 
    new_method = True
    for l in lines :
        r = l.split(comment_marker)[0] #delete comments
        words0 = r.split() #split each line into words
        words = []
        for w in words0: # deal with construction seperator
            if len(w) >= len(construction_seperator)+1 and w[-len(construction_seperator):] == construction_seperator:
                words.append(w[:-1])
                words.append(construction_seperator) 
            else:
                words.append(w)
        if words == [] :
            new_method = True
            continue
        if new_method :
            new_method = False
            rlist += [[words]] 
        else:
            rlist[-1] += [words]
    return rlist # a list, each term corresponds to a new method. each term is a list of lines, each line is a list of words 

def name_to_indicator (ilist:list, mlist:list, name:str):
    if name in ilist:
        return ("i",ilist.index(name))
    else:
        return ("m",mlist.index(name))

def info_to_method ( info : list) :
    try:
        method_name = info[0][0]
        cmd_name = info[0][1].strip(cmd_marker)
        final_name = info[0][2]
        final_type = info[0][4] 
        input_num = info[1].index(":")
        input_name = info[1][:input_num]
        input_type = info[1][input_num+1:]
        construction0 = info[2].copy()
        construction_seq = [] #list of [var_name, method_name, mid_input_name]
        if not (construction0[-1] == construction_seperator):
            construction0.append(construction_seperator)
        while len(construction0) > 0:
            i = construction0.index(construction_seperator)
            construction_seq.append([construction0[0],construction0[2],construction0[3:i]])
            if not (i == len(construction0)):
                construction0 = construction0[i+1:]
            else:
                construction0 = []

        mid_name = [m[0] for m in construction_seq]
        mid_method_name = [m[1] for m in construction_seq]
        mid_item_name = [m[2] for m in construction_seq]
        mid_method = [MethodDict[mn][1] for mn in mid_method_name]
        mid_item_type = [MethodDict[mn][2] for mn in mid_method_name]
        mid_type = [MethodDict[mn][3][-1] for mn in mid_method_name]

        indicator_list = mid_item_name.copy()
        for i in range(len(indicator_list)):
            for j in range(len(indicator_list[i])):
                indicator_list[i][j] = name_to_indicator(input_name, mid_name,indicator_list[i][j])

        # need some more checks here, check each mid construction is legal in type
        if not (mid_type[-1] == final_type) or not (mid_name[-1] == final_name):
            raise ValueError("final construction do not meet requirements")
        
        new_method = ComplexMethod(method_name, mid_type, input_type, cmd_name)
        new_method.implement(mid_method, indicator_list)
        return new_method
    except Exception as e:
        print("Input method is not legal!" + str(e))
        print(info)

with open(file_path) as file:
    lines = file.readlines() # list of lines

info_list = split_to_info(lines)

for info in info_list:
    method = info_to_method(info)
    print(method.name + " is implemented from " + file_path)

'''
The global variable of GraphTree is created here, use in other file as GeomTool.current_tree.
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
    l1 = MethodDict["perp_bis"][1].apply("l1", [p1, p2])
    print("l1 created", l1)
    l = line.apply("l", [p1, p3])
    print("l created")
    o = MethodDict["circum_center"][1].apply("o", [p1, p2, p4])
    print("o created")
    i = angle_bis.apply("i", [p1, p2, p4])
    print("i created")
    l1.calcc()
    print("l1 calculated", l1.hasc, l1.c)
    o.calcc()
    print("o calculated", o.hasc, o.c)
    i.calcc()
    print("i calculated", i.hasc, i.c)
    print("the following points directly depends on p1")
    print( [i.name for i in p1.affect_item] )
    current_tree.calc_all()
    print("all objs:")
    print([i.name for i in current_tree.obj_list])
    print( [i.c for i in current_tree.obj_list])
    p1.disturb()
    print("after disturb p1")
    print( [i.name for i in current_tree.obj_list] )
    print( [i.c for i in current_tree.obj_list])
    current_tree.disturb_all()
    print("after disturb all")
    print( [i.name for i in current_tree.obj_list] )
    print( [i.c for i in current_tree.obj_list])
    