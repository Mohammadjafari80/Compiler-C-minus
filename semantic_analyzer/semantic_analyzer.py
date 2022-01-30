from scope_records import scope_record as sr


class SemanticNode:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f'(val={self.val})'


class SemanticAnalyzer:
    def __init__(self):
        self.semantic_stack = []

    def pop(self):
        return self.semantic_stack.pop()

    def push(self, val):
        self.semantic_stack.append(SemanticNode(val))

    def front(self):
        return self.semantic_stack[len(self.semantic_stack) - 1]
