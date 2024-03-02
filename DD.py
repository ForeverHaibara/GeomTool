import GeomTool

NodeTypeList = ['pt', 'line', 'dist', 'ang'] # geom obj
PredicateDict = {
    'coll' : ['Point', 'Point', 'Point'], 
    'cong' : ['dist', 'dist']
}

class DDNode:
    NotImplemented

class DDTree:
    '''
    It should provide 4 basic function: 
    1. remembers how a result is deduced
    2. quickly search whether a conclusion is already deduced
    3. deduce one more conclusion based on user input
    4. remember each point/line corresponds to which obj in graph to enable calculation
    in future it should 
    3'. deduces all possible conclusions, remember the depth of deduction 

    In order to do this, it should maintain several list for quick search.

    In this version, all result will be stated using points.
    '''
    NotImplemented

def Graph_to_DD (graph : GeomTool.GraphTree):
    '''
    create and return a DDTree
    '''
    NotImplemented

'''
adding a construction should be add simuteniously to graph and DDTree.
'''