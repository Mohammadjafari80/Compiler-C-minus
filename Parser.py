import Scanner
import anytree
#from  Any_tree import anytree as anytree
import parser_utils.Transition_diagram as TD
from anytree import Node, RenderTree
udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)
print(joe)
class parse_token:
    def __init__(self):
        self.type = None
        self.value = ""
        self.code_value = ""
    def set_info(self,token):
        print(token)
        token = token.split(",")
        self.type = token[0][1:]
        self.value =  token[1][1:len(token[1])-1]
        if self.type == "KEYWORD"  or  self.type=="SYMBOL":
            self.code_value = token[1][1:len(token[1])-1]
        elif self.type == "NUM" or self.type == "ID":
            self.code_value = self.type
class parser:
    def __init__(self,scanner_path):
        self.transition_diagram = TD.diagram()
        self.diagrams = self.transition_diagram.diagrams
        self.first = self.transition_diagram.first
        self.follow = self.transition_diagram.follow
        self.predict = self.transition_diagram.predict
        self.NT = self.transition_diagram.non_terminals
        self.T = self.transition_diagram.terminals
        self.stateN = self.transition_diagram.state_number
        self.scanner = Scanner.Scanner(scanner_path)
        self.stack = []
        self.push(self.diagrams[self.NT[0]])
        self.current_token = self.scanner.get_next_token()
        self.cur_state = self.front()
        self.p_token = parse_token()
        self.p_token.set_info(self.current_token)
    def front(self)-> TD.state:
        return self.stack[len(self.stack)-1]
    def pop(self)-> TD.state:
        return self.stack.pop()
    def push(self,node:TD.state):
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
               print(end = "")
            print(i,end=" ")
        print("")
    def parse(self): # TODO add panic mode recovery and also add tree
        while(True):
            while self.cur_state.stateType != TD.StateType.ACC:
                self.print_stack()
                for production in self.cur_state.states.keys():
                    if production in self.T:
                        if production == self.p_token.code_value:
                            temp = self.cur_state.states.get(production,None)
                            if temp != None:
                                self.cur_state = temp
                                self.get_next_token()
                                break
                    else:
                        if self.p_token.code_value in self.first[production]:
                            self.push(self.cur_state.states[production])
                            self.push(self.diagrams[production])
                            self.cur_state = self.front()
                            break
                        elif (None in self.first[production]):
                            self.cur_state = self.cur_state.states[production]

                else:
                    if (None in self.first[self.cur_state.main_grammer] and self.p_token.code_value in self.follow[self.cur_state.main_grammer]):
                        self.pop()
                        self.cur_state = self.pop()

            if len(self.stack) < 2:
                break
            self.pop()
            self.cur_state = self.pop()
        if self.stack[0].number == 0 and self.current_token == "$":
            print("accepted")
scanner_path = "./p2Test/PA2_testcases/T05/input.txt"
p = parser(scanner_path)
p.parse()
print(p.stack)