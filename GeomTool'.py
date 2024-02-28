import random, math

class Geom_object:
    def __init__(self, in_name, in_type, in_method, in_item):
        self.name = in_name # Name of the object
        self.type = in_type # Type of the object
        self.method = in_method # The method used to generate the object
        self.item = in_item # The items used to generate the object
        self.hasc = False
        self.affect_item = []  #The items using this object to generate object
        for parent_item in in_item:
            parent_item.affect_item += [ self ]
        print("init_run", self.name)
    def getc(self, in_tuple):
        self.c = in_tuple # The coordinate or the equation coefficients of the object
        self.hasc = True
    def calcc(self):
        for parent_item in self.item:
            if parent_item.type != "Others" and (not parent_item.hasc):
                parent_item.calcc()
        self.c = self.method.fun(self) # Calculate the coordinate without error check and errorinfo print
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
    

    
