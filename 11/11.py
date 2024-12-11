import numpy as np


class PSolver():

    def __init__(self):
        self.database = {}


    def readinput(self, iname='input11.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip().split(" ") for line in lines]
            
            if len(lines) > 1:
                raise Exception("Nope..")
        self.data = [ int(line) for line in lines[0] ]




    def blink(self, stones, nblinks):
        prodstones = 0
        refstone = stones

        if (stones, nblinks) in self.database:
            return self.database[(stones, nblinks)]
        if nblinks == 0:
            return 0 # no production
        else:
            if stones == 0:
                stones+=1
                prodstones+=self.blink(stones, nblinks-1)
            elif len(stones_str:=str(stones))%2==0:
                stone_left = stones_str[:len(stones_str)//2]
                stone_right = stones_str[len(stones_str)//2:]
                nleft = self.blink(int(stone_left), nblinks-1)
                nright = self.blink(int(stone_right), nblinks-1)
                if nleft==0:
                    nleft = 1
                if nright==0:
                    nright = 1
                prodstones += nleft + nright
            else:
                stones*=2024
                prodstones+=self.blink(stones, nblinks-1)
            self.database[(refstone, nblinks)] = prodstones
            return prodstones


    def solve(self ):
        self.readinput()
        nblinks = 75
        for i, stones in enumerate(self.data):
            self.blink(stones, nblinks=nblinks)
        for i, stones in enumerate(self.data):
            self.blink(stones, nblinks=25)

        # print(self.database)
        res1=0
        res2=0
        for stones in self.data:
            res1+=self.database[(stones, 25)]
            res2+=self.database[(stones, nblinks)]

        print("Solved1:", res1)
        print("Solved2:", res2)
            


if __name__ == "__main__":

    s = PSolver()
    s.solve()

