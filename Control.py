import random, math

class ObjBase : 
    def __init__(self) -> None:
        pass

class GeomObj(ObjBase):
    def __init__(self, in_name, in_type, in_method, in_item):
        super().__init__()
        NotImplemented

class DPNode(GeomObj):
    def __init__(self, in_name, in_type, in_method, in_item):
        super().__init__(in_name, in_type, in_method, in_item)

class RelationObj(ObjBase):
    def __init__(self) -> None:
        super().__init__()

class DDNode(ObjBase):
    def __init__()
class Action: 
    def __init__(self, fn: function, parameter: list) -> None:
        self.action = fn
        self.parameter = parameter

    def perform(self):
        self.action.apply(*self.parameter)

class Construction(Action):
    def __init__(self, functions: list, parameters: list) -> None:
        super().__init__(functions, parameters)
    
class ModifyDPGraph(Action):
    def __init__(self, functions: list, parameters: list) -> None:
        super().__init__(functions, parameters)

class ModifyDD(Action):
    def __init__(self, functions: list, parameters: list) -> None:
        super().__init__(functions, parameters)

class FullAction

# the coordinate of the points will not be calculated until one calls function calcc of every object


'''
class DDNode:
    def __init__(self, obj:ObjBase):
        self.obj = obj
        self.parent
'''

## The acyclic graph, nodes as geom objs, edge from a to b if the construction of a depends on b
        ## self.item [0] = name : str, self.item[i>0] : geomobj

class DPNode:
    def __init__(self, obj : GeomObj, dplist: list):
        self.obj = obj
        self.parent_list = dplist ## all directly depending nodes to create this node
        for i in self.parent_list: ## check that dp list is the same as 
            if not (i.obj in self.obj.item) :
                print("Error, dependecy list is not a sublist of GeomObj.item")
        self.affect_list = [] ## all other nodes that depends on this node
        for i in self.dp_list: 
            i.affect_list += [self] 

    ## rewrite this to GeomObj class, not here
    def root() : return DPNode (None, [], "") ## the root DPNode has no corresponding object 

    def __repr__(self, level = 0) -> str: 
        if level == 0:
            ret = self.obj.item[0] + "\n"
        else:
            ret = "\t" * (level - 1) + "--" + self.obj.item[0] + "\n"
        for i in self.affect_list:
            ret += i.__repr__(level + 1)
        return ret

class DPGraph:
    def __init__(self) -> None:
        self.root = DPNode.root()

    def hasfree(self):
        ## return a list of nodes has free
        return None

    def totallyfree(self):
        ## return a list of nodes is directly linked to root
        return None
    
    def __repr__(self) -> str:
        return self.root.__repr__()


class ConstructionAction:
    def __init__(self,in_name, in_gen_type, in_item_type) -> None:
        pass

    def generate(self, in_fun, in_check, in_errorinfo):
        pass

    def generate_check_triv(self, in_fun):
        pass

class DependencyAction:
    def __init__(self) -> None:
        pass

    def applyto (dptree : DependencyTree) -> None

class FullAction(ConstructionAction):

## we need function input string output Construction + Dependency

