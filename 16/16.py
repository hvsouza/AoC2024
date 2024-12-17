import numpy as np 
import copy
import cmath
import sys

class Rat():
    def __init__(self):
        self.reached = {}
        self.points = 0
        self.direction = 0
        self.lastturn = 0
        self.foundEnd = False

    def __lt__(self, other):
        return self.points < other.points

    def __le__(self, other):
        return self.points <= other.points

    def __repr__(self):
        out = f"points: {self.points}, end = {self.foundEnd}\n"
        for k, v in self.reached.items():
            out+=f"{k}:{v[0]}\n"
        return out
class PSolver():
    def __init__(self):
        self.diff = [ 0, -np.pi/2, +np.pi/2 ]
        self.checkpoint = {}
        self.finish_rats = []
        self.minscore = 1e12
        self.from_here_get_to_end = {}
        self.second=False

    def readinput(self, iname='input16.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ list(line.strip()) for line in lines ]
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == "S":
                    self.start = (i,j)
                if c == "E":
                    self.end = (i,j)
        self.maze = lines

    def checkbondaries(self, i, j):
        if self.maze[i][j] == "#":
            return False, False #No need to check this
        if self.maze[i][j] == "E":
            return True, True
        if self.maze[i][j] == ".":
            return True, False

        return False, False

    def searchEnd(self, i, j, rat):
        
        isalive=True
        next_rats = []

        while(isalive):
            isalive=False
            create_new_rat = False
            originalrat = copy.deepcopy(rat)
            for diff in self.diff:
                newdirection = originalrat.direction + diff
                imagdirec = cmath.exp(newdirection*1j)
                newi = i - int(imagdirec.imag)
                newj = j + int(imagdirec.real)
                extrapoint = 0
                valid, isend = self.checkbondaries(newi,newj)
                # print(valid, newi, newj)
                if not valid:
                    continue

                extrapoint = 1 if diff == 0 else 1001
                currentpoints = originalrat.points + extrapoint
                if currentpoints > self.minscore:
                    continue

                directind = int(imagdirec.real) + int(imagdirec.imag)*1j
                if (newi,newj,directind) in originalrat.reached:
                    continue

                identifier = (newi,newj, directind)

                if identifier in self.checkpoint:
                    if currentpoints < self.checkpoint[identifier]: # no reason to continue
                        self.checkpoint[identifier] = currentpoints
                    elif currentpoints == self.checkpoint[identifier]:
                        if self.second:
                            if identifier+(currentpoints, ) in self.from_here_get_to_end:
                                isend=True
                                currentpoints = self.from_here_get_to_end[identifier+(currentpoints,)]
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue

                else:
                    self.checkpoint[identifier] = currentpoints


                if isend:
                    originalrat.foundEnd = True
                    originalrat.points = currentpoints
                    self.finish_rats.append(originalrat)
                    if currentpoints < self.minscore:
                        self.minscore = currentpoints
                    if self.second:
                        for (_i, _j, _dir), tmp in originalrat.reached.items():
                            _pt = tmp
                            self.from_here_get_to_end[(_i,_j,_dir,_pt)] = currentpoints
                            # print(self.from_here_get_to_end)
                    continue
                if create_new_rat:
                    # print("Creating...")
                    newrat = copy.deepcopy(originalrat)
                    newrat.direction = newdirection
                    newrat.points = currentpoints
                    newrat.reached[(newi,newj,directind)] = newrat.points

                    newrat.lastturn = diff
                    next_rats.append([ newi, newj, newrat ]) 
                else:
                    isalive=True
                    create_new_rat=True
                    rat.direction = newdirection
                    rat.points = currentpoints
                    rat.reached[(newi,newj,directind)] = rat.points
                    rat.lastturn = diff
                    refi = newi
                    refj = newj
            if isalive:
                i = refi
                j = refj

        # print("Dead..", len(next_rats), len(self.checkpoint), self.minscore)
        for i, j, nrat in next_rats[::-1]:
            self.searchEnd(i, j, nrat)

            

    def solve(self):
        self.readinput()
        rat = Rat()
        i, j = self.start
        rat.reached[(i,j,0)] = 0
        rat.direction = 0
        rat.lastturn = 0
        self.searchEnd(i, j, rat)
        minrat = min(self.finish_rats)
        # print(minrat)
        # for i, line in enumerate(self.maze):
        #     for j, c in enumerate(line):
        #         if (i,j) in minrat.reached:
        #             self.maze[i][j] = "@" 

        # for line in self.maze:
        #     print(''.join(line))

        print("Solved1:", minrat.points)




        self.second = True
        self.readinput()
        rat = Rat()
        i, j = self.start
        rat.reached[(i,j,0)] = 0
        rat.direction = 0
        rat.lastturn = 0
        self.checkpoint = {}
        self.finish_rats = []
        self.searchEnd(i, j, rat)
        self.bestspots = {}
        for rat in self.finish_rats:
            if rat.points == minrat.points:
                for i, line in enumerate(self.maze):
                    for j, c in enumerate(line):
                        tmpreached = {(i, j):1 for (i,j,_) in rat.reached.keys()}
                        if (i,j) in tmpreached.keys():
                            self.bestspots[(i,j)] = 1
        print("Solved2:", len(self.bestspots)+1)


if __name__ == "__main__":
    # sys.setrecursionlimit(2000)
    s = PSolver()
    s.solve()
