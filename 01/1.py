import numpy as np
import pandas as pd


def readinput(iname):
    df = pd.read_csv(iname, delim_whitespace=True, header=None);
    return df

def solve1():
    df = readinput("input1.dat")
    d1 = df[0].to_numpy()
    d2 = df[1].to_numpy()

    d1 = np.sort(d1)
    d2 = np.sort(d2)

    diff:np.array = d2-d1
    print("Solved1:", np.abs(diff).sum())
    
def solve2():
    df = readinput("input1.dat")
    """
    Simple solution
    """
    # dfcountr = df[1].value_counts()
    # ntimes:dict = dfcountr.to_dict()
    # values = df[0].to_numpy()
    # score = np.array([ v*ntimes[v] if v in ntimes.keys() else 0 for v in values ])
    # print("Solved2:", score.sum())
    """
    Practice kung fu panda
    """
    df.columns = ["left", "right"]
    dfcountr = df['right'].value_counts().rename("counts")
    dfscore = df['left'].to_frame()
    dfscore = dfscore.merge(dfcountr, left_on="left", right_index=True)
    dfscore['scores'] = dfscore['left']*dfscore['counts']
    print("Solved2:", dfscore['scores'].sum())
    


if __name__ == "__main__":

    solve1()
    
    solve2()
