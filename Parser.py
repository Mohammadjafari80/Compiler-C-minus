import Scanner
class first_follow_predict:
	firsts = [['ε', 'int', 'void'], ['ε', 'int', 'void'], ['int', 'void'], ['int', 'void'], ['(', ';', '['], [';', '['], ['('], ['int', 'void'], ['int', 'void'], [',', 'ε'], ['int', 'void'], ['[', 'ε'], ['{'], ['ε', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['break', ';', 'ID', '(', 'NUM'], ['if'], ['endif', 'else'], ['repeat'], ['return'], [';', 'ID', '(', 'NUM'], ['ID', '(', 'NUM'], ['=', '[', '(', '*', '+', '-', '<', '==', 'ε'], ['=', '*', 'ε', '+', '-', '<', '=='], ['(', 'NUM'], ['(', '*', '+', '-', '<', '==', 'ε'], ['ε', '<', '=='], ['<', '=='], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', 'ε'], ['(', 'NUM'], ['ε', '+', '-'], ['+', '-'], ['(', 'ID', 'NUM'], ['(', '*', 'ε'], ['(', 'NUM'], ['*', 'ε'], ['(', 'ID', 'NUM'], ['(', '[', 'ε'], ['[', 'ε'], ['(', 'ε'], ['(', 'NUM'], ['ε', 'ID', '(', 'NUM'], ['ID', '(', 'NUM'], [',', 'ε']]
	follows = [['$'], ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['(', ';', '[', ',', ')'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['ID'], [')'], [')'], [',', ')'], [',', ')'], ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['}'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], [';', ')', ']', ','], ['(', 'ID', 'NUM'], [';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['<', '==', ';', ')', ']', ','], ['(', 'ID', 'NUM'], ['+', '-', ';', ')', '<', '==', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['+', '-', '<', '==', ';', ')', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['*', '+', '-', '<', '==', ';', ')', ']', ','], [')'], [')'], [')']]
	predicts = [['int', 'void', '$'], ['int', 'void'], ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], ['int', 'void'], ['int', 'void'], ['('], [';', '['], [';'], ['['], ['('], ['int'], ['void'], ['int'], ['void'], [','], [')'], ['int', 'void'], ['['], [',', ')'], ['{'], ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['}'], ['break', ';', 'ID', '(', 'NUM'], ['{'], ['if'], ['repeat'], ['return'], ['ID', '(', 'NUM'], ['break'], [';'], ['if'], ['endif'], ['else'], ['repeat'], ['return'], [';'], ['ID', '(', 'NUM'], ['(', 'NUM'], ['ID'], ['='], ['['], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['='], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['<', '=='], [';', ')', ']', ','], ['<'], ['=='], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['+', '-'], ['<', '==', ';', ')', ']', ','], ['+'], ['-'], ['(', 'ID', 'NUM'], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','], ['(', 'NUM'], ['*'], ['+', '-', '<', '==', ';', ')', ']', ','], ['('], ['ID'], ['NUM'], ['('], ['[', '*', '+', '-', ';', ')', '<', '==', ']', ','], ['['], ['*', '+', '-', ';', ')', '<', '==', ']', ','], ['('], ['*', '+', '-', '<', '==', ';', ')', ']', ','], ['('], ['NUM'], ['ID', '(', 'NUM'], [')'], ['ID', '(', 'NUM'], [','], [')']]
	non_terminals = ['Program', 'Declaration_list', 'Declaration', 'Declaration_initial', 'Declaration_prime', 'Var_declaration_prime', 'Fun_declaration_prime', 'Type_specifier', 'Params', 'Param_list', 'Param', 'Param_prime', 'Compound_stmt', 'Statement_list', 'Statement', 'Expression_stmt', 'Selection_stmt', 'Else_stmt', 'Iteration_stmt', 'Return_stmt', 'Return_stmt_prime', 'Expression', 'B', 'H', 'Simple_expression_zegond', 'Simple_expression_prime', 'C', 'Relop', 'Additive_expression', 'Additive_expression_prime', 'Additive_expression_zegond', 'D', 'Addop', 'Term', 'Term_prime', 'Term_zegond', 'G', 'Factor', 'Var_call_prime', 'Var_prime', 'Factor_prime', 'Factor_zegond', 'Args', 'Arg_list', 'Arg_list_prime']
class parser:
    def __init__(self,grammer):
        pass
    def parse(self):
        pass

f = first_follow_predict()
print(len(f.firsts) == len(f.follows) == len(f.non_terminals))
print(len(f.firsts) == len(f.follows) == len(f.non_terminals) == len(f.predicts))