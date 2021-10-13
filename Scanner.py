
class Scanner:
    def __init__(self,path):
        """
        this function is called at the instantiation of module Scanner
        :arg
        path : the path of the file to be written and compiled by program
        """
        self.input_file = open(path)
        self.line_number = 1
        self.char_index = 0
        self.DFA = DFA(load_mode=False,save_mode=True,save_path="dfa.txt")
    def get_next_token(self):
        pass #TODO
class DFA:
    def __init__(self,load_mode = False , save_mode = False,load_path = "dfa.txt",save_path = "dfa.txt"):
        """
        initialize the DFA module
        """
        try:
            if load_mode :
                self.table = self.load_table(load_path)
            else:
                self.table = self.initialize_table()
            if save_mode:
                self.save_dfa(save_path)
        except:
            pass
        self.accept_mode_with_lookahead = {3:True,5:True,6:False,8:False,9:True,10:False,14:False}
    def initialize_table(self)-> list:
        """[summary]
            Returns:
                list: 2D list of all transitions and state
            """
        table = [[0 for i in range(256)] for j in range(16)]
        """ initialization of table """
        for i in range(256):
            if self.is_is_digits(i):
                table[1][i] = 2
                table[2][i] = 2
                table[4][i] = 4
            if self.is_it_letter(i):
                table[1][i]= 4
                table[4][i] = 4
            if self.is_it_white_space(i):
                table[1][i] = 10
            if self.is_it_symbolwithouteq(i):
                table[1][i] = 6
            elif i == 61: # is input is =
                table[1][i] = 7
                table[7][i] = 8
            else:
                table[7][i] = 9 # remark the others of symbol table
            if i == 47 : # if input is /
                table[1][i] = 11
                table[11][i] = 15
                table[13][i] = 14
            if i == 42: # is input is *
                table[11][i] = 12
                table[12][i] = 13
                table[13][i] = 13
            else:
                table[12][i] = 12 #remark the others of comment for state 12
                if i != 47 :
                    table[13][i] = 12 # remark others of comment for state 13
            if self.is_it_IDorNum_others(i):
                table[2][i] = 3
                table[4][i] = 5
            if i == 10 :
                table[15][i] = 14
            else:
                table[15][i] = 15
        return table

    def is_it_IDorNum_others(self,c:int) -> bool:
        """

        :param c:
        :return:
        """
        return not (self.is_it_letter(c) or self.is_is_digits(c))

    def is_it_symbolwithouteq(self,c:int)->bool:
        """
        :return:
        """
        return ((c >= 40 and c <= 45) or (c>= 58 and c <= 60) or (c == 91 ) or c == 93 or c == 123 or c == 126)
    def is_it_white_space(self,c:int)->bool:
        """

        :param c:
        :return: return whether c is a white space or not
        """
        return (( c>= 9 and c<= 13 )or (c == 32))

    def is_is_digits(self,c : int) -> bool:
        """

        :param c: get the ord of the input char
        :return: return whether the char is digit or not [0-9]
        """
        return (c >= 48 and c <= 57)
    def is_it_letter(self,c: int)-> bool:
        """

        :param c: char input as an ord
        :return: return whether it is [a-z,A-Z] or not
        """
        return ( (c >= 97 and c <= 122 ) or (c >= 65 and c <= 90))
    def save_dfa(self,path : str ):
        wr = ""
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                wr+=str(self.table[i][j])+" "
            wr+="\n"
        f = open(path, "w")
        f.write(wr)
        f.close()
        """
        this function save the dfa in file txt
        :param path: get path to save file as txt
        :return:
        """
    def load_table(self,path:str)->list:
        self.table = []
        with open(path,"r") as f:
            for line in f:
                line.replace('\n', ' ')
                temp = list(map(int,line.split()))
                print(temp)
                self.table.append(temp)
        f.close()
        return self.table
        """

        :param path: get input txt file path
        :return: return the 2D array of DFAS
        """



