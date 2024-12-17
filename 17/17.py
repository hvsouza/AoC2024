import numpy as np
import re
import sys
from tqdm import tqdm


class WTF():
    def __init__(self):
        pass

    def readinput(self, iname="input17.dat"):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
        separator = lines.index('')
        self.registers = {}
        self.map_interger_register = {"A":4, "B":5, "C":6}
        p = re.compile(r'Register (.): (\d+)')
        for line in lines[:separator]:
            m = p.match(line)
            self.registers[self.map_interger_register[ m.group(1) ]] = int(m.group(2))
        pp = re.compile(r'Program: (.*)')
        lineprogram = lines[separator+1:][0]
        m = pp.match(lineprogram)
        self.programs = list(map(int,m.group(1).split(",")))
        self.output = []

        self.map_exec = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
    
    def getcombo(self, literal):
        if literal > 6:
            raise Exception("Wtf..")
        if literal in self.registers:
            literal = self.registers[literal]
        return literal
    def adv(self, literal, reout=4):
        literal = self.getcombo(literal)
        denominator = 2**literal
        self.registers[reout]  = int(self.registers[4]/denominator)
    def bxl(self, literal):
        self.registers[5] = self.registers[5] ^ literal

    def bst(self, literal):
        literal = self.getcombo(literal)
        self.registers[5] = literal%8

    def jnz(self, literal):
        if self.registers[4]<1:
            return
        else:
            self.intruction_pointer=literal
            self.no_jump=False
    def bxc(self, literal):
        self.registers[5] = self.registers[5] ^ self.registers[6]

    def out(self, literal):
        literal = self.getcombo(literal)
        self.output.append( literal%8 )

    def bdv(self, literal):
        self.adv(literal, 5)

    def cdv(self, literal):
        self.adv(literal, 6)
        

    def execute_programs(self):
        self.intruction_pointer = 0
        while(True):
            self.no_jump = True
            try:
                command = self.programs[self.intruction_pointer]
                literal = self.programs[self.intruction_pointer+1]
            except Exception as error:
                # print(error)
                # print("End of the line...")
                return
            # print(command, literal, self.registers, self.output)
            self.map_exec[command](literal)
            if self.no_jump:
                self.intruction_pointer += 2

    def solve1(self):
        self.execute_programs()
        print(','.join(map(str,self.output))) #fuck this shit..

        self.output = []
    def solve2(self):
        champions = [4] # the only one that starts with 0...
        while True:
            thechampion = champions.pop(0)
            ndigits = len(str(thechampion)) 
            #multiples of 8 repeat exactly same output.. the end limits the number of digits.. but relies on break
            for x in range(thechampion*8,40*(8**(ndigits))): 
                self.output = []
                self.registers[4] = x
                self.registers[5] = 0
                self.registers[6] = 0
                self.execute_programs()
                if x in champions: #noticed champions are super close... 
                    champions.remove(x)
                if self.output[-ndigits:] != self.programs[-ndigits:]:
                    break # they stop being equal.. enough
                if len(self.output) > ndigits and self.output[-(ndigits+1):] == self.programs[-(ndigits+1):]:
                    champions.append(x)
                if self.output == self.programs:
                    print(x)
                    return


if __name__ == "__main__":
    s = WTF()
    s.readinput()
    if len(sys.argv)>1:
        s.registers[4] = int(sys.argv[1])
    s.solve1()
    s.solve2()
