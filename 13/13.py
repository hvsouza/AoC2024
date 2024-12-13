import numpy as np
import re
from tqdm import tqdm

class Machine():
    def __init__(self, A, B, prize):
        self.A     = A
        self.B     = B
        self.prize = prize
    def __repr__(self):
        return f"A: {self.A}, B:{self.B}, prize {self.prize}"


class PSolver():
    def __init__(self):
        self.costmoveA = 3
        self.costmoveB = 1

    def readinput(self, iname="input13.dat"):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines if line.strip()]

        machine_infos = 3
        self.nmachines=int(len(lines)/machine_infos)
        themachines = [None]*self.nmachines

        rebutton = re.compile(r"Button .: X\+(\d+), Y\+(\d+)")
        reprize = re.compile(r"Prize: X=(\d+), Y=(\d+)")
        recommands = [rebutton, rebutton, reprize]
        for nm in range(self.nmachines):
            _vars = [[0,0], [0,0], [0,0]]
            for i, iline in enumerate(range(nm*machine_infos, nm*machine_infos+machine_infos)):
                p = recommands[i]
                m = p.match(lines[iline])
                _vars[i][0] = int(m.group(1))
                _vars[i][1] = int(m.group(2))
            themachines[nm] = Machine(_vars[0], _vars[1], _vars[2])
            
        self.themachines = themachines

    def getroundsolutions(self, moveA, moveB, othermoveA, othermoveB, theprize, theotherprize, sol):
        solA = round(sol[0])
        solB = round(sol[1])
        if (solA*(moveA)+solB*(moveB) == (theprize)) and (solA*(othermoveA)+solB*(othermoveB) == (theotherprize)):
            return solA, solB
        return [0, 0]


    def get_moves(self, second=False):
        idx = 0
        theprize = self.machine.prize[idx]
        theotherprize = self.machine.prize[idx+1]
        moveA = self.machine.A[idx]
        moveB = self.machine.B[idx]
        othermoveA = self.machine.A[idx+1]
        othermoveB = self.machine.B[idx+1]

        if second:
            theprize += 10**13
            theotherprize += 10**13

        thematrix = np.array(
            [ [moveA, moveB],
              [othermoveA, othermoveB] ],
        )

        try:
            thematrixinv = np.linalg.inv( thematrix )
            sol = thematrixinv.dot(np.array( [ theprize, theotherprize ], dtype=np.float64 ))
        except:
            raise Exception("No solution...")
        solA, solB = self.getroundsolutions(moveA, moveB, othermoveA, othermoveB, theprize, theotherprize, sol)

        if not second: # actually never happen...
            if solA > 100 or solB>100:
                return [0, 0]
        return solA, solB


    def get_prize(self, machine):
        self.machine = machine
        self.machinemoves_part1 = self.get_moves()
        self.machinemoves_part2 = self.get_moves(True)

    def solve(self):
        self.readinput()
        res1 = 0
        res2 = 0
        for machine in self.themachines:
            self.get_prize(machine)
            moves1 = self.machinemoves_part1
            moves2 = self.machinemoves_part2
            res1+= self.costmoveA*moves1[0] + self.costmoveB*moves1[1]
            res2+= self.costmoveA*moves2[0] + self.costmoveB*moves2[1]
        print("Solved1:", res1)
        print("Solved2:", res2)



if __name__ == "__main__":
    s = PSolver()
    s.solve()
