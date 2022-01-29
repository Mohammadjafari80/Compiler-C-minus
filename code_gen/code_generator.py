from semantic_analyzer import semantic_analyzer as sa
from code_gen.Memory_handler import Memory
from scope_records import scope_record as sr

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


class CodeGenerator:


    def __init__(self):
        self.semantic_analyzer = sa.SemanticAnalyzer()
        self.mem = Memory()
        self.scope_record = sr.Scope()
        self.routine_dict = dict()
        self.routine_dict["#push_type"] = self.push_type

    def generate_code(self, action, token):
        self.routine_dict.get(action)(token)

    def push_type(self, token):
        self.semantic_analyzer.push(type=token)

    def declare_id(self, token):
        self.semantic_analyzer.push(lexeme=token)





c = CodeGenerator()
c.generate_code("#push_type", "int")
