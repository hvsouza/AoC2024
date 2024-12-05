import numpy as np
import re

class PSolver():
    def __init__(self):
        self.sol1 = 0

    def readinput(self, iname='input4.dat'):
        with open(iname,'r') as f:
            lines = f.readlines()
            lines = np.array([ line.strip() for line in lines ])
        self.data_normal = lines 
        self.data_backwards = np.array( [ line[::-1] for line in lines ])

        databroke = np.array( np.array([list(line) for line in lines ]) )


        databroke_back = np.array([ line[::-1]  for line in databroke.transpose() ])

        self.data_hor = np.array( [''.join(line) for line in databroke.transpose() ]) 
        self.data_hor_back = np.array( [line[::-1] for line in self.data_hor] )

        self.data_diagonal = []
        self.data_invdiagonal = []
        r0 = np.arange(len(databroke[0])) # Or r0,r1 = np.ogrid[:m,:n], out[:,:,0] = r0
        r1 = np.arange(len(databroke))

        self.indexes = np.empty((len(databroke[0]), len(databroke), 2), dtype=int)
        self.indexes[:,:,0] = r0[:,None]
        self.indexes[:,:,1] = r1
        # for i in range(len(databroke)):
        #     for j in range(len(databroke[i])):
        #         self.indexes[i][j] = {i:j}


    
        self.idx_diagonal = []
        self.idx_invdiagonal = []
        for dk in np.arange(-(len(databroke)-1), len(databroke), 1):
            self.data_diagonal.append( ''.join(databroke.diagonal(dk)) )
            self.idx_diagonal.append(self.indexes.diagonal(dk).T)
            self.data_invdiagonal.append( ''.join((databroke[::-1]).diagonal(dk)) )
            self.idx_invdiagonal.append(self.indexes[::-1].diagonal(dk).T)


        self.data_diagonal_back = [ line[::-1] for line in self.data_diagonal ]
        self.data_invdiagonal_back = [ line[::-1] for line in self.data_invdiagonal ]
        
        self.everything = [ self.data_normal, self.data_backwards, self.data_hor, self.data_hor_back, self.data_diagonal, self.data_diagonal_back, self.data_invdiagonal, self.data_invdiagonal_back]



    
    def solve1(self):
        prog = re.compile(r"X\+?M\+?A\+?S")
        for i, data in enumerate(self.everything):
            # print(i)
            for string in data:
                m = prog.findall(string)
                # print(m, string)
                self.sol1+=len(m)

    
    def solve2(self):
        self.sol2 = 0
        self.diagonals = [self.data_diagonal, self.data_diagonal_back, self.data_invdiagonal, self.data_invdiagonal_back]

        self.matches_digonal = []
        self.matches_invdiagonal = []

        prog = re.compile(r"MAS")
        # print(self.idx_invdiagonal[7])
        for iref, data in enumerate(self.diagonals):
            # print(iref)
            for i, string in enumerate(data):
                m = prog.finditer(string)
                # if all(False for _ in m):
                #     print(string)
                m = prog.finditer(string)
                for match in m:
                    row = i
                    column = match.start()+1 # position of A
                    if iref<=1: # diagonal
                        if iref==1: # diagonal back
                            column = (len(string)-1)-(match.start()+1) # position of A
                        self.matches_digonal.append(list(self.idx_diagonal[row][column]))
                    else:
                        if iref==3: # diagonal back
                            column = (len(string)-1)-(match.start()+1) # position of A

                        self.matches_invdiagonal.append(list(self.idx_invdiagonal[row][column]))
                        # print(string, match.group(), row, column, self.idx_invdiagonal[row][column])

        # print(self.matches_digonal)
        # print(self.matches_invdiagonal)

        for n in self.matches_digonal:
            if n in self.matches_invdiagonal:
                self.sol2+=1



if __name__ == "__main__":
    
    s = PSolver()
    s.readinput()
    s.solve1()
    print("Solved1:", s.sol1)
    s.solve2()
    print("Solved2:", s.sol2)
