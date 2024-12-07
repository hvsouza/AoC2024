import numpy as np
from itertools import combinations
from tqdm import tqdm


def readinput(iname='input7.dat'):
    with open(iname) as f:
        lines = f.readlines()
        lines = [ line.strip() for line in lines ]
        lines = [ line.split(":") for line in lines ]
        data = [ (int(line[0]),np.array(list(map(int, line[1].split())), dtype=np.int64)) for line in lines ]

    return data

def place_ones(size, count, standard = 1): # found on StackO. Permutations gives me duplicates
    for positions in combinations(range(size), count):
        p = [0] * size
        for i in positions:
            p[i] = standard
        yield np.array(p)

def try_options(listofmultiplications, values, vref):

    match=False
    for dtypes in listofmultiplications:
        res = values[0]
        for dtype, v in zip(dtypes, values[1:]):
            if dtype>0:
                res*=v
            else:
                res+=v
        if res == vref:
            match=True
    return match

def solve1():
    data = readinput()
    sol1 = np.int64(0)
    for k, v in data:
        totaloperations = len(v)-1
        # print(k, v)
        match = False
        
        for nmult in range( totaloperations + 1):
            listofmultiplications = list( place_ones(totaloperations, nmult) )
            # print(totaloperations, nmult, listofmultiplications)
            _match = try_options(listofmultiplications, v, k)
            if _match:
                match=True

        if match:
            sol1+=np.int64(k)
        # else:
        #     print(k,v)

            

    print("Solved1:", sol1)

def try_options_complex(theoperation, values, vref):
    res = values[0]
    for dtype, v in zip(theoperation, values[1:]):
        if dtype==1:
            res*=v
        elif dtype==0:
            res+=v
        else:
            tmpres = str(res)
            tmpv = str(v)
            res=int(tmpres+tmpv)
    if res == vref:
        return True
    return False

def check_valid(k, v):
    totaloperations = len(v)-1
    
    # print(k, v)
    for nmult in tqdm(range( totaloperations + 1), leave=False):
        listofmultiplications = list(place_ones(totaloperations, nmult))
        # print('...', listofmultiplications)
        for themultiplications in listofmultiplications:
            nzeros = len(themultiplications[themultiplications==0])
            # print('zeros..', nzeros)
            for nconcat in range( nzeros+1 ):
                listofconcat = list( place_ones( nzeros, nconcat, 2) )
                for theconcat in listofconcat:
                    theoperation = themultiplications.copy()
                    theoperation[theoperation==0] = theconcat
                    match = try_options_complex(theoperation, v, k)
                    if match:
                        return k
    return 0
def solve2():
    data = readinput()
    sol2 = np.int64(0)
    for k, v in tqdm(data):
        sol2+=check_valid(k, v)

    print("Solved2:", sol2)

if __name__ == "__main__":
    solve1()
    solve2()
