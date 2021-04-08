import numpy as np
import random
import _map as m
import heapq as hq
import constants
import timeit

class Agent:
    def __init__(self, dim, strategy):
        self.map = m.Map(dim)
        self.agent_loc = self.get_drop_point(dim)
        self.belief = []
        self.build_belief(dim)
        self.strategy = strategy
        self.dist_trav = 0
        self.num_searches = 0
        #print('Cell to find', '\n', self.map.target_loc, '\n', '-------')

    def get_drop_point(self, dim):
        i = np.random.randint(0, high=dim)
        j = np.random.randint(0, high=dim)
        return (i, j)

    def build_belief(self, dim):
        y, x = self.agent_loc
        for i in range(dim):
            for j in range(dim):
                self.belief.append([1 / dim ** 2, -(abs(y - i) + abs(x - j)), (i, j)])
        self.belief.sort()

    def run(self):
        if self.strategy == 1:
            self.strategy1()
        if self.strategy == 2:
            self.strategy2()

    def strategy1(self):
        check = self.belief[-1]
        while(not self.update_prob(check)):
            check = self.belief[-1]
            #print(check_cell)
        #print('Done')

    def strategy2(self):
        priority = [[x[0] * self.map.get_terrain(x[1]), x[0], x[1]]
                    for x in self.belief]
        priority.sort()
        check = priority[-1][1:]
        while(not self.update_prob(check)):
            priority = [[x[0] * self.map.get_terrain(x[1]),x[0],x[1]]
                for x in self.belief]
            #priority.sort()
            priority = sorted(priority, key=lambda element: (element[0], -(abs(element[1][0] - check[1][0]) + abs(element[1][1] - check[1][1]))))
            check = priority[-1][1:]
        #print('Done')

    def update_prob(self,check):
        iprior,check_cell = check
        if self.map.query(check_cell):
            #game over
            return(True)
        terrain = self.map.get_terrain(check_cell)
        denominator = (iprior * terrain + (1 - iprior))
        now = []
        for prior,cell in self.belief:
            curr = prior / denominator
            if cell == check_cell:
                    curr *= terrain
            now.append([curr,cell])
        self.belief = now
        #self.belief.sort()
        self.belief = sorted(self.belief, key=lambda element: (element[0], -(abs(element[1][0] - check[1][0]) + abs(element[1][1] - check[1][1]))))
        print(self.belief)
        print(check[1])
        input()
        return(False)
'''
s1 = []
s2 = []
for i in range(1000):
    start = timeit.default_timer()
    a = Agent(10,1)
    a.run()
    #s1.append(timeit.default_timer()-start)

    start = timeit.default_timer()
    b = Agent(10,2)
    b.run()
    s2.append(timeit.default_timer()-start)
print(sum(s1)/len(s1))
print(sum(s2)/len(s1))
'''
agent = Agent(50, 1)
print(agent.agent_loc)
print(agent.belief)
