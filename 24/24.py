import numpy as np
import re
import itertools
from tqdm import tqdm



class PSolver():
    def __init__(self):
        self.operation = {
            "OR": np.bitwise_or,
            "XOR": np.bitwise_xor,
            "AND": np.bitwise_and,
        }

    def readinput(self, iname='input24.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
        separator = lines.index('')
        wires = lines[:separator]
        self.wires = {}
        pwire = re.compile(r"([^:]*): (\d)")

        for wire in wires:
            m = pwire.match(wire)
            self.wires[m.group(1)] = int(m.group(2))

        self.toprocess = []
        connections = lines[separator+1:]
        pcon = re.compile(r"(...) ([^\ ]+) (...) -> (...)")
        for c in connections:
            m = pcon.match(c)
            self.toprocess.append(m.groups())

    def solve1(self):
        self.readinput()
        stack = self.toprocess.copy()
        self.wires_input = {}
        self.proper_order = []
        while (stack):
            p = stack.pop(0)
            wire1   = p[0]
            cmd     = p[1]
            wire2   = p[2]
            wireout = p[3]
            if wire1 not in self.wires or wire2 not in self.wires:
                stack.append(p) # back to the 
            else:
                self.wires[wireout] = self.operation[cmd](self.wires[wire1],self.wires[wire2])
                self.wires_input[wireout] = p
                self.proper_order.append(p)

        wiresz = { w: v for w, v in self.wires.items() if w[0] == "z"}
        wiresz = dict(sorted(wiresz.items()))
        binarynumber=""
        for v in reversed(wiresz.values()):
            binarynumber+=str(v)
        print("Solved1", int(binarynumber,2))
        self.totalbits = len(wiresz)


    """
    The sum is:
    z = (x ^ y) ^ carrot
    carrot = (x & y) | carrot
    so I expect: 
    (x0 ^ y0) ^ 0-> z0
    (x0 & y0) -> somecarrot
    (x1 ^ y1) -> tmp
    (x1 & y1) -> next_carrot
    tmp ^ somecarrot -> z1 
    tmp & somecarrot -> carrot2
    next_carrot | carrot2 -> somecarrot
    ... `somecarrot` has to be correct.
    ...
    """
    def solve2(self):

        self.wrong = []
        self.toprocess = [ list(p) for p in self.toprocess ]
        self.mistake=True
        while self.mistake:
            self.mistake=False
            somecarrot = None 
            for i in range(self.totalbits):
                find2 = 0
                for p in self.toprocess:
                    if p[0] == f"x{i:02d}" or p[2] == f"x{i:02d}":
                        # matched.. now break in two..
                        if p[1] == "XOR":
                            if i != 0:
                                tmp = p[3]
                            find2 += 1
                        elif p[1] == "AND":
                            next_carrot = p[3]
                            find2 += 1
                        if find2==2:
                            break
                if i > 0:
                    self.check_addition(tmp, somecarrot, i)
                    if self.mistake: break #start over...
                    carrot2 = self.get_carrot2(tmp, somecarrot)
                    tmpcarrot = self.check_somecarrot(next_carrot, carrot2)
                    if self.mistake: break #start over...
                    somecarrot = tmpcarrot
                    if somecarrot[0] == "z": #done
                        break
                else:
                    somecarrot = next_carrot #this one is ok ... 
        print("Solved2:", ','.join(sorted(set(self.wrong))))

    def check_somecarrot(self, next_carrot, carrot2):
        for p in self.toprocess:
            idxnext = None
            if p[0] == carrot2:
                idxnext = 2
            elif p[2] == carrot2:
                idxnext = 0
            if idxnext is not None:
                if p[1] == "OR":
                    if p[idxnext] == next_carrot:
                        pass
                    else:
                        self.wrong.append(next_carrot)
                        self.wrong.append(p[idxnext])
                        self.adjust_output(next_carrot, p[idxnext])
                    return p[3]
        raise Exception("Wtf...")

    def adjust_output(self, current, replace):
        self.mistake = True

        for i, p in enumerate(self.toprocess):
            if p[3] == current:
                ic = i
            if p[3] == replace:
                ir = i
        self.toprocess[ic][3] = replace
        self.toprocess[ir][3] = current
    def check_addition(self, tmp, carrot, i):
        # assuming carrot is correct
        for p in self.toprocess:
            idxtmp = None
            if p[0] == carrot:
                idxtmp = 2
            elif p[2] == carrot:
                idxtmp = 0
            if idxtmp is not None:
                if p[1] == "XOR": # This too
                    if p[idxtmp] == tmp:
                        if p[3] != f"z{i:02d}":
                            self.wrong.append(p[3])
                            self.wrong.append(f"z{i:02d}")
                            self.adjust_output(p[3], f"z{i:02d}")
                        return 
                    else:
                        if p[3] != f"z{i:02d}":
                            raise Exception("Should this happen?")
                        self.wrong.append(tmp)
                        self.wrong.append(p[idxtmp])
                        self.adjust_output(tmp, p[idxtmp])
                        return 

    def get_carrot2(self, tmp, carrot):
        # assuming carrot is correct
        for p in self.toprocess:
            idxtmp = None
            if p[0] == carrot:
                idxtmp = 2
            elif p[2] == carrot:
                idxtmp = 0
            if idxtmp is not None:
                if p[1] == "AND": # This too
                    if p[idxtmp] == tmp:
                        return p[3]
                    else:
                        raise Exception("Nope...")

        raise Exception("Nope2...")

s = PSolver()
s.solve1()
s.solve2()



