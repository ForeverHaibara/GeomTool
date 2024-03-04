import random
import GeomTool

# auto perturbation
PERT_NUM = 1e-6

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

def calculate(in_text, geom_list):
    for obj in geom_list:
        if obj.name + '.' in in_text or obj.name + '[' in in_text:
            if obj.hasc:
                if obj.type == "Point":
                    in_text = in_text.replace(obj.name + '.x', str(obj.c[0]))
                    in_text = in_text.replace(obj.name + '.y', str(obj.c[1]))
                    in_text = in_text.replace(obj.name + '[0]', str(obj.c[0]))
                    in_text = in_text.replace(obj.name + '[1]', str(obj.c[1]))
                if obj.type == "Line":
                    in_text = in_text.replace(obj.name + '.a', str(obj.c[0]))
                    in_text = in_text.replace(obj.name + '.b', str(obj.c[1]))
                    in_text = in_text.replace(obj.name + '.c', str(obj.c[2]))
                    in_text = in_text.replace(obj.name + '[0]', str(obj.c[0]))
                    in_text = in_text.replace(obj.name + '[1]', str(obj.c[1]))
                    in_text = in_text.replace(obj.name + '[2]', str(obj.c[2]))
                if obj.type == "Circle":
                    in_text = in_text.replace(obj.name + '.x', str(obj.c[0]))
                    in_text = in_text.replace(obj.name + '.y', str(obj.c[1]))
                    in_text = in_text.replace(obj.name + '.r', str(obj.c[2]))
                    in_text = in_text.replace(obj.name + '[0]', str(obj.c[0]))
                    in_text = in_text.replace(obj.name + '[1]', str(obj.c[1]))
                    in_text = in_text.replace(obj.name + '[2]', str(obj.c[2]))
            else:
                return None
    try:
        return eval(in_text)
    except Exception:
        return None

