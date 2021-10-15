from enum import Enum
class Node:
    def __init__(self, node_name, is_it_final=False, is_it_error=False, error_type=None,lookahead = False,token_type = None,token_matter = False):
        self.node_name = node_name
        self.is_it_final = is_it_final
        self.is_it_error = is_it_error
        self.error_type = error_type
        self.lookahead = lookahead
        self.token_type = token_type
        self.token_matter = token_matter
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
class DFA:
    def __init__(self, load_mode=False, save_mode=False, load_path="dfa.txt", save_path="dfa.txt"):
        """
        initialize the DFA module
        """

        self.states = {-1: Node(node_name=-1, is_it_final=True, is_it_error=True, error_type=Error.invalid_input),
                        0: Node(node_name=0),
                        1: Node(node_name=1),
                        2: Node(node_name=2, is_it_final=True, is_it_error=True, error_type=Error.invalid_number),
                        3: Node(node_name=3, is_it_final=True,lookahead=True,token_type=Token.num,token_matter=True),
                        4: Node(node_name=4),
                        5: Node(node_name=5, is_it_final=True,lookahead=True,token_type=Token.id,token_matter=True),
                        6: Node(node_name=6, is_it_final=True,token_type=Token.symbol,token_matter=True),
                        7: Node(node_name=7),
                        8: Node(node_name=8, is_it_final=True,lookahead=True,token_type=Token.symbol,token_matter=True),
                        9: Node(node_name=9, is_it_final=True,token_type=Token.symbol,token_matter=True),
                       10: Node(node_name=10),
                       11: Node(node_name=11, is_it_final=True,lookahead=True,token_type=Token.white_space),
                       12: Node(node_name=12),
                       13: Node(node_name=13, is_it_final=True, is_it_error=True, error_type=Error.unmatched_comment),
                       14: Node(node_name=14, is_it_final=True,lookahead=True,token_type=Token.symbol,token_matter=True),
                       15: Node(node_name=15),
                       16: Node(node_name=16),
                       17: Node(node_name=17,is_it_final=True,token_type=Token.comment),
                       18: Node(node_name=18),
                       19: Node(node_name=19),
                    }

        try:
            if load_mode :
                self.table = self.load_table(load_path)
            else:
                self.table = self.initialize_table()
            if save_mode:
                self.save_dfa(save_path)
        except:
            pass
    def get_state(self,current_state:int,c:int) -> Node:
        return self.states.get(self.table[current_state][c])
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
                table[0][i] = 4
                table[4][i] = 4
                table[1][i] = 2
            if self.is_it_white_space(i):
                table[0][i] = 10
                table[10][i] = 10
            else:
                table[10][i] = 11
            if self.is_it_unique_symbol(i):
                table[0][i] = 6
            elif i == 61:  # is input is =
                table[0][i] = 7
                table[7][i] = 9
            elif self.is_it_valid(i):
                table[7][i] = 8  # remark the others of symbol table
            if i == 47:  # if input is /
                table[0][i] = 15
                table[12][i] = 13
                table[15][i] = 16
                table[19][i] = 17
            elif self.is_it_valid(i):
                table[12][i] = 14
            if i == 42:  # is input is *
                table[0][i] = 12
                table[15][i] = 18
                table[18][i] = 19
                table[19][i]= 19
            else:
                table[18][i] = 18  # remark the others of comment for state 12
                if i != 47:
                    table[19][i] = 18  # remark others of comment for state 13
            if self.is_it_IDorNum_others(i):
                table[1][i] = 3
                table[4][i] = 5
            if i == 10:
                table[16][i] = 17
            else:
                table[16][i] = 16
        return table

    def is_it_IDorNum_others(self, c: int) -> bool:
        """

        :param c:
        :return:
        """
        return self.is_it_white_space(c) or self.is_it_symbol(c) or c == 47

    def is_it_unique_symbol(self, c: int) -> bool:
        """
        :return:
        """
        return (c != 42) and ((40 <= c <= 45) or (58 <= c <= 60) or (c == 91) or c == 93 or c == 123 or c == 125)

    def is_it_symbol(self, c: int) -> bool:
        """
        :return:
        """
        return (40 <= c <= 45) or (58 <= c <= 61) or (c == 91) or c == 93 or c == 123 or c == 125

    def is_it_white_space(self, c: int) -> bool:
        """

        :param c:
        :return: return whether c is a white space or not
        """
        return (9 <= c <= 13) or (c == 32)

    def is_is_digits(self, c: int) -> bool:
        """

        :param c: get the ord of the input char
        :return: return whether the char is digit or not [0-9]
        """
        return c >= 48 and c <= 57
    def is_it_valid(self,c:int)->bool:
        return (97 <= c <= 122) or (65 <= c <= 90) or (c >= 48 and c <= 57) or ((40 <= c <= 45) or (58 <= c <= 61) or (c == 91) or c == 93 or c == 123 or c == 125) or ((9 <= c <= 13) or (c == 32))

    def is_it_letter(self, c: int) -> bool:
        """

        :param c: char input as an ord
        :return: return whether it is [a-z,A-Z] or not
        """
        return (97 <= c <= 122) or (65 <= c <= 90)

    def save_dfa(self, path: str):
        """
        this function save the dfa in file txt
        :param path: get path to save file as txt
        :return:
        """
        wr = ""
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                wr += str(self.table[i][j]) + " "
            wr += "\n"
        f = open(path, "w")
        f.write(wr)
        f.close()

    def load_table(self,path:str)->list:
        """

        :param path: get input txt file path
        :return: return the 2D array of DFAS
        """
        self.table = []
        with open(path, "r") as f:
            for line in f:
                line.replace('\n', ' ')
                temp = list(map(int,line.split()))
                self.table.append(temp)
        f.close()
        return self.table




