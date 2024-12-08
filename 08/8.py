import numpy as np
import re


class PSolver():
    def __init__(self):
        self.iname='input8.dat'


    def readinput(self):
        with open(self.iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
            lines = [ list(line) for line in lines ]


        self.data = lines
        
    def print_map(self, data):
        for d in data:
            print(''.join(d))
        print('\n')


    def fill_antinodes(self, ref, others, resonance=False):
        # print(ref)
        i, j = ref
        for io, jo in others:
            icheck = -(io - i)
            jcheck = -(jo - j)

            ianti = i + icheck
            janti = j + jcheck
            unforseen_consequences=True
            while(unforseen_consequences):
                if not resonance:
                    unforseen_consequences=False
                if ianti >= 0 and ianti < len(self.data) and janti >= 0 and janti < len(self.data[0]):
                    self.antinodes[ianti][janti]="#"
                    ianti += icheck
                    janti += jcheck
                else:
                    unforseen_consequences=False



    def solve1(self):
        self.readinput()
        self.antinodes = [ d.copy() for d in self.data ]
        # self.print_map(self.antinodes)
        self.uniq_chars = {}
        for i, d in enumerate(self.data):
            for j, c in enumerate(d):
                if c!= '.':
                    if c not in self.uniq_chars:
                        self.uniq_chars[c]=[(i,j)]
                    else:
                        self.uniq_chars[c]+=[(i,j)]

        for antenas, positions in self.uniq_chars.items():
            # print(antenas, positions)
            for ip, position_ref in enumerate(positions):
                otherpositions = positions.copy()
                _ = otherpositions.pop(ip)
                self.fill_antinodes(position_ref, otherpositions)
        
        # self.print_map(self.antinodes)
        res = 0
        for d in self.antinodes:
            for c in d:
                if c == "#":
                    res+=1

        print("Solved1:", res)

    def solve2(self):
        for antenas, positions in self.uniq_chars.items():
            # print(antenas, positions)
            for ip, position_ref in enumerate(positions):
                if len(positions)>1:
                    self.antinodes[position_ref[0]][position_ref[1]]="#"

                otherpositions = positions.copy()
                _ = otherpositions.pop(ip)
                self.fill_antinodes(position_ref, otherpositions, resonance=True)

        res = 0
        for d in self.antinodes:
            for c in d:
                if c == "#":
                    res+=1

        # self.print_map(self.antinodes)
        print("Solved2:", res)

if __name__ == "__main__":
    s = PSolver()
    s.solve1()
    s.solve2()