class ExplainLine:
    def __init__(self, in_text, geom_list):
        mode_list=["mdpt", "pt", "line", "para", "perp", "pbis", "abis", "circ"]
        inword = False
        informula = False
        word = ''
        self.wordlist = []
        self.geom_list = geom_list
        self.mode_list = mode_list
        while len(in_text) > 0:
            read_char = in_text[0]
            if informula:
                if read_char == '$':
                    informula = False
                    self.wordlist.append(word)
                    word = ''
                else:
                    word += read_char
            else:
                if read_char == '$':
                    informula = True
                else:
                    if read_char != ' ':
                        inword = True
                        word += read_char
                    if (inword and read_char == ' '):
                        inword = False
                        self.wordlist.append(word)
                        word = ''
            in_text = in_text[1:]
        self.geom_appear = []
        self.mode_appear = ""
        for word in self.wordlist:
            for geom_num in range(len(geom_list)):
                if geom_list[geom_num].name == word:
                    self.geom_appear.append(geom_num)
            if word in mode_list:
                self.mode_appear = word
                
    def isname(self, instr):
        for geom_num in range(len(self.geom_list)):
            if self.geom_list[geom_num].name == instr:
                return geom_num
        return -1
    def isnameobj(self, instr):
        for geom_num in range(len(self.geom_list)):
            if self.geom_list[geom_num].name == instr:
                return self.geom_list[geom_num]
        return None
    
    def wordtype(self, instr):
        isn = self.isname(instr)
        if isn >= 0:
            return self.geom_list[isn].type
        if is_float(instr):
            return "Number"
        if is_float(str(calculate(instr, self.geom_list))):
            return "Formula"
        return None
    
    def newname(self):
        for word_num in range(len(self.wordlist)):
            if self.wordlist[word_num] == "=" and word_num > 0:
                return self.wordlist[word_num - 1]
        return None
    
    def kerneluse(self):

        MethodList = list(GeomTool.MethodDict.values())
        NewMethodDict = dict()
        for term in MethodList:
            if term[0] in NewMethodDict:
                NewMethodDict[term[0]].append([term[1], term[2], term[3]])
            else:
                NewMethodDict[term[0]] = [[term[1], term[2], term[3]]]

        mode_name = ""

        word_num = -1
        for word_num in range(len(self.wordlist)):
            if self.wordlist[word_num] in self.mode_list:
                mode_name = self.wordlist[word_num]
                break
            if self.wordlist[word_num] in NewMethodDict:
                mode_name = self.wordlist[word_num]
                break
            
        """
        The Built in Methods! 
        """
        
        if mode_name == "line":
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return [GeomTool.MethodDict['line'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
        if mode_name == "circ":
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return [GeomTool.MethodDict['circle'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
        if mode_name == "pbis":
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return [GeomTool.MethodDict['perp_bis'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
        
        if mode_name == "mdpt":
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return [GeomTool.MethodDict['mid_pt'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Circle":
                return [GeomTool.MethodDict['circle_center'][1], [self.isnameobj(self.wordlist[word_num + 1])]]

        if mode_name == "abis":
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point" and self.wordtype(self.wordlist[word_num + 3]) == "Point":
                return [GeomTool.MethodDict['angle_bis'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 3])]]
        
        if mode_name == "pt":
            if word_num == len(self.wordlist) - 1:
                return [GeomTool.MethodDict['free_pt'][1], []]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Line":
                return [GeomTool.MethodDict['pt_on_line'][1], [self.isnameobj(self.wordlist[word_num + 1])]]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Circle":
                return [GeomTool.MethodDict['pt_on_circle'][1], [self.isnameobj(self.wordlist[word_num + 1])]]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Number" and self.wordtype(self.wordlist[word_num + 2]) == "Number":
                return [GeomTool.MethodDict['free_pt'][1], [], float(self.wordlist[word_num + 1]) * random.gauss(1, PERT_NUM) + random.gauss(0, PERT_NUM), float(self.wordlist[word_num + 2]) * random.gauss(1, PERT_NUM) + random.gauss(0, PERT_NUM)]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Number" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return [GeomTool.MethodDict['pt_on_line'][1], [self.isnameobj(self.wordlist[word_num + 1])], float(self.wordlist[word_num + 2]) * random.gauss(1, PERT_NUM) + random.gauss(0, PERT_NUM), float(self.wordlist[word_num + 3]) * random.gauss(1, PERT_NUM) + random.gauss(0, PERT_NUM)]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Number" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return [GeomTool.MethodDict['pt_on_circle'][1], [self.isnameobj(self.wordlist[word_num + 1])], float(self.wordlist[word_num + 2]) * random.gauss(1, PERT_NUM) + random.gauss(0, PERT_NUM), float(self.wordlist[word_num + 3]) * random.gauss(1, PERT_NUM) + random.gauss(0, PERT_NUM)]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return [GeomTool.MethodDict['inx_line_line'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return [GeomTool.MethodDict['inx_line_line'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                return [GeomTool.MethodDict['inx_line_line'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                lineobj = self.isnameobj(self.wordlist[word_num + 1])
                circobj = self.isnameobj(self.wordlist[word_num + 2])
                testx = float(self.wordlist[word_num + 3])
                testy = float(self.wordlist[word_num + 4])
                isclose = ((testx * -lineobj.c[1] + testy * lineobj.c[0]) > (circobj.c[0] * -lineobj.c[1] + circobj.c[1] * lineobj.c[0])) ^ ((lineobj.item[0].c[0] * -lineobj.c[1] + lineobj.item[0].c[1] * lineobj.c[0]) > (lineobj.item[1].c[0] * -lineobj.c[1] + lineobj.item[1].c[1] * lineobj.c[0]))
                if isclose:
                    return [GeomTool.MethodDict['inx_line_circle_far'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
                else:
                    return [GeomTool.MethodDict['inx_line_circle_close'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                lineobj = self.isnameobj(self.wordlist[word_num + 2])
                circobj = self.isnameobj(self.wordlist[word_num + 1])
                testx = float(self.wordlist[word_num + 3])
                testy = float(self.wordlist[word_num + 4])
                isclose = ((testx * -lineobj.c[1] + testy * lineobj.c[0]) > (circobj.c[0] * -lineobj.c[1] + circobj.c[1] * lineobj.c[0])) ^ ((lineobj.item[0].c[0] * -lineobj.c[1] + lineobj.item[0].c[1] * lineobj.c[0]) > (lineobj.item[1].c[0] * -lineobj.c[1] + lineobj.item[1].c[1] * lineobj.c[0]))
                if isclose:
                    return [GeomTool.MethodDict['inx_line_circle_far'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
                else:
                    return [GeomTool.MethodDict['inx_line_circle_close'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]

            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                circ1obj = self.isnameobj(self.wordlist[word_num + 1])
                circ2obj = self.isnameobj(self.wordlist[word_num + 2])
                testx = float(self.wordlist[word_num + 3])
                testy = float(self.wordlist[word_num + 4])
                if -testy * circ1obj.c[0] + testx * circ1obj.c[1] + testy * circ2obj.c[0] - circ1obj.c[1] * circ2obj.c[0] - testx * circ2obj.c[1] + circ1obj.c[0] * circ2obj.c[1] >= 0:
                    return [GeomTool.MethodDict['inx_circle_circle_pos'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
                else:
                    return [GeomTool.MethodDict['inx_circle_circle_pos'][1], [self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 1])]]
        
        if mode_name == "para":
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return [GeomTool.MethodDict['para_line'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return [GeomTool.MethodDict['para_line'][1], [self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 1])]]

        if mode_name == "perp":
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return [GeomTool.MethodDict['perp_line'][1], [self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])]]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return [GeomTool.MethodDict['perp_line'][1], [self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 1])]]
        
        if mode_name != "":
            for usage in NewMethodDict[mode_name]:
                method = usage[0]
                in_item_list = usage[1]

                FINISHED = True
                if word_num == len(self.wordlist) - 1 - len(in_item_list):
                    item_list = []
                    for item_num in range(1, len(in_item_list) + 1):
                        if self.wordtype(self.wordlist[word_num + item_num]) != in_item_list[item_num - 1]:
                            FINISHED = False
                            break
                        item_list.append(self.isnameobj(self.wordlist[word_num + item_num]))
                    if FINISHED:
                        return [method, item_list]


        return None
    
    def descent_conditions(self):
        word_num = 0
        conditions = []
        while word_num < len(self.wordlist):
            if self.wordlist[word_num] == "eq":
                conditions.append(["eq", self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2])])
                word_num += 3
                continue
            if self.wordlist[word_num] == "eqdist":
                conditions.append(["eqdist", self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 3]), self.isnameobj(self.wordlist[word_num + 4])])
                word_num += 5
                continue
            if self.wordlist[word_num] == "col":
                conditions.append(["col", self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 3])])
                word_num += 4
                continue
            if self.wordlist[word_num] == "cyc":
                conditions.append(["cyc", self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 3]), self.isnameobj(self.wordlist[word_num + 4])])
                word_num += 5
                continue
            if self.wordlist[word_num] == "para":
                conditions.append(["para", self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 3]), self.isnameobj(self.wordlist[word_num + 4])])
                word_num += 5
                continue
            if self.wordlist[word_num] == "perp":
                conditions.append(["perp", self.isnameobj(self.wordlist[word_num + 1]), self.isnameobj(self.wordlist[word_num + 2]), self.isnameobj(self.wordlist[word_num + 3]), self.isnameobj(self.wordlist[word_num + 4])])
                word_num += 5
                continue

            if self.wordtype(self.wordlist[word_num]) == "Formula":
                conditions.append(["Formula", self.wordlist[word_num]])
                word_num += 1
                continue
            word_num += 1
        return conditions     
    
    def waitfor(self):
        # print("Hi")
        if len(self.wordlist) > 0 and self.wordlist[0] == "descent":
            return ["Point", "Line", "Circle", "Done"]

        MethodList = list(GeomTool.MethodDict.values())
        NewMethodDict = dict()
        for term in MethodList:
            if term[0] in NewMethodDict:
                NewMethodDict[term[0]].append([term[1], term[2], term[3]])
            else:
                NewMethodDict[term[0]] = [[term[1], term[2], term[3]]]

        mode_name = ""

        word_num = -1
        for word_num in range(len(self.wordlist)):
            if self.wordlist[word_num] in self.mode_list:
                mode_name = self.wordlist[word_num]
                break
            if self.wordlist[word_num] in NewMethodDict:
                mode_name = self.wordlist[word_num]
                break

            
        """
        The Built in Methods! 
        """
        
        if mode_name in ("line", "circ", "pbis"):
            if word_num == len(self.wordlist) - 1:
                return ["Point"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Point":
                return ["Point"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return ["Done"]
            
        if mode_name == "mdpt":
            if word_num == len(self.wordlist) - 1:
                return ["Point", "Circle"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Point":
                return ["Point"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return ["Done"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Circle":
                return ["Done"]
            
        if mode_name == "abis":
            if word_num == len(self.wordlist) - 1:
                return ["Point"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Point":
                return ["Point"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return ["Point"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point" and self.wordtype(self.wordlist[word_num + 3]) == "Point":
                return ["Done"]
        
        if mode_name == "pt":
            if word_num == len(self.wordlist) - 1:
                return ["Pt"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Number" and self.wordtype(self.wordlist[word_num + 2]) == "Number":
                return ["Done"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Line":
                return ["Done", "Line", "Circle", "Number"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Number" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Done"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Circle":
                return ["Done", "Line", "Circle", "Number"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Number" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Done"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return ["Done"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Done"]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                return ["Done"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Circle":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                return ["Done"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Circle":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                return ["Done"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                return ["Done"]
        
        if mode_name in ("para", "perp"):
            if word_num == len(self.wordlist) - 1:
                return ["Point", "Line"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Point":
                return ["Line"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return ["Done"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Line":
                return ["Point"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return ["Done"]
            
        if mode_name != "":
            outlst = []
            for usage in NewMethodDict[mode_name]:
                in_item_list = usage[1]

                if word_num >= len(self.wordlist) - 1 - len(in_item_list):
                    SUCCESS = True
                    for item_num in range(word_num + 1, len(self.wordlist)):
                        if self.wordtype(self.wordlist[item_num]) != in_item_list[item_num - word_num - 1]:
                            SUCCESS = False
                    if not SUCCESS:
                        continue
                    elif word_num == len(self.wordlist) - 1 - len(in_item_list):
                        outlst.append("Done")
                    else:
                        outlst.append(in_item_list[len(self.wordlist) - 1 - word_num])
                else:
                    continue
            
            if len(outlst) > 0:
                return outlst
            
            
        return ["Point", "Line", "Circle"]

            
if __name__ == '__main__':
    a = ExplainLine('descent col p a b ', [])
    print(a.wordlist)
    print(a.geom_appear)