from scope_records import scope_record as sr


class Memory():
    def __init__(self):
        self.code_add = 0
        self.static_data = 100
        self.dynamic_data = 500

    def get_temp(self):
        self.dynamic_data += 4
        return self.dynamic_data - 4

    def get_static_address(self, ):
        self.static_data += 4
        return self.static_data - 4
