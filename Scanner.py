class Scanner:
    def __init__(self,path):
        input_file = open(path)
        self.input = input_file.read()
        self.line_number = 1
        self.char_index = 0
        self.input_size = len(self.input)
        while self.char_index < self.input_size :
            print(self.input[self.char_index])
            self.char_index= self.char_index+1
