import random, math

'''
A temporory naming choice. Please rewrite this once dependency is finished.
'''

name_counter = 100
def default_name (Type : str) : 
    name_counter += 1
    if Type == "Point":
        return "p"+str(name_counter)
    if Type == "Line":
        return "l"+str(name_counter)
    if Type == "Circle":
        return "c"+str(name_counter)
    else:
        return "NoName"
    
    

class GeomObj:
    def __init__(self, in_name, in_type, in_method, in_item, in_tree = None):
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
        if in_tree == None:
            if in_item == []:
                print("Error, init of free object must provide a tree!")
            self.tree = in_item[0].tree
        else:
            self.tree = in_tree
        print("init_run", self.name)

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

    def check(self):
        if len(self.item) != len(self.method.item_type):
            return False
        for item_num in range(len(self.item)):
            if self.method.item_type[item_num] != "Others" and self.item[item_num].type != self.method.item_type[item_num]:
                return False
            if not self.method.item_type[item_num].hasc:
                return False
        return self.method.check(self)
    
    def errorinfo(self):
        if len(self.item) != len(self.method.item_type):
            return "Method supposed to use " + str(len(self.method.item_type)) + " Items but got " + str(len(self.item))
        for item_num in range(len(self.item)):
            if self.method.item_type[item_num ] != "Others" and self.item[item_num].type != self.method.item_type[item_num ]:
                return "Item " + str(item_num) + " supposed to be Type " + self.method.item_type[item_num ] + " but got " + self.item[item_num].type
            if not self.method.item_type[item_num].hasc:
                return "Item " + str(item_num) + " not computed"
        return self.method.errorinfo(self)
    
    
class Method:
    def __init__(self, in_name, in_gen_type : list, in_item_type : list):
        self.name = in_name # Name of the method
        self.gen_type = in_gen_type # Type of the generated object(s), still a list even when generate a single object
        self.item_type = in_item_type # Type of the used items
        self.implimented = False # turn True once apply and calculation method is provided
        self.apply = None
        self.fun = None
        self.check = None
        self.errorinfo = None

class BasicMethod(Method):
    '''
    Basic Geometic construction methods class. Creates only one object. Stores dependency information.
    '''
    def __init__(self, in_name, in_gen_type: list, in_item_type: list):
        super().__init__(in_name, in_gen_type, in_item_type)
        if len(in_gen_type) != 1:
            print("Error during init " + in_name + " method, Basic method must create exactly one object!")

    def implement(self, in_fun, in_check, in_errorinfo): # fill more information needed
        self.apply = lambda in_name, in_item: GeomObj(in_name, self.gen_type[0], self, in_item) # The function apply to generate a geom_object
        self.fun = in_fun # The numerical function to give out coordinate or equation coefficients, input self
        self.check = in_check # The numerical boolean check function, input self
        self.errorinfo = in_errorinfo # The error info output function, input self

    def implement_check_triv(self, in_fun):
        self.apply = lambda in_name, in_item: GeomObj(in_name, self.gen_type[0], self, in_item) # The function apply to generate a geom_object with trivial nondegenerate condition
        self.fun = in_fun
        self.check = lambda self: True # Trivial check
        self.errorinfo = lambda self: "" # Trivial errorinfo





        
    
class ComplexMethod(Method):

    def construct_in_item (in_item : list, m_item : list, indicator_list : list, i : int):
        item_list = []
        for j in indicator_list[i]:
            if j[0] == "i":
                item_list += in_item[j[1]]
            if j[0] == "m":
                item_list += m_item[j[1]]
        return item_list

    def recursively_apply (final_name : str, in_item, method_list : list, indicator_list : list):
        m_item = []
        for i in len(method_list):
            item_list = ComplexMethod.construct_in_item(in_item, m_item, indicator_list, i)
            if isinstance(method_list[i], BasicMethod) :
                
                m_item += [method_list[i].apply (name = None, ...)]
    '''
    Class of complex methods, recursively create all needed geometric constructions.
    use apply to create all objects recursively, use calc to calc all coordinates of dependending objects recursively
    '''
    def __init__(self, in_name, in_gen_type: list, in_item_type: list):
        super().__init__(in_name, in_gen_type, in_item_type)
        
    def implement(self, in_method_list, in_indicator_list):
        if (len(in_method_list) != len(self.gen_type)) or (len(in_indicator_list) != len(self.gen_type)):
            print("Error during implement " + self.name + " method, length of method list, gen type, indicator list do NOT match !")
        self.method_list = in_method_list
        self.indicator_list = in_indicator_list
        self.apply = lambda in_name, in_item : recursively_apply(in_name, in_item, self.method_list, self.indicator_list)

## in_item : b c,    
## a = f b c
## d = g a b
## indicator_list : [("i",0), ("i",1)], [("m",0), ("i",0)]
## method_list : ["f", "g"]

class GraphTree:
    def __init__(self):
        self.root = create_empty(self) 
        self.obj_list = [self.root]

    
    