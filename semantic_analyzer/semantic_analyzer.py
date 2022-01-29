from scope_records import scope_record as sr


class SemanticNode:
    def __init__(self, val):
        self.val = val


class SemanticAnalyzer:
    def __init__(self):
        self.semantic_stack = []

    def pop(self):
        self.semantic_stack.pop()

    def push(self, val):
        self.semantic_stack.append(SemanticNode(val))
