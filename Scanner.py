from enum import Enum
import DFA.DFA
from DFA import *
class SymbolTableItem:
    def __init__(self,token_type,name,id):
        self.token_type = token_type
        self.id = id
        self.name = name
class EOFERROR(Exception):
    pass

class Scanner:

    def __init__(self,path):
        """
        this function is called at the instantiation of module Scanner
        :arg
        path : the path of the file to be written and compiled by program
        """
        self.input_address = path
        self.input_file = open(path,"r")
        self.symbol_address = "symbol_table.txt"
        self.token_address ="tokens.txt"
        self.error_address = "lexical_errors.txt"
        self.line_number = 0
        self.char_index = 0
        self.current_state = 0
        self.current_lexeme = ""
        self.buffer = "not empty"
        self.buffer_size = 0
        self.DFA = DFA.DFA(load_mode=False, save_mode=False, save_path="dfa.txt")
        self.symbol_Table = SymbolTable()
        self.error_table = {}
        self.token_table = {}
        self.line_number_of_comment = 0
    def scan(self):
        while True:
            token = self.get_next_token()
            if token == False:
                if self.current_state == 18 or self.current_state == 19:
                    self.insert_error(line_number=self.line_number_of_comment, error_type=DFA.Error.unclosed_comment,
                                      error_lexeme=self.current_lexeme)
                if self.current_state == 1 or self.current_state == 4 or self.current_state == 7 or self.current_state == 12:
                    next = self.current_state +1
                    if self.current_state == 12 or self.current_state == 1:
                        next+=1
                    token = self.get_token_string(self.DFA.states[next],self.current_lexeme)
                    self.insert_token(token=token, line_number=self.line_number)
                self.input_file.close()
                self.save_token()
                self.save_errors()
                self.symbol_Table.save_symbol_table(self.symbol_address)
                return
            self.insert_token(token=token,line_number=self.line_number)
    def get_next_token(self):
        while self.buffer != "":
            while self.char_index < self.buffer_size:
                input_char = self.buffer[self.char_index]
                ascii_code = ord(input_char)
                next_state = self.DFA.get_state(self.current_state,ascii_code)
                #TODO check for better solution
                if next_state.node_name == 15:
                    self.line_number_of_comment = self.line_number
                if next_state.is_it_final:
                    if next_state.token_matter:
                        if next_state.lookahead:
                            token = self.get_token_string(next_state,self.current_lexeme)
                        else:
                            self.char_index +=1
                            token = self.get_token_string(next_state,self.current_lexeme+input_char)
                        self.current_state = 0
                        self.current_lexeme = ""
                        #if ascii_code == 10:
                            #self.read_next_line()
                        return token
                    if next_state.is_it_error:
                        self.insert_error(self.line_number,next_state.error_type,self.current_lexeme+str(input_char))
                    self.current_lexeme = ""
                    self.current_state = 0
                else:
                    self.current_lexeme+=input_char
                    self.current_state = next_state.node_name
                self.char_index += 1
                if next_state.lookahead:
                    self.char_index -= 1
            self.read_next_line()
        return False

    def insert_error(self,line_number,error_type :DFA.Error,error_lexeme:str):
        error_lexeme = error_lexeme.replace("\n", "")
        if error_type == DFA.Error.unclosed_comment:
            if len(error_lexeme) > 7:
                error_lexeme = str(error_lexeme[0:7])+str("...")
            else:
                error_lexeme = str(error_lexeme)+str("...")
        temp = self.error_table.get(line_number,None)
        if temp is None:
            self.error_table[line_number] = "("+str(error_lexeme)+", "+str(error_type.value)+")"
        else:
            self.error_table[line_number] = temp+" "+"("+str(error_lexeme)+", "+str(error_type.value)+")"
    def read_next_line(self):
        self.buffer = self.input_file.readline()
        self.buffer_size = len(self.buffer)
        if self.buffer_size !=0:
            self.line_number +=1
        self.char_index = 0
    def get_token_string(self,state,lexeme):
        if state.token_type == DFA.Token.id:
            (id,type_of_token,lexeme) = self.symbol_Table.get_token(lexeme)
            return "("+str(type_of_token.value)+", "+str(lexeme)+")"
        else:
            return "("+str(state.token_type.value)+", "+str(lexeme)+")"
    def insert_token(self, token:str,line_number) -> (int,DFA.Token,str):
        temp = self.token_table.get(line_number,None)
        if temp is None:
            self.token_table[line_number] = token
        else:
            self.token_table[line_number] = temp+" "+token
    def save_token(self):
        f = open(self.token_address,"w")
        for (key,val) in self.token_table.items():
            f.write(str(key)+".\t"+val+" \n")
        f.close()
    def save_errors(self):
        f = open(self.error_address,"w")
        for (key,val) in self.error_table.items():
            f.write(str(key)+".\t"+val+" \n")
        if len(self.error_table) == 0:
            f.write("There is no lexical error.\n")
        f.close()





class SymbolTable:
    def __init__(self):
        self.table = {"if":1, "else":2, "void": 3, "int":4, "repeat":5, "break":6, "until":7, "return":8}
        self.last_id = 9
    def get_token(self, lexeme:str) -> (int,DFA.Token,str):
        temp = self.table.get(lexeme,None)
        if temp is None:
            self.table[lexeme] = self.last_id
            self.last_id+=1
            return self.last_id, DFA.Token.id, lexeme
        if temp <= 8 :
            return temp, DFA.Token.keyword, lexeme
        return temp, DFA.Token.id, lexeme
    def save_symbol_table(self,address):
        f = open(address, "w")
        for (key,val) in self.table.items():
            f.write(str(val)+".\t"+key+"\n")
        f.close()




