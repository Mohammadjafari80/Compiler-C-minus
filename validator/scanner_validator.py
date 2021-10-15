import Scanner
import os
print(os.getcwd())
def read_file(path):
    f = open(path,"r")
    b = f.readlines()
    f.close()
    return b
for i in range(10):
    path ="Documents/term5/compiler/project/quera/PA1/PA1_testcases1.2"
    n = "0"+ str(i+1)
    if i < 9:
        n = str((i+1))
    npath =  path+"/"+"T"+str(n)+"/"
    error = read_file(path+"/lexical_errors.txt")
    token = read_file(path+"/tokens.txt")
    symbol = read_file(path+"/symbol_table.txt")


