import numpy as np
import cmath 


def readinput(iname='input6.dat'):
    data = 0
    with open(iname,'r') as f:
        lines = f.readlines()
        lines = [ line.strip() for line in lines ]
        lines = [ list(line) for line in lines ]
        data = lines

    return data


class PSolver():
    def __init__(self):
        self.guardtype = { ">":0, "v":-(np.pi/2), "<":-(np.pi), "^":-(3*np.pi/2) }
        self.insideparadox = False # are we sure? 
        self.tested = {}


    def range_2d(self, data):
        self.m = len(data)
        self.n = len(data[0])
        for i in range(self.m):
            for j in range(self.n):
                yield i, j

    def navigate(self):
        starti = self.guard[0]
        startj = self.guard[1]
        movei = -int(self.guard[2].imag)
        movej = int(self.guard[2].real)

        newi = starti + movei
        newj = startj + movej
        # print(starti, startj, movei, movej)
        self.invalidstep = False
        if newi == self.m or newi == -1:
            self.invalidstep = True
        if newj == self.n or newj == -1:
            self.invalidstep = True

        if self.invalidstep:
            return False
        else:
            next_place = self.data[newi][newj]
            if next_place == '.' or next_place==self.original_pos:
                self.viewer[newi][newj] = "X"
                i = newi
                j = newj
                self.guard[0] = i
                self.guard[1] = j
            else:
                self.theta -= np.pi/2
                # print(self.theta)
                next_direction = cmath.exp( (self.theta)*1j )
                # print(next_direction)
                self.guard[2] = next_direction
            # for v in self.viewer:
            #     print(''.join(v))
            return True


    def navigate_paradox(self, data):
        starti = self.guard[0]
        startj = self.guard[1]
        movei = -int(self.guard[2].imag)
        movej = int(self.guard[2].real)

        newi = starti + movei
        newj = startj + movej
        # print(starti, startj, movei, movej)
        self.invalidstep = False
        if newi == self.m or newi == -1:
            self.invalidstep = True
        if newj == self.n or newj == -1:
            self.invalidstep = True

        if self.invalidstep:
            return False, False
        else:
            next_place = data[newi][newj]
            if next_place == '.' or next_place==self.original_pos:
                if not self.insideparadox:
                    if (newi, newj) not in self.paradoxes:
                        theta = self.theta
                        guardclone = self.guard.copy()
                        self.check_paradox(newi, newj)
                        self.guard = guardclone
                        self.theta = theta
                self.viewer[newi][newj] = "X"
                i = newi
                j = newj
                self.guard[0] = i
                self.guard[1] = j
            else:
                if (newi, newj, movei, movej) not in self.hits_wall:
                    self.hits_wall[ (newi, newj, movei, movej) ] = 1
                else:
                    return False, True #PARADOX :o

                self.theta -= np.pi/2
                # print(self.theta)
                next_direction = cmath.exp( (self.theta)*1j )
                # print(next_direction)
                self.guard[2] = next_direction
            # if not self.insideparadox:
            #     for v in self.viewer:
            #         print(''.join(v))
            #     print("\n")
            return True, False


    def check_paradox(self, i, j):
        
        if (i,j) == (self.oi, self.oj) or (i,j) in self.tested:
            return

        # print("Search paradox")
        self.insideparadox = True
        self.hits_wall = {}
        patrol = True
        data = [ d.copy() for d in self.data ]
        viewer = [ d.copy() for d in self.viewer ]
        data[i][j] = "#"
        self.viewer[i][j] = "O"

        self.theta = self.otheta
        self.guard = self.oguard.copy()

        while (patrol):
            patrol, isparadox = self.navigate_paradox(data)
        
        self.insideparadox = False
        if isparadox:
            # print("PARADOX!!!", i, j)
            self.paradoxes[(i, j)] = 1


        self.viewer = viewer
        self.tested[(i,j)] = 1
        return

        



    def solve1(self):
        self.data = readinput()
        self.viewer = [ d.copy() for d in self.data ]


        for i, j in self.range_2d(self.data):
            if self.data[i][j] in self.guardtype:
                self.theta = self.guardtype[self.data[i][j]]
                direction = cmath.exp( (self.theta)*1j )
                self.guard = [i, j, direction, self.data[i][j]]
                self.viewer[i][j] = "X"
                self.original_pos = self.data[i][j]
                # print(self.theta)
                # print(self.guard)
                # print(self.guardtype)

        patrol = True
        while (patrol):
            patrol = self.navigate()

        res=0
        for v in self.viewer:
            # print(''.join(v))
            for m in v:
                if m == "X":
                    res+=1

        print("Solved1:", res)
                
    def solve2(self):
        self.data = readinput()
        self.viewer = [ d.copy() for d in self.data ]

        self.paradoxes = {}
        self.hits_wall = {}


        for i, j in self.range_2d(self.data):
            if self.data[i][j] in self.guardtype:
                self.theta = self.guardtype[self.data[i][j]]
                direction = cmath.exp( (self.theta)*1j )
                self.guard = [i, j, direction, self.data[i][j]]
                self.viewer[i][j] = "X"
                self.original_pos = self.data[i][j]

                self.otheta = self.theta
                self.odir = direction
                self.oguard = [i, j, direction, self.data[i][j]]
                self.oi = i
                self.oj = j

        patrol = True
        while (patrol):
            patrol, _ = self.navigate_paradox(self.data)

        res=0
        print("Solved2:", len(self.paradoxes))
    

if __name__ == "__main__":
    s = PSolver()
    # s.solve1()
    s.solve2()
