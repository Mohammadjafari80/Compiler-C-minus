class Break:
    def __init__(self):
        self.q = []

    def add_repeat(self):
        self.q.append([])

    def add_break(self, add):
        self.q[len(self.q) - 1].append(add)

    def get_breaks_address(self):
        return self.q.pop()
