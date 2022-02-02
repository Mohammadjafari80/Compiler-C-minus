from enum import Enum


class VarTYPE(Enum):
    var = "var"
    func = "function"
    array = "array"


class Type(Enum):
    INT = "int"
    VOID = "void"


class Record:
    def __init__(self, lexeme, scope_number, args=0, type=Type.VOID, var_type=VarTYPE.var, address=0, arr_size=1):
        self.lexeme = lexeme
        self.type = type
        self.args = args
        self.var_type = var_type
        self.scope_num = scope_number
        self.address = address
        self.local_var = 0
        self.arr_size = arr_size

    def update_args(self, val=1):
        self.args += val
        self.local_var += val

    def update_local_var(self, val=1):
        self.local_var += val

    def __str__(self):
        return f'lexeme : {self.lexeme} , type = {self.type} , args : {self.args} , var_type : {self.var_type} , scope_num : {self.scope_num} , address : {self.address} , arr_size : {self.arr_size} , local_var : {self.local_var} '

    def __repr__(self):
        return f'(lexeme={self.lexeme}, type={self.type}, args={self.args}, var_type={self.var_type}, scope={self.scope_num}, address={self.address} , arr_size : {self.arr_size}) , local_var : {self.local_var} '


class Scope:
    def __init__(self, CG):
        self.scope_stack = [0]
        self.scope_record = []
        self.current_scope = 0
        self.head_pointer = 0
        self.current_fun = None
        self.in_function = False
        self.code_gen = CG

    def front(self):
        return self.scope_stack[self.current_scope]

    def insert_record(self, lexeme, args=0, type=Type.VOID, var_type=VarTYPE.var, address=0, arr_size=1):
        if lexeme == "main":
            self.code_gen.set_main_address(address)
        self.head_pointer += 1
        r = Record(lexeme, self.current_scope, args, type, var_type, address, arr_size)
        self.scope_record.append(r)
        return r


    def delete_current_scope(self):
        begin = self.scope_stack.pop()
        for _ in range(self.head_pointer - begin):
            deleted = self.scope_record.pop()
            if deleted.var_type == 'temp':
                self.code_gen.semantic_analyzer.pop()
                self.code_gen.mem.get_static_address(-4)
        self.head_pointer = begin
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
        if self.in_function:
            self.in_function = False
            return
        self.current_scope += 1
        self.scope_stack.append(self.head_pointer)

    def print_records(self):
        for p in self.scope_record:
            print(p)

    def get_last_record(self):
        return self.scope_record[len(self.scope_record) - 1]
