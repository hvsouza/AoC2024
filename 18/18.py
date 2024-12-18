import numpy as np

class PSolver():
    def __init__(self):
        self.m = 71
        self.n = 71
        self.maze = [ ["."]*self.n for _ in range(self.m) ]

    def readinput(self, iname='input18.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ list(map(int, (line.strip()).split(","))) for line in lines ]
        self.dbytes = lines

    def reach_end(self):
        checked = { self.start: 0 }
        history = { self.start: () }
        tocheck = [self.start]
        moves = [ 1, -1, 1j, -1j ]
        while (tocheck):
            thecheck = tocheck.pop(0)
            for diff in moves:
                i = thecheck[0] + int(diff.real)
                j = thecheck[1] + int(diff.imag)
                if i<0 or i>=self.m or j<0 or j>=self.n or self.maze[i][j]=="#":
                    continue
                if (i,j) not in checked:
                    tocheck.append((i,j))
                    checked[(i,j)] = checked[thecheck] + 1
                    history[(i,j)] =  thecheck 
                elif checked[thecheck]+1 < checked[(i,j)]:
                    checked[(i,j)] = checked[thecheck] + 1
                    history[(i,j)] = thecheck
        return checked, history

    def solve1(self):
        self.readinput()

        for db in self.dbytes[:1024]:
            self.maze[db[1]][db[0]] = "#"

        self.start = (0,0)
        self.target = (self.m-1, self.n-1)

        checked, history = self.reach_end()
        previous = history[self.target]
        while True:
            self.maze[previous[0]][previous[1]] = "O"
            if previous == self.start:
                break
            previous = history[previous]
        # for line in self.maze:
        #     print(''.join(line))
        print(checked[self.target])

    def solve2(self):
        self.readinput()

        for db in self.dbytes:
            self.maze[db[1]][db[0]] = "#"

        self.start = (self.m-1,self.n-1)
        self.target = (0,0)

        aux = 1
        while True:
            checked, history = self.reach_end()
            if self.target in checked:
                break
            db = self.dbytes[-aux]
            self.maze[db[1]][db[0]] = "."
            aux+=1

        print(self.dbytes[-aux+1])


if __name__ == "__main__":
    s = PSolver()
    s.solve1()
    s.solve2()
