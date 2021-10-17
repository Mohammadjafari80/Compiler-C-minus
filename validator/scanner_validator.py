import Scanner
import os


def read_file(path):
    f = open(path, "r")
    b = f.readlines()
    f.close()
    return b


for i in range(10):
    cur_path = os.path.dirname(__file__)
    print(cur_path)
    path = os.path.relpath(f"{os.getcwd()}\\test\\test", cur_path)
    print(path)

    n = f"0{i + 1}" if i >= 9 else f"{i+1}"

    error = read_file(f"{path}\\T{n}\\lexical_errors.txt")
    token = read_file(f"{path}\\T{n}\\tokens.txt")
    symbol = read_file(f"{path}\\T{n}\\symbol_table.txt")