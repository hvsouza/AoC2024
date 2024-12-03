import numpy as np
import re

def readinput(iname):

    data = 0
    with open(iname,'r') as f:
        lines = f.readlines()
        data = lines[0]
        if len(lines)>1:
            for line in lines[1:]:
                data = data + line

    return data
        

def solve1():
    data = readinput("input3.dat")
    m = re.findall(r'mul\(\d+,\d+\)', data)
    res=0
    for mul in m:
        mn = re.search(r'mul\((\d+),(\d+)\)', mul)
        val1 = int(mn.group(1))
        val2 = int(mn.group(2))
        res+=val1*val2


    print("Solved1:", res)

def solve2():
    data = readinput("input3.dat")
    res=0
    do = re.split(r'do\(\)', data)
    for to_do in do:
        donot = re.split(r'don\'t\(\)', to_do)
        m = re.findall(r'mul\(\d+,\d+\)', donot[0])
        for mul in m:
            mn = re.search(r'mul\((\d+),(\d+)\)', mul)
            val1 = int(mn.group(1))
            val2 = int(mn.group(2))
            res+=val1*val2


    print("Solved2:", res)
if __name__ == "__main__":

    solve1()
    solve2()
