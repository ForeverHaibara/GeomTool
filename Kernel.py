import Explainer, GeomTool

def runline(in_line, in_graph_tree):
    
    exp = Explainer.ExplainLine(in_line, in_graph_tree.obj_list)
    if len(exp.wordlist) == 1 and exp.isnameobj(exp.wordlist[0]) != None:
        return str(exp.isnameobj(exp.wordlist[0]))
    
    kerneluse = exp.kerneluse()
    if kerneluse not in (None, []):
        defaultname = GeomTool.default_name(kerneluse[0].gen_type[0])
        newobj = kerneluse[0].apply(defaultname, kerneluse[1])
        if newobj.check():
            newobj.calcc()
        return defaultname + ' is created'
        
        
    
    return "" # Should return information want to print