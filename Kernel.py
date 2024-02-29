import Explainer, GeomTool

def runline(in_line, in_graph_tree):
    
    exp = Explainer.ExplainLine(in_line, in_graph_tree.obj_list)
    
    if len(exp.wordlist) == 0:
        return ""
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "help":
        return "Commands list: help, hide, hidenlist, show, showall, objlist. Use commands like 'help hide' to see details. Use 'help1' to see built-in commands. "
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "help1":
        return "Built-in commands list: pt, line, circ, mdpt, para, perp, pbis, abis. Use commands like 'help pt' to see details. You can also input the name of an object to see details of the object. Use 'help2' to see more. "
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "help2":
        return "For points, c = (x, y) is the coordinate. For lines, c = (p, q, r) defines a line px+qy+r=0. For circles, c = (x0, y0, r) determines the center (x0, y0) and radius r. Use 'help3' to see more. "
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "help3":
        return "I cannot help you anymore! There is no royal way in geometry! "
    if len(exp.wordlist) == 2 and exp.wordlist[0] == "help":
        if exp.wordlist[1] == "help":
            return "help [Command]: Provides detailed informations for a command. "
        if exp.wordlist[1] == "hide":
            return "hide [Objects]: Hide geometric objects. Hiden objects would not be displayed on the screen. "
        if exp.wordlist[1] == "show":
            return "show [Objects]: Show geometric objects. Making these objects visible on the screen. "
        if exp.wordlist[1] == "hidenlist":
            return "hidenlist: Print a list of names of all hiden geometric objects. "
        if exp.wordlist[1] == "showall":
            return "showall: Show all geometric objects, including intermediate objects used in geometric constructions. "
        if exp.wordlist[1] == "objlist":
            return "objlist: Print a list of names of all hiden geometric objects, including intermediate objects used in geometric constructions. "
        
        if exp.wordlist[1] == "pt":
            return "pt [Number] [Number]: Create a free point. pt [Line/Circle] [Number] [Number]: Create a free point on a line/circle. pt [Line/Circle] [Line/Circle] [Number] [Number]: Create the intersection point of a line/circle and another line/circle. The two numbers give the (x, y) coordinate of the closest intersection point. <NOTE> In the case of two lines, since the intersection point is unique, coordinate could be omitted. Use pt [Line] [Line] in this case. "
        if exp.wordlist[1] == "line":
            return "line [Point] [Point]: Create a line passing through the two points. "
        if exp.wordlist[1] == "circ":
            return "circ [Point] [Point]: Create a circle whose center is the first point and passing through the second point. "
        if exp.wordlist[1] == "mdpt":
            return "mdpt [Point] [Point]: Create the mid-point of two points. mdpt [Circle]: Create the circumcenter of a circle. "
        if exp.wordlist[1] == "para":
            return "para [Point] [Line], para [Line] [Point]: Create a line passing through the point and parallel to the line. "
        if exp.wordlist[1] == "perp":
            return "perp [Point] [Line], perp [Line] [Point]: Create a line passing through the point and perpendicular to the line. "
        if exp.wordlist[1] == "pbis":
            return "pbis [Point] [Point]: Create the perpendicular bisector of the two points. "
        if exp.wordlist[1] == "abis":
            return "abis [Point] [Point] [Point]: Create the angle bisector line of the angle formed by the three points. "
        
        
    if len(exp.wordlist) == 1 and exp.isnameobj(exp.wordlist[0]) != None:
        return str(exp.isnameobj(exp.wordlist[0]))
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "objlist":
        outstr = ''
        for obj in in_graph_tree.obj_list:
            outstr += obj.name + ' '
        if outstr != '':
            return outstr[:-1]
        else:
            return "No objects"
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "hidenlist":
        outstr = ''
        for obj in in_graph_tree.obj_list:
            if obj.visible == False:
                outstr += obj.name + ' '
        if outstr != '':
            return "Hiden: " + outstr[:-1]
        else:
            return "Nothing hiden"
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "showall":
        for obj in in_graph_tree.obj_list:
            obj.visible = True
        return "All objects are shown"
    
    if exp.wordlist[0] == "show":
        outstr = ''
        for word_num in range(1, len(exp.wordlist)):
            obj = exp.isnameobj(exp.wordlist[word_num])
            if obj != None:
                obj.visible = True
                outstr += obj.name + ' '
        if outstr != '':
            return outstr + 'shown'
    
    if exp.wordlist[0] == "hide":
        outstr = ''
        for word_num in range(1, len(exp.wordlist)):
            obj = exp.isnameobj(exp.wordlist[word_num])
            if obj != None:
                obj.visible = False
                outstr += obj.name + ' '
        if outstr != '':
            return outstr + 'hiden'
    
    kerneluse = exp.kerneluse()
    if kerneluse not in (None, []):
        defaultname = GeomTool.default_name(kerneluse[0].gen_type[-1])
        newobj = kerneluse[0].apply(defaultname, kerneluse[1])
        new_obj_check = newobj.check_and_calcc() # Bool
        
        if len(kerneluse) == 2:       
            pass
        if len(kerneluse) > 2 and kerneluse[0].name == "free_pt":
            newobj.c = (kerneluse[2], kerneluse[3])
        
        return defaultname + ' is created'
        
    try:
        ev = eval(in_line)
        return str(ev)
    except:
        pass
    
    return "Failed to run '" + in_line[:-1] + "', use 'help' for help" # Should return information want to print