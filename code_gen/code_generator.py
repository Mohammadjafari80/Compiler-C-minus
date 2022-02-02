from semantic_analyzer import semantic_analyzer as sa
from code_gen.Memory_handler import Memory
from scope_records import scope_record as sr
from collections import namedtuple
from code_gen.Break_handler import Break
import scope_records

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
        index = self.mem.get_program_block()
        self.init_main_pb = index
        self.program_block.append(Three_Address_Code('JP', "?", None, None))
        self.program_block[i - 1] = Three_Address_Code('ASSIGN', f'#{self.mem.get_front_code()}', f'@{self.mem.sp}',
                                                       None)
        self.program_block[i] = Three_Address_Code('ADD', f'#{4 * 1}', f'{self.mem.sp}', f'{self.mem.sp}')
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code(None, None, None, None))
        ''' # end of program '''
        r = self.scope_record.insert_record("output", 0, "FUN", "void", self.mem.get_front_code())
        self.scope_record.current_fun = r
        r.update_local_var()
        r.update_args()
        # temp = self.get_temp()
        # self.mem.get_program_block()
        # self.program_block.append(Three_Address_Code("ADD", "#4", f"@{self.mem.display}", temp))
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code("PRINT", f'@{self.mem.display}', None, None))
        size = r.local_var
        self.pop_run_time_stack(size)
        self.reverse_display()
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', f"@{self.mem.sp}", self.mem.return_add, None))
        self.pop_run_time_stack()
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('JP', f"@{self.mem.return_add}", None, None))
        self.return_void("a")
        (r, _) = self.handle_temp_for_stack(self.mem.return_val)
        self.semantic_analyzer.push(r)
        self.scope_record.current_fun = None

    def set_main_address(self, address):
        self.program_block[self.init_main_pb] = Three_Address_Code('JP', address, None, None)

    def __init__(self, parser):
        self.init_main_pb = 5
        self.parser = parser
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
        self.semantic_analyzer = sa.SemanticAnalyzer()
        self.mem = Memory(self)
        self.initial()
        self.last_print = 0

    def get_temp_exp(self, type='local_var'):
        self.scope_record.current_fun.update_local_var()
        address = self.scope_record.current_fun.local_var
        r = self.scope_record.insert_record(lexeme="temp", args=0, type=type, var_type='temp', address=address)
        self.push_run_time_stack()
        return r

    def get_temp(self):
        return self.mem.get_static_address()

    def parse_token(self, token):
        lexeme = token.split(",")[1] if token != '$' else token
        lexeme = lexeme.replace(")", "")
        return (lexeme.strip())

    def generate_code(self, action, token):
        print("-----------------------------------------------------------------------------------------------")
        print(action, token)
        self.routine_dict.get(action)(self.parse_token(token))
        self.print_program_block()
        print(self.semantic_analyzer.semantic_stack)
        self.scope_record.print_records()

    def push_run_time_stack(self, val="#0"):
        self.mem.get_program_block()
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', f'{val}', f'@{self.mem.sp}', None))
        self.program_block.append(Three_Address_Code('ADD', f'#{4}', f'{self.mem.sp}', f'{self.mem.sp}'))

    def assign_zero_to_stack(self, address):
        pass

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
            self.push_run_time_stack()
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
            for i in range(size):
                self.mem.get_program_block()
                self.program_block.append(Three_Address_Code('ASSIGN', f'#{0}', f'{address + 4 * i}', None))
            self.scope_record.insert_record(lexeme=lexeme, args=size, type='global_var_arr', var_type=var_type,
                                            address=address, arr_size=size)
        else:
            lexeme, var_type = self.semantic_analyzer.pop().val, self.semantic_analyzer.pop().val
            address = self.scope_record.current_fun.local_var
            self.scope_record.current_fun.update_local_var(size)
            for i in range(size):
                self.push_run_time_stack()
            self.scope_record.insert_record(lexeme=lexeme, args=None, type='local_var_arr', var_type=var_type,
                                            address=address, arr_size=size)

    def into_scope(self, token):
        self.scope_record.new_scope()

    def out_of_scope(self, token):
        if (self.scope_record.current_fun != None) and \
                self.scope_record.current_fun.scope_num == self.scope_record.current_scope - 1:
            r = self.scope_record.current_fun
            size = r.local_var
            self.pop_run_time_stack(size)
            self.reverse_display()
            temp = self.mem.return_add  #
            self.mem.get_program_block()
            self.program_block.append(Three_Address_Code('ASSIGN', f"@{self.mem.sp}", temp, None))
            self.pop_run_time_stack()
            self.mem.get_program_block()
            self.program_block.append(Three_Address_Code('JP', f"@{temp}", None, None))
            self.scope_record.current_fun = None

        self.scope_record.delete_current_scope()  # TODO check whether because we changed it

    def push_id(self, token):  # Not sure if that's what we were supposed to do #push all to stack
        lexeme = token
        address = self.scope_record.find_record(lexeme)
        self.semantic_analyzer.push(val=address)  # it's actually an address

    def analyse_id(self, val):
        try:
            val.address
            # if type(val) == sr.Record or type(val) == scope_records.scope_record.Record:

            if (val.type == "global_var_arr") or (val.type == "global_var"):
                return val.address
            if (val.type == "local_var_arr") or (val.type == "local_var") or (val.type == "arg_var") or (
                    val.type == "arg_var_arr"):
                size = (val.address) * 4
                temp = self.get_temp()
                self.mem.get_program_block()
                self.program_block.append(Three_Address_Code("ADD", f"#{size}", self.mem.display, temp))
                if val.type == "arg_var_arr":
                    self.mem.get_program_block()
                    self.program_block.append(Three_Address_Code("ASSIGN", f"@{temp}", temp, None))
                return f'@{temp}'
        except:
            return val

    def assign(self, token):
        address_rhs, address_lhs = self.semantic_analyzer.pop().val, self.semantic_analyzer.pop().val
        self.mem.get_program_block()
        self.program_block.append(
            Three_Address_Code('ASSIGN', self.analyse_id(address_rhs), self.analyse_id(address_lhs), None))
        self.semantic_analyzer.push(address_lhs)

    def pop_exp(self, token):
        self.semantic_analyzer.pop()

    def handle_num_indexing(self, index, address):
        (r, temp) = self.handle_temp_for_stack('#0', 'args_var_arr')
        self.mem.get_program_block()
        self.program_block.append(
            Three_Address_Code('ADD', f'#{index}', f'{address}', f'@{temp}'))
        return r

    def handle_add_indexing(self, index, address):
        (r, temp) = self.handle_temp_for_stack('#0', 'args_var_arr')
        self.mem.get_program_block()
        self.program_block.append(
            Three_Address_Code('ADD', f'{index}', f'{address}', f'@{temp}'))
        return r

    def handle_ind_record_indexing(self, index, address):
        pass

    def indirect_adr(self, token):  # TODO _ change
        index = self.analyse_id(self.semantic_analyzer.pop().val)
        address = self.analyse_id(self.semantic_analyzer.pop().val)
        (r, temp) = self.handle_temp_for_stack('#0', 'arg_var_arr')
        if type(address) == str and '@' in address:
            t = address.replace("@", "")
            self.mem.get_program_block()
            self.program_block.append(Three_Address_Code('ADD', f'{index}', f'{t}', f'@{temp}'))
        else:
            self.mem.get_program_block()
            self.program_block.append(Three_Address_Code('ADD', f'{index}', f'#{address}', f'@{temp}'))

        self.semantic_analyzer.push(r)

        # if type(index) == sr.Record:
        #   self.handle_ind_record_indexing(index, address)
        # else:# type(index) == str and "#" in index:
        #    self.program_block.append(Three_Address_Code('ADD', f'{index}', f'{address}', f'@{temp}'))
        # else:
        # self.program_block.append(Three_Address_Code('ADD', f'{index}', f'{address}', f'@{temp}'))

    def push_op(self, token):
        self.semantic_analyzer.push(val=token)  # it's an operand

    def operate(self, token):
        rhs, op, lhs = self.analyse_id(self.semantic_analyzer.pop().val), \
                       self.semantic_analyzer.pop().val, \
                       self.analyse_id(self.semantic_analyzer.pop().val)
        (r, temp) = self.handle_temp_for_stack("#0")
        op = op.strip()
        operation = ''
        if op == '+':
            operation = 'ADD'
        elif op == '-':
            operation = 'SUB'
        elif op == '*':
            operation = 'MULT'
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code(operation, rhs, lhs, f'@{temp}'))
        self.semantic_analyzer.push(r)

    def save_if(self, token):
        add = self.analyse_id(self.semantic_analyzer.pop().val)
        i = self.mem.get_program_block()
        self.program_block.append(
            Three_Address_Code('JPF', "?", "?", None))
        self.semantic_analyzer.push(add)
        self.semantic_analyzer.push(i)

    def end_simple_if(self, token):
        self.program_block[int(self.semantic_analyzer.pop().val)] = Three_Address_Code('JPF',
                                                                                       self.analyse_id(
                                                                                           self.semantic_analyzer.pop().val),
                                                                                       self.mem.get_front_code(), None)

    def save_if_else(self, token):
        i = self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('JP', "?", None, None))
        index = int(self.semantic_analyzer.pop().val)
        self.program_block[index] = Three_Address_Code('JPF',
                                                       self.analyse_id(self.semantic_analyzer.pop().val),
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
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code("PRINT", f'#{jp_add}', None, None))

        # self.program_block.append(Three_Address_Code('JP', jp_add, None, None))
        for index in self.breakH.get_breaks_address():
            self.program_block[index] = Three_Address_Code('JP', self.mem.get_front_code(), None, None)

    def push_compare(self, token):
        self.semantic_analyzer.push(token)

    def compare_operate(self, token):
        rhs, op, lhs = self.analyse_id(self.semantic_analyzer.pop().val), \
                       self.semantic_analyzer.pop().val, \
                       self.analyse_id(self.semantic_analyzer.pop().val)

        (r, temp) = self.handle_temp_for_stack("#0")
        self.mem.get_program_block()

        if op == '==':
            self.program_block.append(Three_Address_Code('EQ', rhs, lhs, f'@{temp}'))
        elif op == '<':
            self.program_block.append(Three_Address_Code('LT', rhs, lhs, f'@{temp}'))

        self.semantic_analyzer.push(r)

    def print_program_block(self):
        i = 0
        for p in self.program_block:
            if i >= self.last_print:
                print(f'{i} : {p}')
            i += 1
        self.last_print = i

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
        i = self.semantic_analyzer.pop().val
        record = self.semantic_analyzer.pop().val
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('JP', record.address, None, None))
        self.program_block[i - 1] = Three_Address_Code('ASSIGN', f'#{self.mem.get_front_code()}', f'@{self.mem.sp}',
                                                       None)

        self.program_block[i] = Three_Address_Code('ADD', f'#{4 * 1}', f'{self.mem.sp}', f'{self.mem.sp}')
        # TODO push return value to stack
        (r, _) = self.handle_temp_for_stack(self.mem.return_val)
        self.semantic_analyzer.push(r)

    def handle_temp_for_stack(self, val, type='local_var'):
        r = self.get_temp_exp(type)
        temp = self.get_temp()
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ADD', self.mem.display, f'#{(r.address) * 4}', temp))
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', val, f'@{temp}', None))
        return r, temp

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
        self.push_run_time_stack(self.mem.display)
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', f'{self.mem.sp}', f'{self.mem.display}', None))

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
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', "#0", self.mem.return_val, None))
        pass

    def return_expression(self, token):  # TODO
        val = self.analyse_id(self.semantic_analyzer.pop().val)
        self.mem.get_program_block()
        self.program_block.append(Three_Address_Code('ASSIGN', val, self.mem.return_val, None))
        # self.semantic_analyzer.push(self.mem.return_val)
