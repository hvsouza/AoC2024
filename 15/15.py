import numpy as np
import re



class PSolver():
    def __init__(self):
        self.second=False


    def readinput(self, iname='input15.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
        separator = lines.index('')

        warehouse = lines[:separator]
        movements = lines[separator+1:]
        self.stuff = {}

        mapmovements = {"<":-1j, "^":-1, ">":1j, "v":1}
        if self.second:
            for i, line in enumerate(warehouse):
                warehouse[i] = warehouse[i].replace("#", "##")
                warehouse[i] = warehouse[i].replace("O", "[]")
                warehouse[i] = warehouse[i].replace(".", "..")
                warehouse[i] = warehouse[i].replace("@", "@.")
        self.warehouse = warehouse
        for i, line in enumerate(warehouse):
            for j, c in enumerate(line):
                self.stuff[(i, j)] = c
                if c == "@":
                    self.robot = (i, j)
                    self.stuff[(i, j)] = "."

        movements = ''.join(movements)
        self.movements = [ mapmovements[c] for c in movements ]


    def push_big_boxes(self, i, j, idiff, jdiff):
        myedge = self.stuff[(i,j)]
        moved = self.thepush(i, j, idiff, jdiff, False)
        if self.second:
            if idiff != 0: # when moving vertically
                if self.stuff[(i,j)] == "]": #look left
                    extraj = -1
                else: # look right
                    extraj = 1
                moved = moved & self.thepush(i, j+extraj, idiff, jdiff, True)
            
        if moved:
            self.robot = (i, j)
            self.places_to_change[(i, j)] = True
        return moved

    def thepush(self, i, j, idiff, jdiff, isedge = False):
            
        if (i, j) in self.places_to_change:
            return True
            # nothing to do... 
        myedge = self.stuff[(i,j)]
        newi, newj = i, j
        self.places_to_change[(i,j)] = isedge
        while (True):
            previousedge = self.stuff[(newi, newj)]
            newi+=idiff
            newj+=jdiff
            newcoord = (newi, newj) 
            if self.stuff[newcoord] == ".": #No problem.. just move
                self.places_to_change[newcoord] = False
                return True
            elif self.stuff[newcoord] == "#": # Nope...
                return False
            else: # keep going :) 
                self.places_to_change[newcoord] = False
                if self.second:
                    if idiff!=0 and self.stuff[newcoord] != previousedge:
                        if self.stuff[newcoord] == "]": #look left
                            extraj = -1
                        else: # look right
                            extraj = 1
                        anotherextraj = j + extraj # j is not moving..
                        moved = self.thepush(newi, anotherextraj, idiff, jdiff, True)
                        if not moved:
                            return False


    def execute_commands(self):
        for idx, move in enumerate(self.movements[:None]):
            i, j = self.robot
            coord = (i, j) 
            idiff, jdiff = int(move.real), int(move.imag)
            newi, newj  = i+idiff, j+jdiff
            newcoord = (newi, newj) 
            moved = False
            self.places_to_change = {}
            if self.stuff[newcoord] == ".": #No problem.. just move
                moved = True
            elif self.stuff[newcoord] == "#": # Nope...
                continue
            else:
                moved = self.push_big_boxes(newi, newj, idiff, jdiff)


            if moved:
                original = { _c: self.stuff[_c] for _c in self.places_to_change.keys() }
                for _c, _isedge in self.places_to_change.items():
                    if not _isedge:
                        ilow = _c[0] - idiff
                        jlow = _c[1] - jdiff
                        self.stuff[_c] = original[(ilow, jlow)]
                    else:
                        self.stuff[_c] = "."

                self.robot = newcoord
                self.stuff[newcoord] = "."


    def solve1(self):
        self.readinput()
        self.execute_commands()
        res = 0
        for coord, stuff in self.stuff.items():
            if stuff == "O":
                res += 100*coord[0] + coord[1]
        print("Solved1:", res)

    def solve2(self):
        self.second=True
        self.readinput()

        self.execute_commands()
        self.warehouse = [ list(ware) for ware in self.warehouse ]
        # for i, line in enumerate(self.warehouse):
        #     for j, c in enumerate(line):
        #         self.warehouse[i][j] = self.stuff[(i,j)]
        #         if (i, j) == self.robot:
        #             self.warehouse[i][j] = "@"
        #     print(''.join(self.warehouse[i]))

        res = 0
        for coord, stuff in self.stuff.items():
            if stuff == "[":
                res += 100*coord[0] + coord[1]
        print("Solved2:", res)


if __name__ == "__main__":
    s = PSolver()
    s.solve1()
    s.solve2()


