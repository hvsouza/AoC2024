import numpy as np

class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname="input23.dat"):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
        # There are no duplicates A-B, B-A (checked)
        self.data = lines

    def fillgroups(self, pc1, pc2, groups):
        if pc1 not in groups:
            groups[pc1] = [pc2]
        else:
            groups[pc1].append(pc2)
        return groups

    def checkmax(self, keys, groups):
        for k in keys:
            others = list(keys).copy()
            others.remove(k)
            for pc in others:
                if k not in groups[pc]:
                    return False
        return True

    def solve(self):
        self.readinput()
        connectionlist = self.data.copy()
        groups = {}
        for tmp in connectionlist:
            # print(tmp)
            pc1, pc2 = tmp.split('-')
            groups = self.fillgroups(pc1,pc2,groups)
            groups = self.fillgroups(pc2,pc1,groups)

        groupsthree = {}
        infinitygroup = {}
        for k, listpcs in groups.items():
            for i, pc in enumerate(listpcs[:-1]):
                otherconnections = []
                for otherpc in listpcs[i:]:
                    if otherpc in groups[pc]:
                        if k[0] == "t" or pc[0] == "t" or otherpc[0]=="t":
                            toadd = tuple(sorted([k, pc, otherpc]))
                            groupsthree[toadd] = 1
                        otherconnections.append(otherpc)
                toadd = tuple(sorted([k, pc] + otherconnections))
                infinitygroup[toadd] = 1
        print("Solved1:", len(groupsthree))

        keysmax = list(reversed(sorted(infinitygroup, key=lambda x: len(x))))
        for kmax in keysmax:
            if self.checkmax(kmax, groups):
                print("Solved2:", ','.join(kmax))
                break

s = PSolver()
s.solve()
