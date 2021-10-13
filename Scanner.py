from enum import Enum
class Token(Enum):
    id = "ID"
    keyword = "KEYWORD"
    num = "NUM"
    symbol = "SYMBOL"
    comment = "COMMENT"
    white_space = "WHITESPACE"
class Error(Enum):
    invalid_input = "Invalid input"
    invalid_number = "Invalid number"
    unmatched_comment = "Unmatched comment"
    unclosed_comment = "Unclosed comment"

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
        self.current_state = 0
        self.current_token = ""
        self.DFA = DFA(load_mode=False,save_mode=True,save_path="dfa.txt")

    def get_next_token(self):

        pass #TODO
class Symbol_tabel:
    def __init__(self):
        self.table = {"if":1, "else":2, "void": 3, "int":4, "repeat":5, "break":6, "until":7, "return":8}
        self.last_id = 9
    def get_token(self,ID:str):
        temp = self.table.get(ID,None)
        if temp == None:
            self.table[ID] = self.last_id
            self.last_id+=1
            return ()
        else:

    pass

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
        self.accept_node_lookahead_check = {3:True,5:True,9:False,8:True,11:True,14:True,17:True}
        self.error_node = {2:Error.invalid_number,-1:Error.invalid_input,13:Error.unmatched_comment}
    def initialize_table(self)-> list:
        """[summary]
            Returns:
                list: 2D list of all transitions and state
            """
        table = [[-1 for i in range(256)] for j in range(20)]
        """ initialization of table """
        for i in range(256):
            if self.is_is_digits(i):
                table[0][i] = 1
                table[1][i] = 1
                table[4][i] = 4
            if self.is_it_letter(i):
                table[0][i]= 4
                table[4][i] = 4
                table[1][i] = 2
            if self.is_it_white_space(i):
                table[0][i] = 10
                table[10][i] =10
            else:
                table[10][i] = 11
            if self.is_it_unique_symbol(i):
                table[0][i] = 6
            elif i == 61: # is input is =
                table[0][i] = 7
                table[7][i] = 9
            else:
                table[7][i] = 8 # remark the others of symbol table
            if i == 47 : # if input is /
                table[0][i] = 15
                table[12][i] = 13
                table[15][i] = 16
                table[19][i] = 17
            else:
                table[12][i] = 14
            if i == 42: # is input is *
                table[0][i] = 12
                table[15][i] = 18
                table[18][i] = 19
                table[19][i]= 19
            else:
                table[18][i] = 18 #remark the others of comment for state 12
                if i != 47 :
                    table[19][i] = 18 # remark others of comment for state 13
            if self.is_it_IDorNum_others(i):
                table[1][i] = 3
                table[4][i] = 5
            if i == 10 :
                table[16][i] = 17
            else:
                table[16][i] = 16
        return table

    def is_it_IDorNum_others(self,c:int) -> bool:
        """

        :param c:
        :return:
        """
        return (self.is_it_white_space(c) or self.is_it_symbol(c) or c == 47)

    def is_it_unique_symbol(self,c:int)->bool:
        """
        :return:
        """
        return  (c!= 42) and ((c >= 40 and c <= 45) or (c>= 58 and c <= 60) or (c == 91 ) or c == 93 or c == 123 or c == 126)
    def is_it_symbol(self,c:int)->bool:
        """
        :return:
        """
        return  ((c >= 40 and c <= 45) or (c>= 58 and c <= 61) or (c == 91 ) or c == 93 or c == 123 or c == 126)
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
        """
        this function save the dfa in file txt
        :param path: get path to save file as txt
        :return:
        """
        wr = ""
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                wr+=str(self.table[i][j])+" "
            wr+="\n"
        f = open(path, "w")
        f.write(wr)
        f.close()

    def load_table(self,path:str)->list:
        """

        :param path: get input txt file path
        :return: return the 2D array of DFAS
        """
        self.table = []
        with open(path,"r") as f:
            for line in f:
                line.replace('\n', ' ')
                temp = list(map(int,line.split()))
                self.table.append(temp)
        f.close()
        return self.table



