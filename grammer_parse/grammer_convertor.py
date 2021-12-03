import json

# Serialize data into file:


grammer = {};
def make_grammer(g):
    g = g.split(" ")
def analysis(line):
    if (len(line) == 0):
        return
    line = line.strip()
    line = line.replace("EPSILON","null")
    g = line.split("->")
    left = g[0].replace(" ", "")
    right = g[1].split("|")
    right_g = []
    for word in right:
        w = word.split()
        right_g.append(w)
    grammer[left] = right_g

with open('G.txt') as f:
    line = f.readline()
    analysis(line)
    while line:
        line = f.readline()
        analysis(line)
json.dump( grammer, open( "grammer.json", 'w' ) )

# Read data from file:
data = json.load( open( "grammer.json" ) )
print(data)