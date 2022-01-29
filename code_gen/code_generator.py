from semantic_analyzer import semantic_analyzer as sa
from code_gen.Memory_handler import Memory
from scope_records import scope_record as sr
from collections import namedtuple


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


    def __init__(self):
        self.semantic_analyzer = sa.SemanticAnalyzer()
        self.mem = Memory()
        self.program_block = []
        self.scope_record = sr.Scope()
        self.routine_dict = dict()
        self.routine_dict['#push_type'] = self.push_type
        self.routine_dict['#declare_id'] = self.declare_id
        self.routine_dict['#finish_var_declare'] = self.finish_var_declare
        self.routine_dict['#push_num'] = self.push_num
        self.routine_dict['#end_array_declare'] = self.end_array_declare
        self.routine_dict['#into_scope'] = self.into_scope
        self.routine_dict['#out_of_scope'] = self.out_of_scope
        self.routine_dict['#indirect_adr'] = self.indirect_adr
        self.routine_dict['#push_op'] = self.push_op
        self.routine_dict['#operate'] = self.operate


    def generate_code(self, action, token):
        self.routine_dict.get(action)(token)

    def push_type(self, token):
        self.semantic_analyzer.push(val=token)

    def declare_id(self, token):
        self.semantic_analyzer.push(val=token)

    def finish_var_declare(self, token):
        lexeme, var_type = self.semantic_analyzer.pop().val, self.semantic_analyzer.pop().val
        address = self.mem.get_static_address()
        self.scope_record.insert_record(lexeme=lexeme, args=None, type=var_type, address=address)

    def push_num(self, token):
        self.semantic_analyzer.push(val=token)  # it's actually a number

    def end_array_declare(self, token):
        size = int(self.semantic_analyzer.pop().val)
        lexeme = self.semantic_analyzer.pop().val
        var_type = self.semantic_analyzer.pop().type
        address = self.memory.get_static_address(size*4)
        self.scope_record.insert_record(lexeme=lexeme, args=size, type=var_type, address=address)

    def into_scope(self, token):
        self.scope_record.new_scope()

    def out_of_scope(self, token):
        self.scope_record.delete_current_scope()

    def push_id(self, token): # Not sure if that's what we were supposed to do
        lexeme = token
        address = self.scope_record.find_record(lexeme).address
        self.semantic_analyzer.push(lexeme=address)  # it's actually an address

    def assign(self, token):
        self.mem.get_temp(), self.get_temp() # just because we have to?
        address_rhs, address_lhs = self.semantic_analyzer.pop().lexeme, self.semantic_analyzer.pop().lexeme
        address = Memory.get_program_block()
        self.program_block.append(Three_Address_Code(':=', address_rhs, address_lhs, None))

    def indirect_adr(self, token):
        index = int(self.semantic_analyzer.pop.lexeme)
        lexeme = self.semantic_analyzer.pop().lexeme
        address = self.scope_record.find_record(lexeme)
        new_address = address + index
        self.semantic_analyzer.push(lexeme=new_address) # it's actually an address not a Lexeme

    def push_op(self, token):
        self.semantic_analyzer.push(lexeme=token) # it's an operand

    def operate(self, token):
        rhs, op, lhs = self.semantic_analyzer.pop().lexeme,\
                       self.semantic_analyzer.pop().lexeme,\
                       self.semantic_analyzer.pop().lexeme
        temp = self.mem.get_temp()
        address = Memory.get_program_block()
        self.program_block.append(Three_Address_Code(op, rhs, lhs, temp))

