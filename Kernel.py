import Explainer, GeomTool, Pathfinder, GradientDescent

def runline(in_line, in_UI):

    in_graph_tree = in_UI.graph_tree
    all_lines = in_UI.cmdlines
    line_from = in_UI.cmdline_from
    
    in_line = in_line + ' '
    exp = Explainer.ExplainLine(in_line, in_graph_tree.obj_list)
    protectedwordlist = ["=", ".", "+", "-", "*", "/", "?", ",", "!", "^", " ", "'", '"', "help", "hide", "hidenlist", "show", "showall", "objlist", "run", "save", "disturb", "clearall", "lock", "lockall", "unlock", "unlockall", "descent", "methods", 
                         "pt", "line", "circ", "mdpt", "para", "perp", "pbis", "abis"]
    
    if len(exp.wordlist) == 0:
        return ""
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "help":
        return "Commands list: help, hide, hidenlist, show, showall, objlist, run, save, disturb, clearall, lock, lockall, unlock, unlockall. \nUse commands like 'help hide' to see details. \nUse 'help1' to get help about built-in constructions. "
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "help1":
        return "Built-in constructions list: pt, line, circ, mdpt, para, perp, pbis, abis. \nUse commands like 'help pt' to see details. \nYou can also input the name of an object to see details of the object. \nUse commands like 'A = B' to rename object B by A. Use commands like 'A = pt' to create an object with given name. \nUse 'help2' to see more. "
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "help2":
        return "For point, c = (x, y) is the coordinate of the point. \nFor line, c = (p, q, r) defines a line equation px+qy+r=0. \nAnd for circle, c = (x0, y0, r) determines the center (x0, y0) and radius r. \nUse 'help3' to see more. "
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
        if exp.wordlist[1] == "run":
            return "run [Name]: Run all lines in a txt file. "
        if exp.wordlist[1] == "save":
            return "save [Name]: Save all input lines in a txt file. Also save all cmd lines in a log file. "
        if exp.wordlist[1] == "distrub":
            return "disturb [Number]: Disturb all movable objects by a given scale, use 'disturb' to disturb by default value = 1e-4. "
        if exp.wordlist[1] == "clearall":
            return "clearall: Delete all geometric objects. "
        if exp.wordlist[1] == "lock":
            return "lock [Objects]: Lock geometric objects which is movable(free points on the plane, line or circle). When locked, you cannot move these objects by your mouse. "
        if exp.wordlist[1] == "unlock":
            return "unlock [Objects]: Unlock geometric objects which is movable(free points on the plane, line or circle). When unlocked, you can move these objects by your mouse. "
        if exp.wordlist[1] == "lockall":
            return "lockall: Lock all geometric objects which is movable(free points on the plane, line or circle). When locked, you cannot move these objects by your mouse. "
        if exp.wordlist[1] == "unlockall":
            return "unlockall: Unlock all geometric objects which is movable(free points on the plane, line or circle). When unlocked, you can move these objects by your mouse. "
        if exp.wordlist[1] == "methods":
            return "methods: Print a list of all methods, (the geometric constructions, including those implemented). "


        if exp.wordlist[1] == "pt":
            return "pt [Number] [Number]: Create a free point. \npt [Line/Circle] [Number] [Number]: Create a free point on a line/circle. \npt [Line/Circle] [Line/Circle] [Number] [Number]: Create the intersection point of a line/circle and another line/circle. The two numbers give the (x, y) coordinate of the closest intersection point. \n<NOTE> In the case of two lines, since the intersection point is unique, coordinate could be omitted. Use pt [Line] [Line] in this case. "
        if exp.wordlist[1] == "line":
            return "line [Point] [Point]: Create a line passing through the two points. "
        if exp.wordlist[1] == "circ":
            return "circ [Point] [Point]: Create a circle whose center is the first point and passing through the second point. "
        if exp.wordlist[1] == "mdpt":
            return "mdpt [Point] [Point]: Create the mid-point of two points. \nmdpt [Circle]: Create the circumcenter of a circle. "
        if exp.wordlist[1] == "para":
            return "para [Point] [Line], para [Line] [Point]: Create a line passing through the point and parallel to the line. "
        if exp.wordlist[1] == "perp":
            return "perp [Point] [Line], perp [Line] [Point]: Create a line passing through the point and perpendicular to the line. "
        if exp.wordlist[1] == "pbis":
            return "pbis [Point] [Point]: Create the perpendicular bisector of the two points. "
        if exp.wordlist[1] == "abis":
            return "abis [Point] [Point] [Point]: Create the angle bisector line of the angle formed by the three points. "
        
    
    if len(exp.wordlist) == 2 and exp.wordlist[0] == "run":
        return runfile(exp.wordlist[1], in_UI)
    
    if len(exp.wordlist) == 2 and exp.wordlist[0] == "save":
        try:
            file = open(exp.wordlist[1] + ".txt", "w")
            wrdata = ""
            for line_num in range(len(all_lines) - 1):
                if line_from[line_num] == 1:
                    wrdata += all_lines[line_num] + "\n"
            file.write(wrdata)
            file.close()
            file2 = open(exp.wordlist[1] + "_log.txt", "w")
            wrdata = ""
            for line_num in range(len(all_lines)):
                if line_from[line_num] == 1:
                    wrdata += ">>> " + all_lines[line_num] + "\n"
                else:
                    wrdata += "GT: " + all_lines[line_num] + "\n"
            file2.write(wrdata)
            file2.close()
            return "saved to file " + exp.wordlist[1] + ".txt and " + exp.wordlist[1] + "_log.txt"
        except Exception as e:
            return "ΔError with info: " + str(e)
    
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

    if len(exp.wordlist) == 1 and exp.wordlist[0] == "methods":
        outstr = ''
        for method in GeomTool.MethodDict:
            outstr += 'method name = ' + method + ', cmd name = ' + GeomTool.MethodDict[method][0] + '\n'
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
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "clearall":
        newtree = GeomTool.GraphTree()
        GeomTool.current_tree = newtree
        in_UI.graph_tree = newtree
        in_UI.geom_list = newtree.obj_list
        in_UI.geom_chosen = []
        in_UI.geom_picked_list = []
        return "All objects are deleted"
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "disturb":
        in_graph_tree.disturb_all()
        return "All movable objects disturbed"

    if len(exp.wordlist) == 2 and exp.wordlist[0] == "disturb" and Explainer.is_float(exp.wordlist[1]):
        in_graph_tree.disturb_all(float(exp.wordlist[1]))
        return "All movable objects disturbed"
    
    if len(exp.wordlist) >= 2 and exp.wordlist[0] == "descent":
        descent_datum = exp.descent_conditions()
        timer = GradientDescent.descent(descent_datum, in_graph_tree)
        return "Tried " + str(timer) + " times"
    
    """------------
    !!!   NEW   !!!---------------------------------------+----
    ------------"""
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "eq":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.eq()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "eqdist":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.eqdist()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "col":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.col()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "para":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.para()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "cyc":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.cyc()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "simtri":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.simtri()
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "simtri0":
        finder = Pathfinder.GeomInformation(in_graph_tree, disturb=True)
        return finder.simtri()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "eqarea":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.eqarea()
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "eqarea0":
        finder = Pathfinder.GeomInformation(in_graph_tree, disturb=True)
        return finder.eqarea()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "eqratio":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.eqratio()
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "eqratio0":
        finder = Pathfinder.GeomInformation(in_graph_tree, disturb=True)
        return finder.eqratio()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "eqangle":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.eqangle()
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "eqangle0":
        finder = Pathfinder.GeomInformation(in_graph_tree, disturb=True)
        return finder.eqangle()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "cheat":
        finder = Pathfinder.GeomInformation(in_graph_tree)
        return finder.eq() + "\n" + finder.col() + "\n" + finder.cyc() + "\n" + finder.para() + "\n" + finder.simtri() + "\n" + finder.eqdist() # + "\n" + finder.eqarea() + "\n" + finder.eqratio() + "\n" + finder.eqangle()
    
    if len(exp.wordlist) == 1 and exp.wordlist[0] == "cheat0":
        finder = Pathfinder.GeomInformation(in_graph_tree, disturb=True)
        return finder.eq() + "\n" + finder.col() + "\n" + finder.cyc() + "\n" + finder.para() + "\n" + finder.simtri() + "\n" + finder.eqdist() # + "\n" + finder.eqarea() + "\n" + finder.eqratio() + "\n" + finder.eqangle()
    
    """------------
    !!!   NEW   !!!---------------------------------------+----
    ------------"""
    
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
        
    if exp.wordlist[0] == "unlock":
        outstr = ''
        for word_num in range(1, len(exp.wordlist)):
            obj = exp.isnameobj(exp.wordlist[word_num])
            if obj != None and obj.method.name in ("free_pt", "pt_on_line", "pt_on_circle"):
                obj.movable = True
                outstr += obj.name + ' '
        if outstr != '':
            return outstr + 'unlocked'
        else:
            return 'no object to unlock'
    
    if exp.wordlist[0] == "lock":
        outstr = ''
        for word_num in range(1, len(exp.wordlist)):
            obj = exp.isnameobj(exp.wordlist[word_num])
            if obj != None:
                obj.movable = False
                outstr += obj.name + ' '
        if outstr != '':
            return outstr + 'locked'
        else:
            return 'no object to lock'

    if exp.wordlist[0] == "unlockall":
        outstr = ''
        for obj in in_graph_tree.obj_list:
            if obj != None and obj.method.name in ("free_pt", "pt_on_line", "pt_on_circle"):
                obj.movable = True
                outstr += obj.name + ' '
        if outstr != '':
            return outstr + 'unlocked'
        else:
            return 'no object to unlock'
    
    if exp.wordlist[0] == "lockall":
        outstr = ''
        for obj in in_graph_tree.obj_list:
            if obj != None and obj.movable:
                obj.movable = False
                outstr += obj.name + ' '
        if outstr != '':
            return outstr + 'locked'
        else:
            return 'no object to lock'
    
    kerneluse = exp.kerneluse()
    newname = exp.newname()
    if kerneluse not in (None, []):
        if newname == None or exp.isname(exp.wordlist[0]) > 0 or exp.wordlist[0] in protectedwordlist or Explainer.is_float(exp.wordlist[0]) or ' ' in exp.wordlist[0] or '[' in exp.wordlist[0] or ']' in exp.wordlist[0] or '.' in exp.wordlist[0] or '$' in exp.wordlist[0]:
            newobj = kerneluse[0].apply( None , kerneluse[1])
            newname = newobj.name
        else:
            newobj = kerneluse[0].apply(newname, kerneluse[1])
        new_obj_check = newobj.check_and_calcc() # Bool
        
        if kerneluse[0].name in ("free_pt", "pt_on_line", "pt_on_circle"):
            if len(kerneluse) > 2:
                newobj.move((kerneluse[2], kerneluse[3]))
            else:
                newobj.check_and_calcc()
        
        return newname + ' is created'
    
    if len(exp.wordlist) == 3 and exp.wordlist[1] == "=":
        if exp.isname(exp.wordlist[2]) == -1:
            return exp.wordlist[2] + " is not an object name"
        elif exp.isname(exp.wordlist[0]) > 0:
            return exp.wordlist[0] + " is already an object name"
        elif exp.wordlist[0] in protectedwordlist or Explainer.is_float(exp.wordlist[0]) or ' ' in exp.wordlist[0] or '[' in exp.wordlist[0] or ']' in exp.wordlist[0] or '.' in exp.wordlist[0] or '$' in exp.wordlist[0]:
            return exp.wordlist[0] + " can not be an object name"
        else:
            exp.isnameobj(exp.wordlist[2]).name = exp.wordlist[0]
            return "Name changed"
    
    try:
        if len(exp.wordlist) == 1 and exp.wordtype(exp.wordlist[0]) == "Formula":
            return str(Explainer.calculate(exp.wordlist[0], in_graph_tree.obj_list))
        ev = eval(in_line)
        return str(ev)
    except Exception as e:
        return "Failed to run '" + in_line[:-1] + "', use 'help' for help" # Should return information want to print

def runfile(file_name, in_UI):
    all_lines = in_UI.cmdlines
    line_from = in_UI.cmdline_from
    all_lines.pop()
    line_from.pop()
    try:
        if file_name[-4:] != '.txt':
            file_name = file_name + '.txt'
        # 打开文件并逐行读取内容
        with open(file_name, 'r') as file:
            lines = file.readlines()
            
        # 输出每一行的内容
        outstr = ""
        for line in lines:
            if line[0] != "#":
                all_lines.append(line[:-1])
                line_from.append(1)
                all_lines.append(runline(line.replace('\n', '') + ' ', in_UI))
                line_from.append(0)
        return "Done"
    
    except FileNotFoundError:
        return "File " + file_name + " do not Exist"
    except Exception as e:
        return "ΔError with info: " + str(e)