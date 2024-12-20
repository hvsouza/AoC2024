import numpy as np
class PSolver():
    def __init__(self):
        pass


    def readinput(self, iname='input20.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = np.char.array([ list(line.strip()) for line in lines ])

        self.maze = lines
        self.start = np.argwhere(self.maze == "S")[0]
        self.end = np.argwhere(self.maze == "E")[0]

    def get_neighbous(self, pos, cheat=1):
        position = pos[0]
        direction = pos[1]
        return [ 
            (position + cheat*direction, direction),
            (position + cheat*direction*1j, direction*1j),
            (position - cheat*direction*1j, -direction*1j), 
        ]

    def findtrack(self):
        navigate = True 
        i, j = self.start
        for x in range(4):
            tmppos = (i+1j*j) + 1j*1j**x
            if self.maze[int(tmppos.real)][int(tmppos.imag)] != "#":
                sdir = 1j*1j**x
                break
        champ = (i + j*1j, sdir)
        self.track = {}
        self.secondsatpoint = {}
        self.track[champ] = 0
        self.secondsatpoint[(i,j)] = 0
        seconds = 1
        race = True
        
        while (race):
            race=False
            for neighbour in self.get_neighbous(champ):
                i, j = int(neighbour[0].real), int(neighbour[0].imag)
                if self.maze[i][j] == "#":
                    continue
                else:
                    self.track[neighbour] = seconds
                    self.secondsatpoint[(i, j)] = seconds
                    champ = neighbour
                    if self.maze[i][j] != "E":
                        race= True
                    # break
            seconds += 1
    
    def cheatmode(self):
        nfinishes = 0
        for pos, seconds in self.track.items():
            for neighbour in self.get_neighbous(pos, 2):
                i, j = int(neighbour[0].real), int(neighbour[0].imag)
                if i < 0 or i >= len(self.maze) or j < 0 or j >= len(self.maze[0]):
                    continue
                if (i, j) in self.secondsatpoint:
                    seconds_saved = self.secondsatpoint[(i,j)] - (seconds + 2)
                    if (seconds_saved>0) and seconds_saved >= 100:
                        nfinishes+=1
        print("Solved1:", nfinishes)

    def supercheatmode(self):
        nfinishes = 0
        others_clean = self.secondsatpoint.copy()
        for pos, seconds in self.secondsatpoint.items():
            myi, myj = pos
            others = others_clean.copy()
            for otherpos, otherseconds in others.items():
                i, j = otherpos
                if abs(i - myi) + abs(j - myj) <= 20:
                    duration_cheat = abs(i - myi) + abs(j - myj)
                    seconds_saved = self.secondsatpoint[(i,j)] - (seconds + duration_cheat)
                    if (seconds_saved>0) and seconds_saved >= 100:
                        nfinishes+=1
            others_clean.pop((myi,myj))
        print("Solved2:", nfinishes)



            
    def solve1(self):
        self.readinput()
        self.findtrack()
        self.cheatmode()

    def solve2(self):
        self.readinput()
        self.findtrack()
        self.supercheatmode()

s = PSolver()
s.solve1()
s.solve2()
