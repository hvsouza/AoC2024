import numpy as np


class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input22.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ int(line.strip()) for line in lines ]

        self.data = np.array(lines, dtype=np.int32)

    def step1(self, values):
        values = values^(values*64)
        values = values%16777216
        return values
    def step2(self, values):
        values = values^(values//32)
        values = values%16777216
        return values
    def step3(self, values):
        values = values^(values*2048)
        values = values%16777216
        return values

    def process_sequence(self, values):
        values = self.step1(values)
        values = self.step2(values)
        values = self.step3(values)
        return values



    def solve1(self):
        self.readinput()
        for i in range(2000):
            self.data = self.process_sequence(self.data)
        print("Solved1:", self.data.sum())

    def solve2(self):
        self.readinput()
        ntimes:int=2000
        self.diff = np.zeros(shape=(len(self.data),ntimes))
        self.last = np.zeros(shape=(len(self.data),ntimes))
        for i in range(ntimes):
            originaldata = np.array([ int(repr(value)[-1]) for value in self.data])
            self.data = self.process_sequence(self.data)
            afterdata = np.array([ int(repr(value)[-1]) for value in self.data])
            self.diff[:,i] = afterdata-originaldata
            self.last[:,i] = afterdata

        argentinian_history = {}
        for ds, ld in zip(self.diff, self.last):
            this_argentinian = {}
            for x in range(len(ds)-4):
                thesequence = tuple(ds[x:x+4])
                thevalue = ld[x+3]
                if thesequence not in this_argentinian:
                    this_argentinian[thesequence] = thevalue
            for k, v in this_argentinian.items():
                if k not in argentinian_history:
                    argentinian_history[k] = v
                else:
                    argentinian_history[k] += v

        theultimatesequence = max(argentinian_history, key=argentinian_history.get)
        print("Solved2:", argentinian_history[theultimatesequence])


if __name__ == "__main__":
    s = PSolver()
    # s.solve1()
    s.solve2()

