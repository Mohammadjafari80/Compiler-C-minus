from enum import Enum


class VarTYPE(Enum):
    var = "var"
    func = "function"
    array = "array"


class Type(Enum):
    INT = "int"
    VOID = "void"


class Record:
    def __init__(self, lexeme, scope_number, args=0, type=Type.VOID, var_type=VarTYPE.var, address=0):
        self.lexeme = lexeme
        self.type = type
        self.args = args
        self.var_type = var_type
        self.scope_num = scope_number
        self.address = address

    def __str__(self):
        return f'lexeme : {self.lexeme} , type = {self.type} , args : {self.args} , var_type : {self.var_type} , scope_num : {self.scope_num} , address : {self.address}'

    def __repr__(self):
        return f'(lexeme={self.lexeme}, type={self.type}, args={self.args}, var_type={self.var_type}, scope={self.scope_num}, address={self.address})'


class Scope:
    def __init__(self):
        self.scope_stack = [0]
        self.scope_record = []
        self.current_scope = 0
        self.head_pointer = 0

    def front(self):
        return self.scope_stack[self.current_scope]

    def insert_record(self, lexeme, args=0, type=Type.VOID, var_type=VarTYPE.var, address=0):
        self.head_pointer += 1
        self.scope_record.append(Record(lexeme, self.current_scope, args, type, var_type, address))

    def delete_current_scope(self):
        begin = self.scope_stack.pop()
        for _ in range(self.head_pointer - begin - 1):
            self.scope_record.pop()
        self.head_pointer = begin + 1
        self.current_scope -= 1

    def find_record(self, lexeme):
        last_scope_index = self.current_scope
        last_scope = self.front()
        flag = True
        while flag:
            for index in range(last_scope, self.head_pointer):
                if lexeme == self.scope_record[index].lexeme:
                    return self.scope_record[index]
            last_scope_index -= 1
            last_scope = self.scope_stack[last_scope_index]
            if last_scope_index < 0:
                break

    def new_scope(self):
        self.current_scope += 1
        self.scope_stack.append(self.current_scope)

    def print_records(self):
        for p in self.scope_record:
            print(p)
