import numpy as np
import awkward as ak
import math
from tqdm import tqdm
import functools
import itertools


class PSolver():
    def __init__(self):
        self.mapkey = {
            0:"A",
            1:"v",
           -1:"^",
          +1j:">",
          -1j:"<",
        }
        self.map_commands_from_to = {
            0: { },  #"A"
          -1j: { },#"<"
           1j: { }, #">"
           -1: { }, #"^"
            1: { },  #"v"
        }
        # Optimized by hand...
        self.map_commands_from_to[0] = {
          -1j: (1,-1j,-1j, 0),
           1j: (1, 0),
           -1: (-1j, 0),
            1: (-1j, 1, 0),
        }
        self.map_commands_from_to[-1j] = {
            0: (1j, 1j, -1, 0),
           1j: (1j, 1j, 0),
           -1: (1j, -1, 0),
            1: (1j, 0),
        }
        self.map_commands_from_to[1j] = {
            0: (-1, 0),
          -1j: (-1j, -1j, 0),
           -1: (-1j, -1, 0),
            1: (-1j, 0),
        }
        self.map_commands_from_to[-1] = {
            0: (1j, 0),
          -1j: (1, -1j, 0),
           1j: (1, 1j, 0),
            1: (1, 0),
        }
        self.map_commands_from_to[1] = {
            0: (-1, 1j, 0),
          -1j: (-1j, 0),
           1j: (1j, 0),
           -1: (-1, 0),
        }
        self.keypad = np.char.array([ ["X"]*3 for _ in range(4)])
        for i, _ in enumerate(range(len(self.keypad)-1)):
            startp = 7-i*3
            for j, v in enumerate(range(startp,startp+3)):
                self.keypad[i][j] = f"{v}"
        self.keypad[3][1] = "0"
        self.keypad[3][2] = "A"


    def get_neighbours(self, pos_direct):
        position = pos_direct[0]
        direction = pos_direct[1]
        return [
            ((position + direction, direction), 1), 
            ((position +  1j*direction,  1j*direction), 1000),
            ((position + -1j*direction, -1j*direction), 1000),
        ]
    def checkpad(self, i, j):
        if i < 0 or i >= len(self.keypad) or j < 0 or j >= len(self.keypad[0]):
            return True
        elif self.keypad[i][j] == "X":
                return True
        else:
            return False
    def findshortest(self, kstart, ktarget):
        start = np.argwhere(self.keypad == kstart)[0]
        target = np.argwhere(self.keypad == ktarget)[0]
        pos = start[0] + 1j*start[1]
        target = target[0] + 1j*target[1]
        diff = target-pos
        idiff = [ math.copysign(1, diff.real) ]*int(abs(diff.real))
        jdiff = [ 1j*math.copysign(1, diff.imag) ]*int(abs(diff.imag))
        moves = [( tuple(idiff) + tuple(jdiff) + (0,), )]
        if len(idiff) > 1 or len(jdiff) > 1:
            moves += [( tuple(jdiff) + tuple(idiff) + (0,), )]
        for diffs in moves.copy():
            newpos = pos
            for d in diffs[0]:
                newpos = newpos+d
                i, j = int(newpos.real), int(newpos.imag)
                if self.keypad[i][j] == "X":
                    moves.remove(diffs)
        return moves



    def readinput(self, iname='input21.dat'):
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
        self.keys = lines

    @functools.cache
    def getcommands(self, move):
        currentposition = 0
        subcommands = ()
        for target in move: # need to press A after every move
            if currentposition == target:
                # old = subcommands[-1]
                # subcommands = subcommands[:-1]
                # subcommands+=((*old, 0),)
                subcommands+=((0,),)
            else:
                listofcommands = self.map_commands_from_to[currentposition][target]
                currentposition = target
                subcommands+=(listofcommands, )
        return subcommands

    # @functools.cache
    def recursive_instruction_robot(self, moves, nrobots):
        commands = ()
        for move in moves:
            subcommands = self.getcommands(move)
            if nrobots == 1:
                commands+=subcommands
            else:
                commands+=self.recursive_instruction_robot(subcommands, nrobots-1)
        return commands
    @functools.cache
    def recursive_instruction_robot_force(self, moves, nrobots):
        commands = ()
        for move in moves:
            subcommands = self.getcommands(move)
            if nrobots == 1:
                commands+=subcommands
            else:
                if self.nrobots - nrobots >=10:
                    # print("here...")
                    commands+=self.recursive_instruction_robot(subcommands, nrobots-1)
                else:
                    commands+=self.recursive_instruction_robot_force(subcommands, nrobots-1)
                # commands+=self.recursive_instruction_robot_force(subcommands, nrobots-1)
        if len(commands) > 10000:
            # print("breaking...", nrobots)
            commands = (tuple(itertools.chain(*commands)), )
        return commands

    def solve(self, nrobots=2):
        self.readinput()
        res = 0
        self.register_moves = {}
        self.nrobots=nrobots
        for dkey in self.keys:
            dkeynum = int(dkey[:-1])
            dkey = "A" + dkey
            lenmoves=0
            for i, c in enumerate(dkey[:-1]):
                minpossible = 1e25
                moves_opt = self.findshortest(c, dkey[i+1])
                for moves in moves_opt:
                    moves = self.recursive_instruction_robot_force(moves, nrobots)
                    theleng = sum(map(len, moves))
                    if theleng < minpossible:
                        minpossible = theleng
                lenmoves += minpossible
            res += lenmoves*dkeynum
        print(f"Solved for {nrobots} robots:", res)
s = PSolver()
s.solve(2)
s.solve(25)



