import Scanner
import os
def read_file(path):
    f = open(path,"r")
    b = f.readlines()
    f.close()
    return b
for i in range(10):
    cur_path = os.path.dirname(__file__)
    print(cur_path)
    path = os.path.relpath(str(os.getcwd())+"\\test\\test", cur_path)
    print(path)
    n = "0"+ str(i+1)
    if i > 8:
        n = str((i+1))
    npath =  path+"\\"+"T"+str(n)+"\\"
    error = read_file(npath+"lexical_errors.txt")
    token = read_file(npath+"tokens.txt")
    symbol = read_file(npath+"symbol_table.txt")


