from scope_records import scope_record as sr


class SemanticNode:
    def __init__(self, type=sr.Type.VOID, address=0, lexeme=""):
        self.type = type
        self.address = address
        self.lexeme = lexeme


class SemanticAnalyzer:
    def __init__(self):
        self.semantic_stack = []

    def pop(self):
        self.semantic_stack.pop()

    def push(self, type=sr.Type.VOID, address=0, lexeme=""):
        self.semantic_stack.append(SemanticNode(type, address, lexeme))
