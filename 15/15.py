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

    def push_boxes(self, i, j, idiff, jdiff):
        newi, newj = i, j
        myedge = self.stuff[(i,j)]
        while (True):
            newi+=idiff
            newj+=jdiff
            newcoord = (newi, newj) 
            if self.stuff[newcoord] == ".": #No problem.. just move
                self.stuff[newcoord] = "O"
                return True
            elif self.stuff[newcoord] == "#": # Nope...
                return False
            else: # keep going :) 
                continue
        if moved:
            self.robot = newcoord
            self.stuff[newcoord] = "."
        

    def push_big_boxes(self, i, j, idiff, jdiff):
        myedge = self.stuff[(i,j)]
        self.checked = {}
        moved = self.thepush(i, j, idiff, jdiff, False)
        if idiff != 0: # when moving vertically
            if self.stuff[(i,j)] == "]": #look left
                extraj = -1
            else: # look right
                extraj = 1
            moved = moved & self.thepush(i, j+extraj, idiff, jdiff, True)
            
        if moved:
            self.robot = (i, j)
            self.stuff[(i, j)] = "."
        return moved

    def thepush(self, i, j, idiff, jdiff, isedge = False):
        if (i, j) in self.checked:
            if isedge:
                return True
            
        myedge = self.stuff[(i,j)]
        newi, newj = i, j
        while (True):
            self.checked[(newi, newj)] = 1
            previousedge = self.stuff[(newi, newj)]
            newi+=idiff
            newj+=jdiff
            newcoord = (newi, newj) 
            if self.stuff[newcoord] == ".": #No problem.. just move
                self.commands_to_execute.append([newcoord, previousedge])
                if isedge:
                    self.commands_to_execute.append([(i,j), "." ])

                self.checked[(i,j)] = True
                return True
            elif self.stuff[newcoord] == "#": # Nope...
                return False
            else: # keep going :) 
                self.commands_to_execute.append([newcoord, previousedge])
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
        for idx, move in enumerate(self.movements):
            i, j = self.robot
            coord = (i, j) 
            idiff, jdiff = int(move.real), int(move.imag)
            newi, newj  = i+idiff, j+jdiff
            newcoord = (newi, newj) 
            moved = False
            self.commands_to_execute = []
            if self.stuff[newcoord] == ".": #No problem.. just move
                moved = True
            elif self.stuff[newcoord] == "#": # Nope...
                continue
            else:
                if not self.second:
                    moved = self.push_boxes(newi, newj, idiff, jdiff)
                else:
                    moved = self.push_big_boxes(newi, newj, idiff, jdiff)


            if moved:
                if self.second:
                    for _c, _str in self.commands_to_execute:
                        self.stuff[_c] = _str
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
        # self.warehouse = [ list(ware) for ware in self.warehouse ]
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


