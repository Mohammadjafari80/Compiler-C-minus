from semantic_analyzer import semantic_analyzer as sa
from code_gen.Memory_handler import Memory
from scope_records import scope_record as sr
from collections import namedtuple
import code_gen.Break_handler as bh

"""
# num
address
! ooffset
@ address
"""

Three_Address_Code = namedtuple('ThreeAddressCode', 'op y z x')
ops = {'+': 'ADD', '-': 'SUB', '*': 'MULT'}


class CodeGenerator:
    def __init__(self, parser):
        # self.init_main_pb = 5
        self.parser = parser
        self.scope_record = sr.Scope(self)
        self.routine_dict = dict()
        self.routine_dict['#push_id'] = self.push_id
        self.routine_dict['#push_op'] = self.push_op
        self.routine_dict['#push_type'] = self.push_type
        self.routine_dict['#decl_id'] = self.decl_id
        self.routine_dict['#end_decl_var'] = self.end_decl_var
        self.routine_dict['#end_decl_arr'] = self.end_decl_arr
        self.routine_dict['#push_num'] = self.push_num
        self.routine_dict['#push_num_temp'] = self.push_num_temp
        self.routine_dict['#end_arr_param'] = self.end_arr_param
        self.routine_dict['#end_var_param'] = self.end_var_param
        self.routine_dict['#pop_exp'] = self.pop_exp
        self.routine_dict['#fun_declare_init'] = self.fun_declare_init
        self.routine_dict['#into_scope'] = self.into_scope
        self.routine_dict['#return_void'] = self.return_void
        self.routine_dict['#return_exp'] = self.return_exp
        self.routine_dict['#outo_scope'] = self.outo_scope
        self.routine_dict['#fun_declare_end'] = self.fun_declare_end
        self.routine_dict['#jump_over_func'] = self.jump_over_func
        self.routine_dict["find_function"] = self.find_function
        self.routine_dict['#operate'] = self.operate
        self.routine_dict['#indirect_addr'] = self.indirect_addr
        self.routine_dict['#assign_to_local'] = self.assign_to_local
        self.routine_dict['#call_func'] = self.call_func
        self.routine_dict['#assign'] = self.assign
        self.routine_dict['#jp_main'] = self.jp_main

        self.routine_dict['#save_label'] = self.save_label
        self.routine_dict['#if_jpf'] = self.if_jpf
        self.routine_dict['#if_jpf_save_label'] = self.if_jpf_save_label
        self.routine_dict['#then_jp'] = self.then_jp
        self.routine_dict['#label'] = self.label
        self.routine_dict['#repeat_jump'] = self.repeat_jump
        self.routine_dict["save_break"] = self.save_break
        self.semantic_analyzer = sa.SemanticAnalyzer()
        self.mem = Memory(self)
        self.program_block = []
        self.PC = self.mem.code_add
        self.BH = bh.Break()
        self.RT = bh.Return()
        self.function_to_call = None
        self.output_flag = False
        self.cond_jumps = []

    def save_label(self, token):
        self.semantic_analyzer.push(self.PC)
        self.jumps.append(self.PC)
        self.add_command(Three_Address_Code('JPF', '?', '?', ))

    def if_jpf(self, token):
        address, cond = self.semantic_analyzer.pop(), self.analyze_exp(self.semantic_analyzer.pop())
        self.update_command(self.cond_jumps[-1], Three_Address_Code('JPF', cond, address))
        self.cond_jumps.pop()

    def if_jpf_save_label(self, token):
        pass

    def then_jp(self, token):
        pass

    def label(self, token):
        self.BH.add_repeat()

    def repeat_jump(self, token):
        break_list = self.BH.get_breaks_address()
        for br_index in break_list:
            self.update_command(br_index, Three_Address_Code('JP', self.PC, None, None))

    def save_break(self, token):
        self.BH.add_break(self.PC)
        self.add_command(Three_Address_Code('?', None, None, None))

    def assign_to_local(self, token):
        # offset = self.get_offset_temp()
        pass

    def assign(self, token):
        rhs, lhs = self.semantic_analyzer.pop(), self.semantic_analyzer.pop()
        rhsA, lhsA = self.analyze_exp(rhs), self.analyze_exp(lhs, right=False)
        self.add_command(Three_Address_Code("ASSIGN", rhsA, lhsA, None))
        self.semantic_analyzer.push(lhs)

    def jp_main(self, token):
        r = self.scope_record.find_record('main')
        self.function_to_call = r
        self.call_func("a", if_main=True)
        # Whatever we do in call_func

    def find_function(self, token):
        if token == "output":
            self.output_flag = True
            return
        r = self.scope_record.find_record(self.semantic_analyzer.pop())
        self.function_to_call = r

    def call_func(self, token, if_main=False):
        if self.output_flag:
            value_to_print = self.analyze_exp(self.semantic_analyzer.pop())
            self.add_command(Three_Address_Code("PRINT", value_to_print, None, None))
            self.output_flag = False
            return
        arg_num = self.function_to_call.args
        offset = self.function_to_call.local_arr + 1
        arg_arr = []
        for i in range(arg_num):
            arg_arr.append(self.semantic_analyzer.pop())
        arg_arr = arg_arr[::-1]
        save_address = self.PC
        self.add_command(Three_Address_Code("?", None, None, None))  # offset + 1 #TODO return
        self.add_command(Three_Address_Code("?", None, None, None))  # offset + 1 #TODO return
        self.add_command(Three_Address_Code("?", None, None, None))  # offset + 1 #TODO return
        self.add_command(Three_Address_Code("?", None, None, None))  # offset + 1 #TODO return
        temp = self.mem.get_static_address()
        for (i, a) in enumerate(arg_arr):
            self.add_command(Three_Address_Code("ADD", f'#{(offset + i + 2) * 4}', self.mem.activation_record, temp))
            self.add_command(Three_Address_Code("ASSIGN", self.analyze_exp(a), f'@{temp}', None))
        self.update_command(save_address + 2, Three_Address_Code("ASSIGN", f'#{(1 + offset) * 4}', f'{temp}', None))
        self.update_command(save_address + 3,
                            Three_Address_Code("ASSIGN", self.mem.activation_record, f'@{temp}', None))
        self.add_command(Three_Address_Code("ADD", f'#{(offset) * 4}', self.mem.activation_record, temp))
        self.add_command(Three_Address_Code("ASSIGN", temp, self.mem.activation_record, None))
        self.add_command(Three_Address_Code("JP", self.function_to_call.address, None, None))
        self.update_command(save_address, Three_Address_Code("ASSIGN", f'#{offset * 4}', f'{temp}', None))
        self.update_command(save_address + 1, Three_Address_Code("ASSIGN", f'#{self.PC}', f'@{temp}', None))
        self.add_command(
            Three_Address_Code("ASSIGN", f'@{self.function_to_call.address}', self.mem.activation_record, None))
        offset = self.get_offset_temp()
        self.add_command(Three_Address_Code("ADD", f"#{offset * 4}", self.mem.activation_record, temp))
        self.add_command(
            Three_Address_Code("ASSIGN", f'{self.mem.return_val}', f'@{temp}', None))
        if if_main:
            self.add_command(Three_Address_Code("JP", "#5000000000000", None, None))
        self.semantic_analyzer.push(f'!{offset}')

    def analyze_exp(self, exp, right=True):  # TODO just for read
        if "!" in exp:
            temp = self.mem.get_static_address()
            exp = exp.replace("!", "")
            if "@" in exp:
                exp = int(exp.replace("@", ""))
                exp = int(exp)
                self.add_command(Three_Address_Code("ADD", f'#{exp * 4}', self.mem.activation_record, temp))
                self.add_command(Three_Address_Code("ASSIGN", f'@{temp}', temp))
                if right:
                    self.add_command(Three_Address_Code("ASSIGN", f'@{temp}', temp))
                    return temp
                return f'@{temp}'
            exp = int(exp)
            self.add_command(Three_Address_Code("ADD", f'#{exp * 4}', self.mem.activation_record, temp))
            if not right:
                return f'@{temp}'
            self.add_command(Three_Address_Code("ASSIGN", f'@{temp}', temp))
            return f'{temp}'
        elif right:
            temp = self.mem.get_static_address()
            self.add_command(Three_Address_Code("ASSIGN", exp, temp, None))
            return temp
        return exp

    def get_offset_temp(self):
        fun = self.scope_record.current_fun
        address = fun.updat_local_var()
        return address

    def operate(self, token):
        rhs, op, lhs = self.semantic_analyzer.pop(), self.semantic_analyzer.pop(), self.semantic_analyzer.pop()
        op = op.strip()
        offset = self.get_offset_temp()
        operation = ops[op]
        temp = self.mem.get_static_address()
        rhs, lhs = self.analyze_exp(rhs), self.analyze_exp(lhs)
        self.add_command(Three_Address_Code("ADD", f"#{offset * 4}", self.mem.activation_record, temp))
        self.add_command(Three_Address_Code(operation, rhs, lhs, f'@{temp}'))
        self.semantic_analyzer.push(f'!{offset}')

    def indirect_addr(self, token):
        index, address = self.semantic_analyzer.pop(), self.semantic_analyzer.pop()
        index = self.analyze_exp(index)
        address = self.analyze_exp(address)
        offset = self.get_offset_temp()
        temp2 = self.mem.get_static_address()
        self.add_command(Three_Address_Code("MUL", index, f'#{4}', temp2))
        self.add_command(Three_Address_Code("ADD", temp2, address, temp2))
        temp = self.mem.get_static_address()
        self.add_command(Three_Address_Code("ADD", f"#{offset * 4}", self.mem.activation_record, temp))
        self.add_command(Three_Address_Code("ASSIGN", temp2, f'@{temp}', None))
        self.semantic_analyzer.push(f"@!{offset}")

    def return_void(self, token):
        self.RT.add_return(self.PC)
        self.add_command(Three_Address_Code("JP", "?", None, None))

    def return_exp(self, token):
        exp = self.semantic_analyzer.pop()
        add = self.analyze_exp(exp)
        self.add_command(Three_Address_Code("ASSIGN", add, self.mem.return_val, None))
        self.RT.add_return(self.PC)
        self.add_command(Three_Address_Code("JP", "?", None, None))
        # TODO

    def outo_scope(self, token):
        for index in self.RT.q:
            self.update_command(index, Three_Address_Code("JP", self.PC, None, None))  # TODO fill return packing
        temp = self.mem.get_static_address()
        self.add_command(Three_Address_Code("SUB", "#4", self.mem.activation_record, temp))
        self.add_command(Three_Address_Code("ASSIGN", f"@{temp}", temp, None))
        self.add_command(
            Three_Address_Code("ASSIGN", f"@{self.mem.activation_record}", self.mem.activation_record,
                               None))  # TODO save display ghabli ro be display felli
        self.add_command(Three_Address_Code("JP", f'@{temp}', None, None))  # TODO jump return address

        # self.add_command(Three_Address_Code("ASSIGN", "#0", temp, None))

        self.scope_record.delete_current_scope()

    def jump_over_func(self, token):
        pass

    def fun_declare_end(self, token):
        pass

    def into_scope(self, token):
        self.scope_record.new_scope()

    def fun_declare_init(self, token):
        lexeme, var_type = self.semantic_analyzer.pop(), self.semantic_analyzer.pop()
        r = self.scope_record.insert_record(lexeme=lexeme, var_type=var_type, type="FUN", address=self.PC)
        self.scope_record.current_fun = r

    def end_arr_param(self, token):
        lexeme, var_type = self.semantic_analyzer.pop(), self.semantic_analyzer.pop()
        fun = self.scope_record.current_fun
        address = fun.update_args()
        self.scope_record.insert_record(lexeme=lexeme, var_type=var_type, type="arg_arr", address=address)

    def end_var_param(self, token):
        lexeme, var_type = self.semantic_analyzer.pop(), self.semantic_analyzer.pop()
        fun = self.scope_record.current_fun
        address = fun.update_args()
        self.scope_record.insert_record(lexeme=lexeme, var_type=var_type, type="arg_var", address=address)

    def end_decl_arr(self, token):
        num, lexeme, var_type = self.semantic_analyzer.pop(), self.semantic_analyzer.pop(), self.semantic_analyzer.pop()
        num = int(num.replace("#", ""))
        if self.scope_record.current_scope == 0:
            temp = self.mem.get_static_address()
            self.scope_record.insert_record(lexeme=lexeme, var_type=var_type, type="global_arr", address=temp, size=num)
            self.add_command(Three_Address_Code("ASSIGN", f"#{temp}", temp, None))
            for i in range(0, num):
                temp = self.mem.get_static_address()
                self.add_command(Three_Address_Code("ASSIGN", "#0", temp, None))
            return
        fun = self.scope_record.current_fun
        offset = fun.updat_local_var(num + 1)
        self.scope_record.insert_record(lexeme=lexeme, var_type=var_type, type="local_arr", address=offset)
        temp = self.mem.get_static_address()
        temp_2 = self.mem.get_static_address()
        self.add_command(Three_Address_Code("ADD", f"#{(offset * 4)}", self.mem.activation_record, temp))
        self.add_command(Three_Address_Code("ADD", f"#4", temp, temp_2))
        self.add_command(Three_Address_Code("ASSIGN", f'{temp_2}', f'@{temp}', None))
        for i in range(1, num + 1):
            self.add_command(Three_Address_Code("ADD", f"#{(offset + i) * 4}", self.mem.activation_record, temp))
            self.add_command(Three_Address_Code("ASSIGN", "#0", f'@{temp}', None))
        return

    def end_decl_var(self, token):
        lexeme, var_type = self.semantic_analyzer.pop(), self.semantic_analyzer.pop()
        if self.scope_record.current_scope == 0:
            temp = self.mem.get_static_address()
            self.scope_record.insert_record(lexeme=lexeme, var_type=var_type, type="global_var", address=temp)
            self.add_command(Three_Address_Code("ASSIGN", "#0", temp, None))
            return
        fun = self.scope_record.current_fun
        address = fun.updat_local_var()
        self.scope_record.insert_record(lexeme=lexeme, var_type=var_type, type="local_var", address=address)
        temp = self.mem.get_static_address()
        self.add_command(Three_Address_Code("ADD", f"#{address * 4}", self.mem.activation_record, temp))
        self.add_command(Three_Address_Code("ASSIGN", "#0", f'@{temp}', None))
        return

    def add_command(self, tp):
        self.program_block.append(tp)
        self.PC += 1

    def update_command(self, index, tp):
        self.program_block[index] = tp

    def get_command(self, index):
        return self.program_block[index]

    def push_type(self, token):
        self.semantic_analyzer.push(token)

    def push_op(self, token):
        self.semantic_analyzer.push(token)

    def push_num(self, token):
        self.semantic_analyzer.push(f'#{token}')

    def push_num_temp(self, token):
        num = int(token)
        temp = self.mem.get_static_address()
        self.add_command(Three_Address_Code('ASSIGN', f'#{num}', temp, None))
        self.semantic_analyzer.push(f'{temp}')

    def pop_exp(self, token):
        self.semantic_analyzer.pop()

    def push_id(self, token):
        record = self.scope_record.find_record(token)
        if record.scope_num == 0:
            if record.type == 'FUN':
                self.semantic_analyzer.push(token)
            else:
                self.semantic_analyzer.push(record.address)
        else:
            self.semantic_analyzer.push(f'!{record.address}')
