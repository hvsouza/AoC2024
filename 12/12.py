import numpy as np
import re


class Plant():
    def __init__(self, mytype, group=-1):
        self.mytype = mytype
        self.group = group
    def __repr__(self):
        return f"G{self.group}"

class PSolver():
    def __init__(self):
        pass


    def readinput(self, iname='input12.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
            lines = [ list(line) for line in lines ]

        self.data = lines
        self.m = len(self.data)
        self.n = len(self.data[0])
        self.groups = {}
        self.lastgroup = {}
        self.map_plants = {}
        self.diff = [ -1, 1, -1j, 1j ]
        self.myright = {
             -1:[1j, -1, -1j, 1],
              1:[-1j, 1, 1j, -1],
            -1j:[-1, -1j, 1, 1j],
             1j:[1, 1j, -1, -1j]
        }

    def range_2d(self, m, n):
        for i in range(n):
            for j in range(m):
                yield i, j

    def deepsearch(self, plant, i, j):
        contact = True
        for dx in self.diff:
            i2 = int(i + dx.real)
            j2 = int(j + dx.imag)
            if i2 < 0 or i2 >= self.m or j2 < 0 or j2 >= self.m:
                continue
            otherplant = self.data[i2][j2]
            if plant==otherplant:
                if (i2, j2) in self.map_plants: # join group
                    self.map_plants[(i,j)].group = self.map_plants[(i2,j2)].group
                else:
                    self.map_plants[(i2, j2)] = self.map_plants[(i, j)] #they are now connected
                    self.deepsearch( plant, i2, j2)

    def check_other_plants(self, plant, i, j):
        perimeters = 0
        groups_dict_of_this_type = self.groups[plant]

        if (i, j) not in self.map_plants: # already saw this plant
            self.map_plants[ (i, j) ] = Plant(plant)
        for dx in self.diff:
            i2 = int(i + dx.real)
            j2 = int(j + dx.imag)
            if i2 < 0 or i2 >= self.m or j2 < 0 or j2 >= self.m:
                perimeters+=1
                continue
            otherplant = self.data[i2][j2]
            if plant != otherplant:
                perimeters+=1
            else:
                # print(i2, j2, groups_dict_of_this_type)
                if (i2, j2) in self.map_plants: # join group
                    self.map_plants[(i,j)] = self.map_plants[(i2,j2)]
                else:
                    self.map_plants[(i2, j2)] = self.map_plants[(i, j)] #they are now connected
                    self.deepsearch( plant, i2, j2)
        if self.map_plants[(i,j)].group == -1: # create a new group
            the_last_group = self.lastgroup[ plant ]
            new_group = 1 + the_last_group
            self.lastgroup[ plant ] = new_group
            self.map_plants[(i,j)].group = new_group

        groups_dict_of_this_type[ (i, j) ] = ( self.map_plants[ (i,j) ], perimeters )



    def walk_borders(self, i, j, indexes, second=False):
        fances = 0
        i2 = i
        j2 = j
        check_last = False
        isfirst=True
        if (len(indexes) == 1):
            if second:
                return 0
        while(True):
            thetries = self.myright[self.lastmove]
            for ntries, ttry in enumerate(thetries):
                itmp = int(i2+ttry.real)
                jtmp = int(j2+ttry.imag)
                if (itmp, jtmp) not in indexes: # Nope... keep going
                    pass
                else:
                    if not second:
                        if (i2, j2) not in self.touched:
                            self.touched[(i2,j2)] = [ttry]
                        else:
                            self.touched[(i2,j2)] += [ttry]
                    else:
                        if (i2, j2) in self.touched:
                            if ttry in self.touched[(i2,j2)]:
                                # already walked in this direction... border
                                return 0
                        if (i2, j2) not in self.blobs:
                            self.blobs[(i2,j2)] = [ttry]
                    i2, j2 = itmp, jtmp
                    break

            if self.lastmove != ttry:
                self.lastmove = ttry
                if not isfirst:
                    if ntries>2:
                        fances+=2
                    else:
                        fances+=1
            which = "first" if not second else "second"

            if not second:
                self.print(which, i2, j2, fances, check_last, i, j )

            if check_last:
                if ttry == firsttry:
                    break
                else:
                    check_last = False # well.. not the case
            if (i2, j2) == (i, j):
                check_last=True
            if isfirst:
                firsttry = ttry
            isfirst=False
        return fances

    def print(self, *foo):
        if self.debug:
            print(*foo)


    def _fill_dict(self, tdict, k, v):
        if k not in tdict:
            tdict[k] = [v]
        else:
            tdict[k] += [v]

    def searchblobs(self, indexes):
        _is = {}
        _js = {}
        fences = 0
        for (i, j) in indexes:
            self._fill_dict(_is, i, j)
            self._fill_dict(_js, j, i)

        for i, listjs  in _is.items():
            for j in reversed(listjs):
                if (i, j) in self.touched:
                    if self.touched[(i, j)] == 1:
                        # in this case, cannot go left and went down...
                        continue
                if (i, j) in self.blobs:
                    continue
                if (i, j-1) not in indexes: # so, there is a wall
                    self.lastmove = 1
                    # self.print("Searching border:", i, j, self.blobs, self.touched)
                    fences += self.walk_borders(i, j, indexes, True)

        return fences
    def goaround(self, indexes):
        i, j = indexes[0]
        self.touched = {}
        self.blobs = {}
        # first, find the most top right point
        for jfake in range(j):
            if (i, jfake) in indexes:
                j = jfake
        # print(i, j)
        self.lastmove = 1 # found wall just now, start going down..
        self.faces_sides = self.walk_borders(i, j, indexes)
        self.fences_blob = self.searchblobs(indexes)
        # print("sides..", self.faces_sides, "blobls..",self.fences_blob)
        return self.faces_sides, self.fences_blob

    def solve(self):
        self.readinput()
        for i, j in self.range_2d( self.m, self.m ):
            plant = self.data[i][j]
            if plant not in self.groups: #
                self.groups[ plant ] = {}
            if plant not in self.lastgroup: #
                self.lastgroup[ plant ] = -1
            self.check_other_plants(plant, i, j)

        res = 0
        res2 = 0
        for plant, groups in self.groups.items():
            groups_area_perimeter_plant = {}
            for idx, ( group, perimeters ) in groups.items():
                # print(plant, group, perimeters)
                if group not in groups_area_perimeter_plant:
                    groups_area_perimeter_plant[ group ] = [1, perimeters, plant, [idx]]
                else:
                    groups_area_perimeter_plant[ group ][0] += 1
                    groups_area_perimeter_plant[ group ][1] += perimeters
                    groups_area_perimeter_plant[ group ][3] += [idx]
            for group, (area, perimeter, _, idx) in groups_area_perimeter_plant.items():
                # print("Going around:", plant, group)
                self.debug=False
                # if plant=="I":
                #     self.debug=True
                thefance_side, thefance_blobs = self.goaround(idx)
                thefance = thefance_side + thefance_blobs
                self.print(plant, area, thefance, thefance_side, thefance_blobs)
                res += area*perimeter
                res2 += thefance*area
        print("Solved1:", res)
        print("Solved2:", res2)



if __name__ == "__main__":
    s = PSolver()
    s.solve()
