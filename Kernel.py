import Explainer, GeomTool

def runline(in_line, in_graph_tree):
    try:
        ev = eval(in_line)
        return str(ev)
    except:
        pass
    
    exp = Explainer.ExplainLine(in_line, in_graph_tree.obj_list)
    if len(exp.wordlist) == 0:
        return ""
    
    if len(exp.wordlist) == 1 and exp.isnameobj(exp.wordlist[0]) != None:
        return str(exp.isnameobj(exp.wordlist[0]))
    
    kerneluse = exp.kerneluse()
    if kerneluse not in (None, []):
        defaultname = GeomTool.default_name(kerneluse[0].gen_type[0])
        newobj = kerneluse[0].apply(defaultname, kerneluse[1])
        if newobj.check():
            newobj.calcc()
        
        if len(kerneluse) == 2:       
            pass
        if len(kerneluse) > 2 and kerneluse[0].name == "free_pt":
            newobj.c = (kerneluse[2], kerneluse[3])
        
        return defaultname + ' is created'
        
    
    return "Failed to run '" + in_line + "'" # Should return information want to print