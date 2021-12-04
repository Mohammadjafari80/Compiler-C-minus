import Scanner
#import anytree
import parser_utils.Transition_diagram as TD
class parse_token:
    def __init__(self):
        self.type = None
        self.value = ""
        self.code_value = ""
    def set_info(self,token):
        token = token.split(",")
        self.value = token[0][1:]
        self.code_value = token[1][1:len(token[1])-1]

class parser:
    def __init__(self,scanner_path):
        self.transition_diagram = TD.diagram()
        self.diagrams = self.transition_diagram.diagrams
        self.first = self.transition_diagram.first
        self.follow = self.transition_diagram.follow
        self.predict = self.transition_diagram.predict
        self.NT = self.transition_diagram.non_terminals
        self.T = self.transition_diagram.terminals
        print(self.T)
        self.stateN = self.transition_diagram.state_number
        self.scanner = Scanner.Scanner(scanner_path)
        self.stack = []
        self.push(self.diagrams[self.NT[0]])
        print(self.front())
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


    def parse(self):
        while(self.current_token !="$"):
            while self.cur_state.stateType != TD.StateType.ACC:
                for production in self.cur_state.states.keys():
                    if production in self.T:
                        return
                    else:
                        if self.p_token.code_value in self.first[production]:
                            self.push(self.cur_state.states[production])
                            self.push(self.diagrams[production])
                            break
                        else:
                            pass
                self.cur_state = self.front()
            self.current_token = self.scanner.get_next_token()





        pass
scanner_path = "./input.txt"
p = parser(scanner_path)
p.parse()