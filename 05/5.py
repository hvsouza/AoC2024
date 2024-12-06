import numpy as np


def readinput(iname='input5.dat'):
    with open(iname,'r') as f:
        lines = f.readlines()


    rules = {}
    updates = []
    readrules = True
    for line in lines:
        if line=="\n":
            readrules=False
            continue
        if readrules:
            rule = line.strip().split('|')
            pl = int(rule[0])
            pr = int(rule[1])
            if pl not in rules.keys():
                rules[pl] = [pr]
            else:
                rules[pl].append(pr)

        else:
            page = line.strip().split(',')
            page = [ int(p) for p in page ]
            updates.append(page)



    rules = dict(sorted(rules.items()))
    rules = { k: sorted(v) for k, v in rules.items() } 

    return rules, updates

def solve1():
    res=0
    rules, updates = readinput()
    for update in updates:
        # for i, page in reversed(list(enumerate(update))):
        isok = True
        for i, page in enumerate(update):
            if not isok:
                break
            for otherpage in update[i:]:
                if otherpage not in rules:
                    continue
                rules_for_otherpage = rules[otherpage]
                if page in rules_for_otherpage:
                    isok=False
                    break
        if isok:
            middlepoint = update[int(len(update)//2)]
            res+=middlepoint

    print("Solved1:", res)

def solve2():
    res=0
    rules, updates = readinput()
    updates_notok = []
    for update in updates:
        # for i, page in reversed(list(enumerate(update))):
        isok = True
        for i, page in enumerate(update):
            if not isok:
                break
            for otherpage in update[i:]:
                if otherpage not in rules:
                    continue
                rules_for_otherpage = rules[otherpage]
                if page in rules_for_otherpage:
                    isok=False
                    break
        if not isok:
            updates_notok.append(update)


    for update in updates_notok:
        new_update = np.array(update.copy())
        for i, page in enumerate(update):
            if page not in rules.keys() or i==0:
                continue
            page_is_before_of = rules[page]
            for j, pagesbefore in reversed(list(enumerate(new_update[:i]))): 
                if pagesbefore in page_is_before_of: # they should swap
                    current_page_idx = np.argwhere(new_update==page)[0][0]
                    new_page_idx = np.argwhere(new_update==pagesbefore)[0][0]
                    new_update[current_page_idx], new_update[new_page_idx] = new_update[new_page_idx], new_update[current_page_idx]
                    
        middlepoint = new_update[int(len(new_update)//2)]
        res+=middlepoint
    print("Solved2:", res)



            





if __name__ == "__main__":
    solve1()
    solve2()
