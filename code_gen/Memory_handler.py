from scope_records import scope_record as sr
from code_gen import code_generator


class Memory():
    def __init__(self, code_gen):
        self.code_add = 0
        self.sp = 5008
        self.display = 5004
        self.static_data = 3000
        self.return_val = 5000
        self.return_add = 4096
        self.code_g = code_gen
        self.get_program_block()
        self.code_g.program_block.append(code_generator.Three_Address_Code("ASSIGN", f"#{0}", self.return_add, None))
        self.get_program_block()
        self.code_g.program_block.append(code_generator.Three_Address_Code("ASSIGN", f"#{self.sp + 4}", self.sp, None))
        self.get_program_block()
        self.code_g.program_block.append(
            code_generator.Three_Address_Code("ASSIGN", f"#{self.sp + 4}", self.display, None))
        self.get_program_block()
        self.code_g.program_block.append(code_generator.Three_Address_Code("ASSIGN", f"#0", self.return_val, None))
        self.get_program_block()
        self.code_g.program_block.append(code_generator.Three_Address_Code("ASSIGN", f"#0", self.sp + 4, None))
        # self.dynamic_stack = 1000

    def get_static_address(self, skip=4):
        self.get_program_block()
        self.code_g.program_block.append(code_generator.Three_Address_Code("ASSIGN", "#0", self.static_data, None))
        self.static_data += skip
        return self.static_data - skip

    def get_program_block(self):
        self.code_add += 1
        if self.code_add == 71:
            print("here")
        return self.code_add - 1

    def get_front_code(self):
        return self.code_add
