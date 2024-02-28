import GeomTool

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class ExplainLine:
    def __init__(self, in_text, geom_list, mode_list=["mdpt", "pt", "line", "para", "perp", "pbis", "abis", "circ"]):
        inword = False
        word = ''
        self.wordlist = []
        self.geom_list = geom_list
        self.mode_list = mode_list
        while len(in_text) > 0:
            read_char = in_text[0]
            if read_char != ' ':
                inword = True
                word += read_char
            if inword and read_char == ' ':
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
    
    def wordtype(self, instr):
        if is_float(instr):
            return "Number"
        isn = self.isname(instr)
        if isn >= 0:
            return self.geom_list[isn].type
        return None
    
    def waitfor(self):
        find_mode = -1
        mode_name = ""
        word_num = -1
        for word_num in range(len(self.wordlist)):
            if self.wordlist[word_num] in self.mode_list:
                find_mode = word_num
                mode_name = self.wordlist[word_num]
                break
        
        if mode_name in ("line", "circ", "pbis"):
            if word_num == len(self.wordlist) - 1:
                return ["Point"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Point":
                return ["Point"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return []
            
        if mode_name == "mdpt":
            if word_num == len(self.wordlist) - 1:
                return ["Point", "Circle"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Point":
                return ["Point"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return []
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Circle":
                return []
            
        if mode_name == "abis":
            if word_num == len(self.wordlist) - 1:
                return ["Line"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Line":
                return ["Line"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return []
        
        if mode_name == "pt":
            if word_num == len(self.wordlist) - 1:
                return ["Pt"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Number" and self.wordtype(self.wordlist[word_num + 2]) == "Number":
                return []
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Line":
                return ["Line", "Circle", "Number"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Number" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return []
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Circle":
                return ["Line", "Circle", "Number"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Number" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return []
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return []
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Circle":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                return []
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Circle":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Circle" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                return []
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return ["Number"]
            if word_num == len(self.wordlist) - 4 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number":
                return ["Number"]
            if word_num == len(self.wordlist) - 5 and self.wordtype(self.wordlist[word_num + 1]) == "Circle" and self.wordtype(self.wordlist[word_num + 2]) == "Line" and self.wordtype(self.wordlist[word_num + 3]) == "Number" and self.wordtype(self.wordlist[word_num + 4]) == "Number":
                return []
        
        if mode_name in ("para", "perp"):
            if word_num == len(self.wordlist) - 1:
                return ["Point", "Line"]
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Point":
                return ["Line"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Point" and self.wordtype(self.wordlist[word_num + 2]) == "Line":
                return []
            if word_num == len(self.wordlist) - 2 and self.wordtype(self.wordlist[word_num + 1]) == "Line":
                return ["Point"]
            if word_num == len(self.wordlist) - 3 and self.wordtype(self.wordlist[word_num + 1]) == "Line" and self.wordtype(self.wordlist[word_num + 2]) == "Point":
                return []
            
            
        return "Point Line Circle"

            
if __name__ == '__main__':
    a = ExplainLine('  1 2 33 456 74 4 adsf  asfd56445 5', [])
    print(a.wordlist)
    print(a.geom_appear)