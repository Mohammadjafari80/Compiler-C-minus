from enum import Enum


class VarTYPE(Enum):
    var = "var"
    func = "function"
    array = "array"


class Type(Enum):
    INT = "int"
    VOID = "void"


class Record:
    def __init__(self, lexeme, scope_number):
        self.lexeme = lexeme
        self.type = Type.VOID
        self.args = 0
        self.var_type = VarTYPE.var
        self.scope_num = scope_number
        self.address = 0


class Scope:
    def __init__(self):
        self.scope_stack = []
        self.scope_record = []
        self.current_scope = 0

    def front(self):
        return self.scope_stack[self.current_scope]

    def insert_record(self, lexeme):
        self.scope_record.append(Record(lexeme, self.current_scope))

    def delete_current_scope(self):
        self.scope_stack.pop()
        self.current_scope -= 1

    def find_record(self, lexeme):
        last_scope_index = self.current_scope
        last_scope = self.front()
        last_record_index = len(self.scope_record)
        flag = True
        while flag:
            for index in range(last_scope, last_record_index):
                if lexeme == self.scope_record[index].lexeme:
                    return self.scope_record[index]
            last_scope_index -= 1
            last_scope = self.scope_stack[last_scope_index]
            last_record_index = last_scope
            if last_scope_index < 0:
                pass  # TODO NOT found

    def new_scope(self):
        self.current_scope += 1
        self.scope_stack.append(len(self.scope_record)-1)