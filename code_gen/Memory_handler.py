from scope_records import scope_record as sr


class Memory():
    def __init__(self):
        self.code_add = 0
        self.sp = 3008
        self.display = 3004
        self.static_data = 100
        self.dynamic_data = 500
        self.return_val = 3000
        # self.dynamic_stack = 1000

    def get_temp(self):
        self.dynamic_data += 4
        return self.dynamic_data - 4

    def get_static_address(self, skip=4):
        self.static_data += skip
        return self.static_data - skip

    def get_program_block(self):
        self.code_add += 1
        return self.code_add - 1

    def get_front_code(self):
        return self.code_add

    def increase_stack_p(self):
        self.sp += 4
        return self.sp - 4
