import Scanner
import anytree
# from  Any_tree import anytree as anytree
import parser_utils.Transition_diagram as TD
from anytree import Node, RenderTree
from enum import  Enum

EPSILON = None


class ErrorTypes(Enum):
    ILLEGAL = 1
    MISSING = 2
    UNEXPECTED_EOF = 3


class ParseToken:
    def __init__(self):
        self.type = None
        self.value = ""
        self.code_value = ""

    def set_info(self, token):
        token = token.split(",")
        self.type = token[0][1:]
        self.value = token[1][1:len(token[1]) - 1]
        if self.type == "KEYWORD" or self.type == "SYMBOL":
            self.code_value = token[1][1:len(token[1]) - 1]
        elif self.type == "NUM" or self.type == "ID":
            self.code_value = self.type
        if token[1][1:len(token[1]) - 1] == "output":
            print("here")


class Parser:

    def __init__(self, path, save_path):
        self.save_path = save_path
        self.transition_diagram = TD.Diagram()
        self.diagrams = self.transition_diagram.diagrams
        self.first = self.transition_diagram.first
        self.follow = self.transition_diagram.follow
        self.predict = self.transition_diagram.predict
        self.NT = self.transition_diagram.non_terminals
        self.T = self.transition_diagram.terminals
        self.stateN = self.transition_diagram.state_number
        self.scanner = Scanner.Scanner(path, save_path)
        self.stack = []
        self.push(self.diagrams[self.NT[0]])
        self.current_token = self.scanner.get_next_token()
        self.cur_state = self.front()
        self.p_token = ParseToken()
        self.p_token.set_info(self.current_token)
        self.root = Node(self.cur_state.main_grammar)
        self.current_node = self.root
        self.synchronous_set = self.follow
        self.line_number = 1
        self.errors = []
        self.is_stable = True

    def front(self) -> TD.State:
        return self.stack[len(self.stack) - 1]

    def pop(self) -> TD.State:
        return self.stack.pop()

    def push(self, node: TD.State):
        self.stack.append(node)

    def get_next_token(self):
        self.current_token = self.scanner.get_next_token()
        print(self.current_token)
        if self.current_token != "$":
            self.p_token.set_info(self.current_token)
        else:
            self.p_token.code_value = "$"

    def is_all_terminal(self, states):
        for state in states:
            if state not in self.T:
                return False
        return True

    def print_stack(self):
        for i in self.stack:
            if str(i) == "24":
                print(end="")
            print(i, end=" ")
        print("")

    def handle_epsilons(self, state, node):
        if 'null' in state.states.keys():
            Node('epsilon', node)
            return

        for production in self.diagrams[state.main_grammar].states.keys():
            if production in self.NT:
                a = Node(self.diagrams[production].main_grammar, node)
                self.handle_epsilons(self.diagrams[production], a)
                for next_state in state.states[production].states.keys():
                    b = Node(next_state, node)
                    self.handle_epsilons(self.diagrams[next_state], b)

    def parse(self):  # TODO add panic mode recovery and also add tree
        while True:
            while self.cur_state.stateType != TD.StateType.ACC:
                #self.print_tree()
                next_states_list = list(self.cur_state.states.keys())
                #print(self.errors)
                #self.print_stack()

                for production in self.cur_state.states.keys():
                    if production in self.T:
                        if self.scanner.get_line_number() == 7 and self.p_token.value == "*":
                            print("here")
                        if production == self.p_token.code_value:
                            temp = self.cur_state.states.get(self.p_token.code_value)
                            Node(f'({self.p_token.type}, {self.p_token.value})' if production != '$' else '$',
                                 parent=self.current_node)
                            self.cur_state = temp
                            self.get_next_token()
                            break
                        if self.p_token.code_value in next_states_list and self.cur_state.stateType == TD.StateType.MID:
                            temp = self.cur_state.states.get(self.p_token.code_value)
                            Node(f'({self.p_token.type}, {self.p_token.value})' if production != '$' else '$',
                                     parent=self.current_node)
                            self.cur_state = temp
                            self.get_next_token()
                            break
                        if self.cur_state.stateType == TD.StateType.START:
                            print("here")
                            continue
                        temp = self.cur_state.states.get(production)
                        #Node(f'({self.p_token.type}, {self.p_token.value})' if production != '$' else '$',
                                        #parent=self.current_node)
                        self.cur_state = temp
                        #self.get_next_token()
                        if production != self.p_token.code_value:
                            self.is_stable = False
                            line_number = self.scanner.get_line_number()
                            self.errors.append([ErrorTypes.MISSING, line_number, production])
                            print(ErrorTypes.MISSING, line_number, production)
                        break
                    else:
                        if self.p_token.code_value in self.first[production]:
                            self.current_node = Node(self.diagrams[production].main_grammar, parent=self.current_node)
                            self.push(self.cur_state.states[production])
                            self.push(self.diagrams[production])
                            self.cur_state = self.front()
                            break
                        elif EPSILON in self.first[production] and self.p_token.code_value in self.follow[production]: # TODO NEMIDONAM INJA BAYAD CHE GHALATI KARD
                            a = Node(self.diagrams[production].main_grammar, parent=self.current_node)
                            self.cur_state = self.cur_state.states[production]
                            self.handle_epsilons(self.diagrams[production], a)
                            break
                else:
                    line_number = self.scanner.get_line_number()
                    if (EPSILON in self.first[self.cur_state.main_grammar] and
                            self.p_token.code_value in self.follow[self.cur_state.main_grammar]):
                        self.cur_state = self.pop()
                        self.current_node = self.current_node.parent
                    elif (self.cur_state.stateType == TD.StateType.MID and self.p_token.code_value in self.follow[production]):
                        if self.current_token == "$":
                            self.errors.append([ErrorTypes.UNEXPECTED_EOF, self.scanner.get_line_number() + 1, None])
                            print(ErrorTypes.UNEXPECTED_EOF, self.scanner.get_line_number() + 1, None)
                            self.write_to_file()
                            return
                        self.errors.append([ErrorTypes.MISSING, line_number, production])
                        print(ErrorTypes.MISSING, line_number, production)
                        self.get_next_token()
                        self.is_stable = False
                    elif not(self.p_token.code_value in self.follow[self.cur_state.main_grammar]):
                        if self.current_token == "$":
                            self.errors.append([ErrorTypes.UNEXPECTED_EOF, self.scanner.get_line_number() + 1, None])
                            print(ErrorTypes.UNEXPECTED_EOF, self.scanner.get_line_number() + 1, None)
                            self.write_to_file()
                            return
                        self.errors.append([ErrorTypes.ILLEGAL, line_number, self.p_token.code_value])
                        print(ErrorTypes.ILLEGAL, line_number, self.p_token.code_value)
                        self.get_next_token()
                        self.is_stable = False
                    else:
                        self.errors.append([ErrorTypes.MISSING, line_number, self.cur_state.main_grammar])
                        print(ErrorTypes.ILLEGAL, line_number, self.cur_state.main_grammar)
                        self.pop()
                        self.cur_state = self.pop()
                        self.is_stable = False

            if len(self.stack) < 2:
                break

            self.is_stable = True
            self.pop()
            self.cur_state = self.pop()
            self.current_node = self.current_node.parent

        if self.stack[0].number == 0 and self.current_token == "$":
            print("accepted")

        if not self.is_stable:
            self.errors.append([ErrorTypes.UNEXPECTED_EOF, self.scanner.get_line_number() + 1, None])

        self.write_to_file()
    def print_tree(self):
        tree = ''
        for pre, fill, node in RenderTree(self.root):
            tree += "%s%s\n" % (pre, node.name)
        print(tree)

    def write_to_file(self, address='/parse_tree.txt', syntax_errors_address='/syntax_errors.txt'):
        tree = ''
        for pre, fill, node in RenderTree(self.root):
            tree += "%s%s\n" % (pre, node.name)

        syntax_errors = ''

        if len(self.errors) == 0:
            syntax_errors = 'There is no syntax error.'
        else:
            for error_type, line, error in self.errors:
                if error_type == ErrorTypes.ILLEGAL:
                    syntax_errors += f'#{line} : syntax error, illegal {error}\n'
                elif error_type == ErrorTypes.MISSING:
                    syntax_errors += f'#{line} : syntax error, missing {error}\n'
                elif error_type == ErrorTypes.UNEXPECTED_EOF:
                    syntax_errors += f'#{line} : syntax error, Unexpected EOF\n'

        with open(self.save_path + address, "w", encoding="utf-8") as opened_file:
            opened_file.write(tree)
        opened_file.close()

        with open(self.save_path + syntax_errors_address, "w", encoding="utf-8") as opened_file:
            opened_file.write(syntax_errors)
        opened_file.close()



# for i in range(1,6):
#     save_path = ".//PA2_testcases/T0"+str(i)
#     scanner_path = ".//PA2_testcases/T0"+str(i)
#     p = Parser(scanner_path,save_path)
#     p.parse()


save_path = "."
scanner_path = ".//PA2_testcases/T08"
p = Parser(scanner_path,save_path)
p.parse()