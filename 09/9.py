import numpy as np
import re


class PSolver():

    def __init__(self):
        pass

    def readinput(self, iname="input9.dat"):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]

        if len(lines)!=1:
            raise Exception("Whaaat?")
        self.rawdata = lines[0]
        self.files = {}
        self.frees = {}
        self.newpos = []
        self.rawfiles = self.rawdata[::2]
        self.rawfrees = self.rawdata[1::2]

        for i, d in enumerate(self.rawfiles):
            self.files[i] = int(d)
        for i, d in enumerate(self.rawfrees):
            self.frees[i] = int(d)

    def fill_free_space(self, id, free, junkonly=False):
        for id2, files_end in reversed(self.modified_files.items()):
            # print(id, free, id2, files_end)
            if files_end == 0:
                continue
            if id2 <= id:
                if junkonly:
                    self.newpos+=[0]*free

                return
            files_left = files_end-free
            if files_left < 0:
                files_left = 0
                files_transfered = files_end
                free -= files_transfered
            else:
                if files_left >0 and junkonly:
                    continue
                files_transfered = free
                free = 0

            self.newpos+=[id2]*files_transfered
            self.modified_files[id2] = files_left

    def solve1(self):
        self.readinput()

        
        self.modified_files = self.files.copy()
        for (id, file), free in zip(self.modified_files.items(), self.frees.values()):
            self.newpos+=[id]*file
            self.fill_free_space(id, free)
                    
        res = 0
        # test = ''.join(list((map(str, self.newpos))))
        # print(test)
        for i, v in enumerate(self.newpos):
            res += v*i

        print("Solved1:", res)



    def solve2(self):
        self.readinput()
        self.modified_files = self.files.copy()
        for (id, file), free in zip(self.modified_files.items(), self.frees.values()):
            self.newpos+=[id]*file
            if file==0 and self.files[id] != 0:
                self.newpos+=[0]*self.files[id]
            self.fill_free_space(id, free, junkonly=True)
                    
        res = 0
        # test = ''.join(list((map(str, self.newpos))))
        # print(test)
        for i, v in enumerate(self.newpos):
            res += v*i

        print("Solved2:", res)



if __name__ == "__main__":
    s = PSolver()
    s.solve1()
    s.solve2()
