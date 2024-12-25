import numpy as np

class PSolver():

    def readinput(self, iname='input24.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = np.char.array([ line.strip() for line in lines ])

        separators = np.argwhere(lines=='')
        previous = None
        self.keys = []
        self.locks = []
        for s in separators:
            tmpline = np.array([ list(line) for line in lines[previous:s[0]] ])
            if tmpline[0][0]=="#":
                thetype = self.keys
            else:
                thetype = self.locks
            values = np.zeros_like(tmpline[0], dtype=np.int16)
            for column in range(len(tmpline[0])):
                kcolumn = tmpline[1:-1,column]
                values[column] = np.sum(kcolumn=="#")
            thetype.append(values)
            previous = s[0]+1

    def solve1(self):
        self.readinput()
        self.pairs = {}
        for i, key in enumerate(self.keys):
            for j, lock in enumerate(self.locks):
                if np.all(key+lock<=5):
                    self.pairs[(i,j)] = self.pairs.get((i,j),0) + 1

        print("Solved1:", len(self.pairs))

s = PSolver()
s.solve1()
