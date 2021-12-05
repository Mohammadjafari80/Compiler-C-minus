import Scanner
import anytree
# from  Any_tree import anytree as anytree
import parser_utils.Transition_diagram as TD
from anytree import Node, RenderTree

EPSILON = None


class ParseToken:
    def __init__(self):
        self.type = None
        self.value = ""
        self.code_value = ""

    def set_info(self, token):
        print(token)
        token = token.split(",")
        self.type = token[0][1:]
        self.value = token[1][1:len(token[1]) - 1]
        if self.type == "KEYWORD" or self.type == "SYMBOL":
            self.code_value = token[1][1:len(token[1]) - 1]
        elif self.type == "NUM" or self.type == "ID":
            self.code_value = self.type


class Parser:

    def __init__(self, path):
        self.transition_diagram = TD.Diagram()
        self.diagrams = self.transition_diagram.diagrams
        self.first = self.transition_diagram.first
        self.follow = self.transition_diagram.follow
        self.predict = self.transition_diagram.predict
        self.NT = self.transition_diagram.non_terminals
        self.T = self.transition_diagram.terminals
        self.stateN = self.transition_diagram.state_number
        self.scanner = Scanner.Scanner(path)
        self.stack = []
        self.push(self.diagrams[self.NT[0]])
        self.current_token = self.scanner.get_next_token()
        self.cur_state = self.front()
        self.p_token = ParseToken()
        self.p_token.set_info(self.current_token)
        self.root = Node(self.cur_state.main_grammar)
        self.current_node = self.root

    def front(self) -> TD.State:
        return self.stack[len(self.stack) - 1]

    def pop(self) -> TD.State:
        return self.stack.pop()

    def push(self, node: TD.State):
        self.stack.append(node)

    def get_next_token(self):
        self.current_token = self.scanner.get_next_token()
        if self.current_token != "$":
            self.p_token.set_info(self.current_token)
        else:
            self.p_token.code_value = "$"

    def print_stack(self):
        for i in self.stack:
            if str(i) == "62":
                print(end="")
            print(i, end=" ")
        print("")

    def handle_epsilons(self, state, node):
        print(state.states.keys())
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
                self.print_stack()
                for production in self.cur_state.states.keys():
                    if production in self.T:
                        if production == self.p_token.code_value:
                            temp = self.cur_state.states.get(production, None)
                            if temp is not None:
                                Node(f'({self.p_token.type}, {self.p_token.value})' if production != '$' else '$',
                                     parent=self.current_node)
                                self.cur_state = temp
                                self.get_next_token()
                                break

                    else:
                        if self.p_token.code_value in self.first[production]:
                            self.current_node = Node(self.diagrams[production].main_grammar, parent=self.current_node)
                            self.push(self.cur_state.states[production])
                            self.push(self.diagrams[production])
                            self.cur_state = self.front()
                            break
                        elif EPSILON in self.first[production]:
                            a = Node(self.diagrams[production].main_grammar, parent=self.current_node)
                            self.cur_state = self.cur_state.states[production]
                            self.handle_epsilons(self.diagrams[production], a)
                else:
                    if (EPSILON in self.first[self.cur_state.main_grammar] and
                            self.p_token.code_value in self.follow[self.cur_state.main_grammar]):
                        self.pop()
                        self.cur_state = self.pop()
                        self.current_node = self.current_node.parent

            if len(self.stack) < 2:
                break
            self.pop()
            self.cur_state = self.pop()
            self.current_node = self.current_node.parent
        if self.stack[0].number == 0 and self.current_token == "$":
            print("accepted")
        self.write_to_file()

    def write_to_file(self, address='./parse_tree.txt'):
        tree = ''
        for pre, fill, node in RenderTree(self.root):
            tree += "%s%s\n" % (pre, node.name)

        with open(address, "w", encoding="utf-8") as opened_file:
            opened_file.write(tree)

scanner_path = ".//PA2_testcases/T05/input.txt"
p = Parser(scanner_path)
p.parse()
print(p.stack)
