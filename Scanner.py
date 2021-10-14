from enum import Enum
import DFA.DFA

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

class SymbolTableItem:
    def __init__(self,token_type,name,id):
        self.token_type = token_type
        self.id = id
        self.name = name

class Scanner:

    def __init__(self,path):
        """
        this function is called at the instantiation of module Scanner
        :arg
        path : the path of the file to be written and compiled by program
        """
        self.input_address = path
        self.symbol_address = "symbol_table.txt"
        self.token_address ="tokens.txt"
        self.error_address = "lexical_errors.txt"
        self.line_number = 1
        self.char_index = 0
        self.current_state = 0
        self.current_lexeme = ""
        self.buffer = ""
        self.buffer_size = 0
        self.DFA = DFA(load_mode=False, save_mode=True, save_path="dfa.txt")
        self.symbol_Table = SymbolTable()

    def get_next_token(self):
        while self.char_index < self.buffer_size:
            input_char = self.buffer[self.char_index]
            ascii_code = ord(input_char)
            next_state = self.DFA.get_state(self.current_state,ascii_code)
            if next_state.is_it_final:
                if next_state.token_matter:
                    if next_state.lookahead:
                        token = self.get_token_string(next_state,self.current_lexeme)
                    else:
                        self.char_index +=1
                        token = self.get_token_string(next_state,self.current_lexeme+input_char)
                    self.current_state = 0
                    self.current_lexeme = ""
                    return token
                if next_state.is_it_error:
                    pass #TODO
                self.current_lexeme = ""
                self.current_state = 0
            else:
                self.current_lexeme+=input_char
                self.current_state = next_state.node_name
            self.char_index += 1
            if next_state.lookahead:
                self.char_index -= 1
    def get_token_string(self,state,lexeme):
        if state.token_type == Token.id:
            (id,type_of_token,lexeme) = self.symbol_Table.get_token(lexeme)
            return "("+str(type_of_token.values)+", "+str(lexeme)+")"
        else:
            return "("+str(state.token_type.values)+", "+str(lexeme)+")"
class SymbolTable:

    def __init__(self):
        self.table = {"if":1, "else":2, "void": 3, "int":4, "repeat":5, "break":6, "until":7, "return":8}
        self.last_id = 9

    def get_token(self, lexeme:str) -> (int,Token,str):
        temp = self.table.get(lexeme,None)
        if temp is None:
            self.table[lexeme] = self.last_id
            self.last_id+=1
            return self.last_id, Token.id, lexeme
        if temp <= 8 :
            return temp, Token.keyword, lexeme
        return temp, Token.id, lexeme

    pass


class ErrorTable:
    def __init__(self):
        pass

    # A suffix
    # Write
    # Add Error
    # Track Line Numbers


class Node:
    def __init__(self, node_name, is_it_final=False, is_it_error=False, error_type=None,lookahead = False,token_type = None,token_matter = False):
        self.node_name = node_name
        self.is_it_final = is_it_final
        self.is_it_error = is_it_error
        self.error_type = error_type
        self.lookahead = lookahead
        self.token_type = token_type
        self.token_matter = token_matter



