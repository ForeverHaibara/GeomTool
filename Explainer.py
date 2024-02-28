import GeomTool

class ExplainLine:
    def __init__(self, in_text, geom_list, mode_list=["mdpt", "pt", "line", "para", "perp", "pbis", "abis", "circ"]):
        inword = False
        word = ''
        self.wordlist = []
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
            
if __name__ == '__main__':
    a = ExplainLine('  1 2 33 456 74 4 adsf  asfd56445 5', [])
    print(a.wordlist)
    print(a.geom_appear)