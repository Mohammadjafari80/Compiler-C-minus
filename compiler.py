import Scanner
path = "./input.txt"
scanner = Scanner.Scanner(path)
t = scanner.DFA.load_table("dfa.txt")
print(t)
