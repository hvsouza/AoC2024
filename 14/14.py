import numpy as np
import re
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from tqdm import tqdm
import copy


class MrRobot():
    def __init__(self, x, y, vx, vy, id):
        self.ox = x
        self.oy = y
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.id = id
        self.xmax = 101
        self.ymax = 103
        # self.xmax = 11
        # self.ymax = 7
        self.historyprotocol = False
        self.paths = [(self.ox,self.oy)]
        self.idx = 0

    def _getnewpos(self, s, v, t, tmax):
        return (s + v*t)%tmax
    def move(self, seconds=100):
        if not self.historyprotocol:
            self.x = self._getnewpos(self.x, self.vx, seconds, self.xmax)
            self.y = self._getnewpos(self.y, self.vy, seconds, self.ymax)
            if self.ox == self.x and self.oy == self.y:
                self.historyprotocol = True
                self.maxpath=len(self.paths)
            else:
                self.paths.append((self.x,self.y))
        else:
            if self.idx < self.maxpath-1:
                self.idx+=1
            else:
                self.idx=0
            self.x = self.paths[self.idx][0]
            self.y = self.paths[self.idx][0]




    def __repr__(self):
        return f"Robot {self.id}: x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}"

class PSolver():
    def __init__(self):
        self.xmax = 101
        self.ymax = 103

    def readinput(self, iname="./input14.dat"):
        self.robots = [] #order 66
        with open(iname) as f:
            lines = f.readlines()
            lines = [ line.strip() for line in lines if line.strip() ]
            p = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
            for i, line in enumerate(lines): 
                m = p.match(line)
                x  = int(m.group(1))
                y  = int(m.group(2))
                vx = int(m.group(3))
                vy = int(m.group(4))
                robot = MrRobot(x,y,vx,vy, i)
                self.robots.append(robot)


    def range_2d(self, tlist):
        m = len(tlist)
        n = len(tlist[0])
        for i in range(m):
            for j in range(n):
                yield i, j


    def precise_step(self, seconds):
        self.readinput()
        self.viewer = [ ["."]*self.xmax for _ in range(self.ymax) ]
        self.slots = np.array([ [0]*self.xmax for _ in range(self.ymax) ])
        for robot in self.robots:
            robot:MrRobot
            robot.move(seconds = seconds)
            self.slots[robot.y][robot.x] +=1

        for i, j in self.range_2d(self.viewer):
            if self.slots[i][j]>0:
                self.viewer[i][j] = str(self.slots[i][j])

    def solve1(self):
        self.readinput()
        self.precise_step(seconds=100)
        # for view in self.viewer:
        #     print(''.join(view))
        self.quadrants = [ None ]*4
        self.quadrants[0] = self.slots[:self.ymax//2, :self.xmax//2]
        self.quadrants[1] = self.slots[:self.ymax//2, self.xmax//2+(self.xmax%2):]
        self.quadrants[2] = self.slots[self.ymax//2+(self.ymax%2):, self.xmax//2+(self.xmax%2):]
        self.quadrants[3] = self.slots[self.ymax//2+(self.ymax%2):, :self.xmax//2]
        res = 1
        for quad in self.quadrants:
            nrobots = quad.sum()
            res*=nrobots
        print("Solved1:", res)

    def update(self, i):
        self.im.set_array(self.image_array[i][0])
        self.t:plt.annotate
        # self.t.set_text(self.image_array[i][1])
        return [self.im]


    def solve2(self):
        self.readinput()
        self.part1slot = copy.deepcopy(self.slots)
        self.slots = np.array([ [0]*self.xmax for _ in range(self.ymax) ])
        protocols = np.array([ False for _ in self.robots ])

        while(True): # limit is # self.xmax * self.ymax
            for i, robot in enumerate(self.robots):
                robot:MrRobot
                robot.move(seconds=1)
                if robot.historyprotocol:
                    protocols[i] = True
            if np.all(protocols):
                print("All robots know... ")
                break

        thematches = { i: 0 for i, _ in enumerate(self.robots[0].paths) }
        for robot in self.robots:
            robot.paths = np.array(robot.paths)
        for i, robot in enumerate(tqdm(self.robots[:-1])):
            the_robot_path = robot.paths
            for j, otherrobot in enumerate(self.robots[i+1:]):
                if j == i: #myself...
                    continue 
                arrmatch = np.where(the_robot_path == np.array(otherrobot.paths))
                if len(arrmatch) == 0:
                    arrmatch = []
                for idx in arrmatch[0]:
                    thematches[idx] += 1

        
        thematches = {k: v for k, v in reversed(sorted(thematches.items(), key=lambda item: item[1]))}
        seconds, counts = list(thematches.items())[0]
        print("Solved2:", seconds)
        # self.image_array = []
        # for second in range(seconds-100, seconds+1):
        #     self.precise_step(second)
        #     self.image_array.append([ copy.deepcopy(self.slots), second ])
        
        # fig, self.ax = plt.subplots()
        # for i, (imag, second) in enumerate(self.image_array):
        #     self.ax:plt.Axes
        #     self.ax:plt.Axes
        #     self.im = self.ax.imshow( imag)
        #     self.ax.set_title("Day 14 :o")
        #     # self.t = self.ax.annotate(self.image_array[0][1], xy=(1, 1), xycoords="axes fraction", fontsize=16)
            

        #     # # Create the animation object
        #     # animation_fig = animation.FuncAnimation(fig, self.update, frames=len(self.image_array), interval=25, blit=True, repeat=True, repeat_delay=2000)

        #     # # Show the ianimation
        #     # plt.show()

        #     # animation_fig.save("xtree.gif", writer=animation.ImageMagickWriter( fps=25,  extra_args=[ '-delay', '2' ]))
        #     # animation_fig.save("xtree.gif", writer='ffmpeg')
        #     plt.savefig(f"frames/frame{i}.png")


if __name__ == "__main__":
    s = PSolver()
    s.solve1()
    s.solve2()

