from enum import Enum
import json
class first_follow_predict:
	firsts = [['ε', 'int', 'void'], ['ε', 'int', 'void'], ['int', 'void'], ['int', 'void'], ['(', ';', '['], [';', '['], ['('], ['int', 'void'], ['int', 'void'], [',', 'ε'], ['int', 'void'], ['[', 'ε'], ['{'], ['ε', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['break', ';', 'ID', '(', 'NUM'], ['if'], ['endif', 'else'], ['repeat'], ['return'], [';', 'ID', '(', 'NUM'], ['ID', '(', 'NUM'], ['=', '[', '(', '*', '+', '-', '<', '==', 'ε'], ['=', '*', 'ε', '+', '-', '<', '=='], ['(', 'NUM'], ['(', '*', '+', '-', '<', '==', 'ε'], ['ε', '<', '=='], ['<', '=='], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', 'ε'], ['(', 'NUM'], ['ε', '+', '-'], ['+', '-'], ['(', 'ID', 'NUM'], ['(', '*', 'ε'], ['(', 'NUM'], ['*', 'ε'], ['(', 'ID', 'NUM'], ['(', '[', 'ε'], ['[', 'ε'], ['(', 'ε'], ['(', 'NUM'], ['ε', 'ID', '(', 'NUM'], ['ID', '(', 'NUM'], [',', 'ε']]
	follows = [['$'], ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['(', ';', '[', ',', ')'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['ID'], [')'], [')'], [',', ')'], [',', ')'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['}'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], ['(', 'ID', 'NUM'], [';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['(', 'ID', 'NUM'], ['+', '-', ';', ')', '<', '==', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['*', '+', '-', '<', '==', ';', ')', ']', ','], [')'], [')'], [')']]
	predicts = [['int', 'void', '$'], ['int', 'void'], ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void'], ['int', 'void'], ['('], [';', '['], [';'], ['['], ['('], ['int'], ['void'], ['int'], ['void'], [','], [')'], ['int', 'void'], ['['], [',', ')'], ['{'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['}'], ['break', ';', 'ID', '(', 'NUM'], ['{'], ['if'], ['repeat'], ['return'], ['ID', '(', 'NUM'], ['break'], [';'], ['if'], ['endif'], ['else'], ['repeat'], ['return'], [';'], ['ID', '(', 'NUM'], ['(', 'NUM'], ['ID'], ['='], ['['], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['='], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['<', '=='], [';', ')', ']', ','], ['<'], ['=='], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['+', '-'], ['<', '==', ';', ')', ']', ','], ['+'], ['-'], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['*'], ['+', '-', '<', '==', ';', ')', ']', ','], ['('], ['ID'], ['NUM'], ['('], ['[', '*', '+', '-', ';', ')', '<', '==', ']', ','], ['['], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['('], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['('], ['NUM'], ['ID', '(', 'NUM'], [')'], ['ID', '(', 'NUM'], [','], [')']]
	non_terminals = ['Program', 'Declaration_list', 'Declaration', 'Declaration_initial', 'Declaration_prime', 'Var_declaration_prime', 'Fun_declaration_prime', 'Type_specifier', 'Params', 'Param_list', 'Param', 'Param_prime', 'Compound_stmt', 'Statement_list', 'Statement', 'Expression_stmt', 'Selection_stmt', 'Else_stmt', 'Iteration_stmt', 'Return_stmt', 'Return_stmt_prime', 'Expression', 'B', 'H', 'Simple_expression_zegond', 'Simple_expression_prime', 'C', 'Relop', 'Additive_expression', 'Additive_expression_prime', 'Additive_expression_zegond', 'D', 'Addop', 'Term', 'Term_prime', 'Term_zegond', 'G', 'Factor', 'Var_call_prime', 'Var_prime', 'Factor_prime', 'Factor_zegond', 'Args', 'Arg_list', 'Arg_list_prime']


class StateType(Enum):
    MID = "MID"
    START = "Start"
    ACC = "Acc"

class state:
    def __init__(self,n,mainG,state_type = StateType.MID ):
        self.main_grammer = mainG
        self.stateType = state_type
        self.number = n
        self.states = {}
    def add_state(self,n,index,t,accepting,NT):
        if (index >= len(t) ):
            return
        if index == len(t) - 1:
            self.states[t[index]] = accepting
            accepting.number = n
            return
        temp = state(n+1,NT)
        self.states[t[index]] = temp
        temp.add_state(temp.number, index+1, t, accepting,NT)
    def __str__(self):
        return str(self.number)




class diagram:
    def __init__(self):
        self.state_number = 0
        self.grammar = json.load(open("./parser_utils/grammer.json"))
        self.first = json.load(open("./parser_utils/files/first.json"))
        self.follow = json.load(open("./parser_utils/files/follow.json"))
        self.predict = json.load(open("./parser_utils/files/predict.json"))
        self.non_terminals = list(self.grammar.keys())
        self.terminals = set(self.flatten(list(self.grammar.values()))) - set(self.non_terminals)
        self.diagrams = {}
        for NT in self.non_terminals:
            self.diagrams[NT] = self.create_diagram_each(self.grammar[NT],NT)

    def create_diagram_each(self,productions,NT):
        starting = state(self.state_number,NT, StateType.START)
        accepting = state(self.state_number,NT, StateType.ACC)
        for product in productions:
            starting.add_state(self.state_number, 0, product, accepting,NT)
            self.state_number = accepting.number
        self.state_number = accepting.number + 1
        accepting.number = self.state_number
        self.state_number = self.state_number + 1
        return starting



    def flatten(self, x):
        if isinstance(x, list):
            return [a for i in x for a in self.flatten(i)]
        else:
            return [x]

