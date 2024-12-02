import numpy as np


def readinput(iname):
    with open(iname) as f:
        lines = f.readlines()
        lines = [ line.strip() for line in lines ]
        data = [ np.array([ int(v) for v in line.split() ]) for line in lines ]
    return data

def solve1():

    data = readinput("input2.dat")

    safereports = 0
    for r in data:
        d = r[1:] - r[:-1]

        isvalid=False
        if (np.all(d>0) or np.all(d<0)) and np.all(np.abs(d)<=3):
            isvalid=True
            safereports+=1
        else:
            pass

        # if isvalid:
        #     print(r)
    print("Solved1:", safereports)


def deepclean(r, d):
    for i in range(len(r)):
        r2 = np.delete(r, i) #remove the previous element
        d2 = r2[1:] - r2[:-1]
        found_now = allgutch(d2)
        if found_now:
            return True
    return False


def allgutch(d):
    if (np.all(d>0) or np.all(d<0)) and np.all(np.abs(d)<=3):
        return True
    else:
        return False

def make_check(r, d, isvalid, safereports):
    if allgutch(d):
        isvalid=True
        safereports+=1
    else:
        found = deepclean(r, d)
        if found:
            isvalid=True
            safereports+=1

    return isvalid, safereports


def solve2():

    data = readinput("input2.dat")
    safereports = 0
    for r in data:
        d = r[1:] - r[:-1]
        isvalid=False
        isvalid, safereports = make_check(r, d, isvalid, safereports)

    print("Solved2:", safereports)

if __name__ == "__main__":

    solve1()
    solve2()

