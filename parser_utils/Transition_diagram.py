from enum import Enum
class StateType(Enum):
    MID = "MID"
    START = "Start"
    ACC = "Acc"
import json
class state:
    def __init__(self,n,state_type = StateType.MID ):
        self.stateType = state_type
        if state_type != StateType.ACC:
            print(n)
        self.number = n
        self.states = {}
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
print(d.diagrams)