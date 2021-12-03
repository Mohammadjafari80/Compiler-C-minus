from enum import Enum
class first_follow_predict:
	firsts = [['ε', 'int', 'void'], ['ε', 'int', 'void'], ['int', 'void'], ['int', 'void'], ['(', ';', '['], [';', '['], ['('], ['int', 'void'], ['int', 'void'], [',', 'ε'], ['int', 'void'], ['[', 'ε'], ['{'], ['ε', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['break', ';', 'ID', '(', 'NUM'], ['if'], ['endif', 'else'], ['repeat'], ['return'], [';', 'ID', '(', 'NUM'], ['ID', '(', 'NUM'], ['=', '[', '(', '*', '+', '-', '<', '==', 'ε'], ['=', '*', 'ε', '+', '-', '<', '=='], ['(', 'NUM'], ['(', '*', '+', '-', '<', '==', 'ε'], ['ε', '<', '=='], ['<', '=='], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', 'ε'], ['(', 'NUM'], ['ε', '+', '-'], ['+', '-'], ['(', 'ID', 'NUM'], ['(', '*', 'ε'], ['(', 'NUM'], ['*', 'ε'], ['(', 'ID', 'NUM'], ['(', '[', 'ε'], ['[', 'ε'], ['(', 'ε'], ['(', 'NUM'], ['ε', 'ID', '(', 'NUM'], ['ID', '(', 'NUM'], [',', 'ε']]
	follows = [['$'], ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['(', ';', '[', ',', ')'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['ID'], [')'], [')'], [',', ')'], [',', ')'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['}'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], ['(', 'ID', 'NUM'], [';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['(', 'ID', 'NUM'], ['+', '-', ';', ')', '<', '==', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['*', '+', '-', '<', '==', ';', ')', ']', ','], [')'], [')'], [')']]
	predicts = [['int', 'void', '$'], ['int', 'void'], ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void'], ['int', 'void'], ['('], [';', '['], [';'], ['['], ['('], ['int'], ['void'], ['int'], ['void'], [','], [')'], ['int', 'void'], ['['], [',', ')'], ['{'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['}'], ['break', ';', 'ID', '(', 'NUM'], ['{'], ['if'], ['repeat'], ['return'], ['ID', '(', 'NUM'], ['break'], [';'], ['if'], ['endif'], ['else'], ['repeat'], ['return'], [';'], ['ID', '(', 'NUM'], ['(', 'NUM'], ['ID'], ['='], ['['], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['='], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['<', '=='], [';', ')', ']', ','], ['<'], ['=='], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['+', '-'], ['<', '==', ';', ')', ']', ','], ['+'], ['-'], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['*'], ['+', '-', '<', '==', ';', ')', ']', ','], ['('], ['ID'], ['NUM'], ['('], ['[', '*', '+', '-', ';', ')', '<', '==', ']', ','], ['['], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['('], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['('], ['NUM'], ['ID', '(', 'NUM'], [')'], ['ID', '(', 'NUM'], [','], [')']]
	non_terminals = ['Program', 'Declaration_list', 'Declaration', 'Declaration_initial', 'Declaration_prime', 'Var_declaration_prime', 'Fun_declaration_prime', 'Type_specifier', 'Params', 'Param_list', 'Param', 'Param_prime', 'Compound_stmt', 'Statement_list', 'Statement', 'Expression_stmt', 'Selection_stmt', 'Else_stmt', 'Iteration_stmt', 'Return_stmt', 'Return_stmt_prime', 'Expression', 'B', 'H', 'Simple_expression_zegond', 'Simple_expression_prime', 'C', 'Relop', 'Additive_expression', 'Additive_expression_prime', 'Additive_expression_zegond', 'D', 'Addop', 'Term', 'Term_prime', 'Term_zegond', 'G', 'Factor', 'Var_call_prime', 'Var_prime', 'Factor_prime', 'Factor_zegond', 'Args', 'Arg_list', 'Arg_list_prime']

class StateType(Enum):
    MID = "MID"
    START = "Start"
    ACC = "Acc"
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True)
import json
class state:
    def __init__(self,n,state_type = StateType.MID ):
        self.stateType = state_type
        if state_type != StateType.ACC:
            print(n)
        self.number = n
        self.states = {}
    def toJSON(self):
        return {
            "stateType":self.state_type,
            "number":self.number,
            "states":[]
        }
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True)
    def add_state(self,n,index,t,accepting):
        if (index >= len(t) ):
            return
        if (index == len(t) -1 ):
            self.states[t[index]] = accepting
            accepting.number = n
            return
        temp= state(n+1)
        self.states[t[index]] = temp
        temp.add_state(temp.number,index+1,t,accepting)




class diagram:
    def __init__(self,address):
        self.statenumber = 0
        self.grammer = json.load(open("grammer.json"))
        self.first = json.load(open("files/first.json"))
        self.follow = json.load(open("files/follow.json"))
        self.predict = json.load(open("files/predict.json"))
        self.non_terminals = list(self.grammer.keys())
        self.diagrams = {}
        for NT in self.non_terminals:
            self.diagrams[NT] = self.create_diagram_each(self.grammer[NT])
    def create_diagram_each(self,productions):
        starting = state(self.statenumber,StateType.START)
        accepting = state(self.statenumber,StateType.ACC)
        for product in productions:
            starting.add_state(self.statenumber,0,product,accepting)
            self.statenumber = accepting.number
        self.statenumber = accepting.number+1
        accepting.number = self.statenumber
        print(accepting.number)
        self.statenumber = self.statenumber+1
        return starting
    def create_action_table(self):
        pass





d = diagram("grammer.json")
print(d.grammer)
print(d.non_terminals)
#json.dump( d.diagrams, open( "diagram.json", 'w' ) )
#print(d.diagrams)
print(d.follow["Program"][0])