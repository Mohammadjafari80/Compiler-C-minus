from semantic_analyzer import semantic_analyzer as sa
from code_gen.Memory_handler import Memory
from scope_records import scope_record as sr
from collections import namedtuple
from code_gen.Break_handler import Break

""""
#push_type : pushing type of id into stack for future use
#declare_id :  declare id and push it
#finish_var_declare : pop two object 
#push_num : push constant number 
#end_array_declare : pop objext and number of required member and fill symbol table.
#into_scope : declare new scope
#outo_scope : delete last scope
#push_id : push address of id
#assign : pop two address assign tow each other
#indirect_adr : sum with array address and calculate new address
#push_op : push operand
#operate : pop two and get tempory address and calculate and push address
"""
Three_Address_Code = namedtuple('ThreeAddressCode', 'op y z x')


class CodeGenerator:
    def initial(self):
        self.before_call("a")
        i = int(self.semantic_analyzer.pop().val)
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('JP', "?", None, None))
        self.program_block[i - 1] = Three_Address_Code('ASSIGN', f'#{self.mem.get_front_code()}', f'@{self.mem.sp}',
                                                       None)
        self.program_block[i] = Three_Address_Code('ADD', f'#{4 * 1}', f'{self.mem.sp}', f'{self.mem.sp}')
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code(None, None, None, None))
        r = self.scope_record.insert_record("output", 1, "FUN", "void", self.mem.get_front_code())
        r.update_local_var()
        r.update_args()
        temp = self.mem.get_temp()
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code("ADD", "#4", f"@{self.mem.display}", temp))
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code("PRINT", temp, None, None))
        size = r.local_var
        self.pop_run_time_stack(size)
        self.reverse_display()
        temp = self.mem.get_temp()
        self.mem.get_program_block(), self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', f"@{self.mem.sp}", temp, None))
        self.pop_run_time_stack()
        self.program_block.append(Three_Address_Code('JP', f"@{temp}", None, None))

    def set_main_address(self, address):
        self.program_block[self.init_main_pb] = Three_Address_Code('JP', address, None, None)

    def __init__(self, parser):
        self.init_main_pb = 5
        self.parser = parser
        self.semantic_analyzer = sa.SemanticAnalyzer()
        self.mem = Memory()
        self.breakH = Break()
        self.program_block = []
        self.scope_record = sr.Scope(self)
        self.routine_dict = dict()
        self.routine_dict['#push_type'] = self.push_type
        self.routine_dict['#declare_id'] = self.declare_id
        self.routine_dict['#finish_var_declare'] = self.finish_var_declare
        self.routine_dict['#push_num'] = self.push_num
        self.routine_dict['#end_array_declare'] = self.end_array_declare
        self.routine_dict['#into_scope'] = self.into_scope
        self.routine_dict['#outo_scope'] = self.out_of_scope
        self.routine_dict['#push_id'] = self.push_id
        self.routine_dict['#assign'] = self.assign
        self.routine_dict['#indirect_adr'] = self.indirect_adr
        self.routine_dict['#push_op'] = self.push_op
        self.routine_dict['#operate'] = self.operate
        self.routine_dict['#jump_repeat'] = self.jump_repeat
        self.routine_dict['#label'] = self.label
        self.routine_dict['#end_if_else'] = self.end_if_else
        self.routine_dict['#save_if_else'] = self.save_if_else
        self.routine_dict['#end_simple_if'] = self.end_simple_if
        self.routine_dict['#save_if'] = self.save_if
        self.routine_dict['#push'] = self.push
        self.routine_dict['#save_break'] = self.save_break
        self.routine_dict['#label_break_repeat'] = self.label_break_repeat
        self.routine_dict['#compare_operate'] = self.compare_operate
        self.routine_dict['#push_arg'] = self.push_arg
        self.routine_dict['#call'] = self.call

        self.routine_dict['#before_call'] = self.before_call
        self.routine_dict['#return_expression'] = self.return_expression
        self.routine_dict['#return_void'] = self.return_void
        self.routine_dict['#pop_exp'] = self.pop_exp
        self.routine_dict['#set_offset_function_arr'] = self.set_offset_function_arr
        self.routine_dict['#set_offset_function'] = self.set_offset_function
        self.routine_dict['#fun_declare_end'] = self.fun_declare_end
        self.routine_dict['#fun_declare_init'] = self.fun_declare_init
        self.initial()
        """
        #push_type : pushing type of id into stack for future use
#push_num : push constant number
#push_id : push address of id
#assign : pop two address assign tow each other
#indirect_adr : sum with array address and calculate new address
#push_op : push operand
#operate : pop two and get tempory address and calculate and push address
#label
#jump_repeat
#save_if
#end_simple_if
#save_if_else
#end_if_else
#compare_operate
#push_compare_operand
#fun_declare_init
#fun_declare_end
#set_offset_function
#set_offset_function_arr
#pop_exp
#return_void
#return_expresion

#before_call
#call
#push_arg



#declare_id :  declare id and push it
#finish_var_declare : pop two object
#end_array_declare : pop objext and number of required member and fill symbol table.
#into_scope : declare new scope
#outo_scope : delete last scope

        """

    def parse_token(self, token):
        lexeme = token.split(",")[1] if token != '$' else token
        lexeme = lexeme.replace(")", "")
        return (lexeme.strip())

    def generate_code(self, action, token):
        print(action)
        print("befor ---------------------------")
        print(self.print_program_block())
        print(self.scope_record.scope_stack)
        print(self.scope_record.print_records())
        print(self.semantic_analyzer.semantic_stack)
        print("after ---------------------------")
        self.routine_dict.get(action)(self.parse_token(token))
        print(self.print_program_block())
        print(self.scope_record.scope_stack)
        print(self.scope_record.print_records())
        print(self.semantic_analyzer.semantic_stack)

    def push_run_time_stack(self, val="#0", size=1):
        self.mem.get_program_block()
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', f'{val}', f'@{self.mem.sp}', None))
        self.program_block.append(Three_Address_Code('ADD', f'#{4 * size}', f'{self.mem.sp}', f'{self.mem.sp}'))

    def pop_run_time_stack(self, size=1):
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('SUB', f'{self.mem.sp}', f'#{size * 4}', f'{self.mem.sp}'))

    def save_break(self, token):
        i = self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('JP', "?", None, None))
        self.breakH.add_break(i)

    def label_break_repeat(self, token):
        self.semantic_analyzer.push(self.mem.get_front_code())
        self.breakH.add_repeat()

    def push_type(self, token):
        self.semantic_analyzer.push(val=token)

    def declare_id(self, token):  # TODO CHNAGE
        self.semantic_analyzer.push(val=token)

    def finish_var_declare(self, token):
        if self.scope_record.current_fun == None:
            lexeme, var_type = self.semantic_analyzer.pop().val, self.semantic_analyzer.pop().val
            address = self.mem.get_static_address()
            self.scope_record.insert_record(lexeme=lexeme, args=None, type='global_var', var_type=var_type,
                                            address=address)
        else:
            lexeme, var_type = self.semantic_analyzer.pop().val, self.semantic_analyzer.pop().val
            address = self.scope_record.current_fun.local_var
            self.scope_record.current_fun.update_local_var()
            self.mem.get_program_block()
            self.program_block.append(Three_Address_Code('ADD', f'#{4 * 1}', f'{self.mem.sp}', f'{self.mem.sp}'))
            self.scope_record.insert_record(lexeme=lexeme, args=None, type='local_var', var_type=var_type,
                                            address=address)

    def push(self, token):
        self.semantic_analyzer.push(val=token)  # it's actually a number

    def push_num(self, token):
        self.semantic_analyzer.push(val=f'#{token}')  # it's actually a number

    def end_array_declare(self, token):
        val = self.semantic_analyzer.pop().val
        val = val.replace("#", "")
        val = val.replace(" ", "")
        size = int(val)
        if self.scope_record.current_scope == 0:
            lexeme = self.semantic_analyzer.pop().val
            var_type = self.semantic_analyzer.pop().val
            address = self.mem.get_static_address(size * 4)
            self.scope_record.insert_record(lexeme=lexeme, args=size, type='global_var_arr', var_type=var_type,
                                            address=address, arr_size=size)
        else:
            lexeme, var_type = self.semantic_analyzer.pop().val, self.semantic_analyzer.pop().val
            address = self.scope_record.current_fun.local_var
            self.scope_record.current_fun.update_local_var(size)
            self.mem.get_program_block()
            self.program_block.append(Three_Address_Code('ADD', f'#{4 * size}', f'{self.mem.sp}', f'{self.mem.sp}'))
            self.scope_record.insert_record(lexeme=lexeme, args=None, type='local_var_arr', var_type=var_type,
                                            address=address, arr_size=size)

    def into_scope(self, token):
        self.scope_record.new_scope()

    def out_of_scope(self, token):
        if (
                self.scope_record.current_fun != None) and self.scope_record.current_fun.scope_num == self.scope_record.current_scope - 1:
            r = self.scope_record.current_fun
            size = r.local_var
            self.pop_run_time_stack(size)
            self.reverse_display()
            temp = self.mem.get_temp()
            self.mem.get_program_block()
            self.program_block.append(Three_Address_Code('ASSIGN', f"@{self.mem.sp}", temp, None))
            self.pop_run_time_stack()
            self.mem.get_program_block()
            self.program_block.append(Three_Address_Code('JP', f"@{temp}", None, None))
        self.scope_record.delete_current_scope()  # TODO check whether because we changed it

    def push_id(self, token):  # Not sure if that's what we were supposed to do #push all to stack
        lexeme = token
        address = self.scope_record.find_record(lexeme)
        self.semantic_analyzer.push(val=address)  # it's actually an address

    def analyse_id(self, val):
        if type(val) == sr.Record:
            if (val.type == "global_var_arr") or (val.type == "global_var"):
                return val.address
            if (val.type == "local_var_arr") or (val.type == "local_var") or (val.type == "arg_var"):
                size = (val.address + 1) * 4
                temp = self.mem.get_temp()
                self.mem.get_program_block()
                self.program_block.append(Three_Address_Code("ADD", f"#{size}", self.mem.display, temp))
                if val.type == "arg_var_arr":
                    self.program_block.append(Three_Address_Code("ASSIGN", f"@{temp}", temp, None))
                return f'@{temp}'

        return val

    def assign(self, token):  # todo
        address_rhs, address_lhs = self.analyse_id(self.semantic_analyzer.pop().val), self.analyse_id(
            self.semantic_analyzer.pop().val)
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', address_rhs, address_lhs, None))
        self.semantic_analyzer.push(address_lhs)

    def pop_exp(self, token):
        self.semantic_analyzer.pop()

    def indirect_adr(self, token):  # TODO _ change
        if self.parser.scanner.get_line_number() == 17:
            print("here")
        index = self.analyse_id(self.semantic_analyzer.pop().val)
        address = self.analyse_id(self.semantic_analyzer.pop().val)
        if type(index) == str and "#" in index:
            index = index.replace("#", "")
            index = index.replace(" ", "")
            size = int(index)
            if '@' in address:
                temp = self.mem.get_temp()
                self.mem.get_program_block()
                self.program_block.append(Three_Address_Code("ADD", f'{address}', f'#{size * 4}', temp))
                self.semantic_analyzer.push(f'@{temp}')
                return f'@{temp}'
            new_address = address + size * 4
            self.semantic_analyzer.push(val=new_address)
            return
        size = index
        temp = self.mem.get_temp()
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code("MULT", f'#4', size, temp))
        self.mem.get_program_block()
        if '@' in address:
            self.program_block.append(Three_Address_Code("ADD", f'{address}', temp, temp))
            self.semantic_analyzer.push(val=f'@{temp}')
            return  # it's actually an address not a Lexeme
        self.program_block.append(Three_Address_Code("ADD", f'#{address}', temp, temp))

    def push_op(self, token):
        self.semantic_analyzer.push(val=token)  # it's an operand

    def operate(self, token):  # todo CHECK
        rhs, op, lhs = self.analyse_id(self.semantic_analyzer.pop().val), \
                       self.semantic_analyzer.pop().val, \
                       self.analyse_id(self.semantic_analyzer.pop().val)
        temp = self.mem.get_temp()
        op = op.strip()
        operation = ''
        if op == '+':
            operation = 'ADD'
        elif op == '-':
            operation = 'SUB'
        elif op == '*':
            operation = 'MULT'
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code(operation, rhs, lhs, temp))
        self.semantic_analyzer.push(temp)

    def save_if(self, token):
        i = self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('JPF', self.semantic_analyzer.front().val, "?", None))
        self.semantic_analyzer.push(i)

    def end_simple_if(self, token):
        self.program_block[self.semantic_analyzer.pop().val] = Three_Address_Code('JPF',
                                                                                  self.semantic_analyzer.pop().val,
                                                                                  self.mem.get_front_code(), None)

    def save_if_else(self, token):
        i = self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('JP', "?", None, None))
        index = int(self.semantic_analyzer.pop().val)
        self.program_block[index] = Three_Address_Code('JPF',
                                                       self.semantic_analyzer.pop().val,
                                                       self.mem.get_front_code(), None)
        self.semantic_analyzer.push(i)

    def end_if_else(self, token):
        self.program_block[int(self.semantic_analyzer.pop().val)] = Three_Address_Code('JP',
                                                                                       self.mem.get_front_code(),
                                                                                       None,
                                                                                       None)

    def label(self, token):
        self.semantic_analyzer.push(self.mem.get_front_code())

    def jump_repeat(self, token):
        self.mem.get_program_block()
        # self.mem.get_program_block()
        A = self.semantic_analyzer.pop().val
        jp_add = self.semantic_analyzer.pop().val
        self.program_block.append(Three_Address_Code('JPF', A, jp_add, None))
        # self.program_block.append(Three_Address_Code('JP', jp_add, None, None))
        for index in self.breakH.get_breaks_address():
            self.program_block[index] = Three_Address_Code('JP', self.mem.get_front_code(), None, None)

    def push_compare(self, token):
        self.semantic_analyzer.push(token)

    def compare_operate(self, token):
        rhs, op, lhs = self.analyse_id(self.semantic_analyzer.pop().val), \
                       self.semantic_analyzer.pop().val, \
                       self.analyse_id(self.semantic_analyzer.pop().val)

        self.mem.get_program_block()
        temp = self.mem.get_temp()

        if op == '==':
            self.program_block.append(Three_Address_Code('EQ', rhs, lhs, temp))
        elif op == '<':
            self.program_block.append(Three_Address_Code('LT', rhs, lhs, temp))

        self.semantic_analyzer.push(temp)

    def print_program_block(self):
        for p in self.program_block:
            print(p)

    def before_call(self, token):
        self.mem.get_program_block()
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', "val", self.mem.return_val, None))
        self.program_block.append(Three_Address_Code('ASSIGN', "val", self.mem.return_val, None))
        self.semantic_analyzer.push(self.mem.get_front_code() - 1)
        self.save_stack_address_in_stack()

    def push_arg(self, token):
        self.push_run_time_stack(self.analyse_id(self.semantic_analyzer.pop().val))

    def call(self, token):
        i = self.semantic_analyzer.pop()
        record = self.semantic_analyzer.pop().val
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('JP', record.address, None, None))
        self.program_block[i - 1] = Three_Address_Code('ASSIGN', f'#{self.mem.get_front_code()}', f'@{self.mem.sp}',
                                                       None)
        self.program_block[i] = Three_Address_Code('ADD', f'#{4 * 1}', f'{self.mem.sp}', f'{self.mem.sp}')

    def fun_declare_init(self, token):
        lexeme, var_type = self.semantic_analyzer.pop().val, self.semantic_analyzer.pop().val
        r = self.scope_record.insert_record(lexeme=lexeme, args=0, type='FUN', var_type=var_type,
                                            address=self.mem.get_front_code())
        self.scope_record.current_fun = r
        self.scope_record.new_scope()
        self.scope_record.in_function = True

    def reverse_display(self):
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', f'@{self.mem.sp}', f'{self.mem.display}', None))
        self.pop_run_time_stack()

    def save_stack_address_in_stack(self):
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', f'{self.mem.sp}', f'{self.mem.display}', None))
        self.push_run_time_stack(self.mem.display, 1)

    def fun_declare_end(self, token):  # TODO
        pass

    def set_offset_function(self, token, ):
        lexeme, var_type = self.semantic_analyzer.pop().val, self.semantic_analyzer.pop().val
        address = self.scope_record.current_fun.args
        self.scope_record.current_fun.update_args()
        self.scope_record.insert_record(lexeme=lexeme, args=None, type='arg_var', var_type=var_type,
                                        address=address)

    def set_offset_function_arr(self, token):
        r = self.scope_record.get_last_record()
        r.type = 'arg_var_arr'

    def return_void(self, token):
        self.semantic_analyzer.push('void')
        pass

    def return_expression(self, token):  # TODO
        val = self.analyse_id(self.semantic_analyzer.pop().val)
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', val, self.mem.return_val, None))
        self.semantic_analyzer.push(self.mem.return_val)
