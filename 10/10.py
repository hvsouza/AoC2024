import numpy as np

import re


        
class PSolver():
    def __init__(self):
        self.trailheads = {}
        self.trailends = {}


    def readinput(self, iname='input10.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ np.array(list(map(int, list(line.strip())))) for line in lines ]

        self.data = lines
    def range_2d(self, m, n):
        for j in range(m):
            for i in range(n):
                yield i, j

    def deepernet(self, motherid, myi, myj):
        myid = (myi,myj)
        myval = self.data[myi][myj]
        if myid in self.connections.keys():
            # print("Adding one")
            self.connections[motherid] += self.connections[myid]
        else:
            # print("Nothing yet")
            if myval == 9 :
                # print("niiine")
                self.connections[myid] = [myid]
            else:
                self.connections[myid] = []
                diff = [-1, +1, -1j, +1j]
                for dx in diff:
                    ni = int(myi + (dx).real)
                    nj = int(myj + (dx).imag)
                    if(ni < 0 or ni >= len(self.data)):
                        continue
                    if(nj < 0 or nj >= len(self.data[0])):
                        continue
                    if self.data[ni][nj] == myval+1:
                        self.deepernet(myid, ni, nj)
            self.connections[motherid] += self.connections[myid]
        # print(motherid, myid, self.connections[motherid], self.connections[myid])

    def create_connections(self, i, j): 
        myid = (i,j)
        myval = self.data[i][j]
        if myid not in self.connections.keys():
            self.connections[myid] = [] #number of solutions

            if myval==0:
                self.trailheads[myid] = 1
            elif myval==9:
                self.trailends[myid] = 1
                self.connections[myid] = [myid]
                return
            diff = [-1, +1, -1j, +1j]
            for dx in diff:
                ni = int(i + (dx).real)
                nj = int(j + (dx).imag)
                if(ni < 0 or ni >= len(self.data)):
                    continue
                if(nj < 0 or nj >= len(self.data[0])):
                    continue
                # print(i, j, myval, ni, nj, self.data[ni][nj],  self.connections[myid])
                if self.data[ni][nj] == myval+1:
                    # print("Enter deep")
                    self.deepernet(myid, ni, nj)

    def create_references(self):
        self.connections={}
        for i, j in self.range_2d(len(self.data), len(self.data[0])):
            self.create_connections(i, j)

    def solve(self):
        self.readinput()
        self.create_references()
        # print(self.connections)
        res1=0
        res2=0

        for i, j in self.trailheads.keys():
            res1+=len(set(self.connections[(i,j)]))
            res2+=len(self.connections[(i,j)])
        print("Solved1:", res1)
        print("Solved2:", res2)



if __name__ == "__main__":
    s = PSolver()
    s.solve()

