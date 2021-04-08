import numpy as np
import random
import _map as m
import heapq as hq
import constants
import timeit

class Agent:
        def __init__(self,dim,strategy):
                self.map = m.Map(dim)
                self.belief = []
                for i in range(dim):
                        for j in range(dim):
                                self.belief.append([1/dim**2,(i,j)])
                self.belief.sort()
                self.strategy = strategy
                #print('Cell to find')
                #print(self.map.target_loc)
                #print('-------')
                #need to implement random starting cell
                self.agent = [1/dim**2,(0,0)]

        def run(self):
                if self.strategy == 1:
                        self.strategy1()
                if self.strategy == 2:
                        self.strategy2()
                if self.strategy == 3:
                        self.strategy3()

        def strategy1(self):
                check = self.belief[-1]
                while(not self.update_prob(check)):
                        check = self.belief[-1]
                        #print(check_cell)
                #print('Done')

        def strategy2(self):
                priority = [[x[0]*(1-self.map.get_terrain(x[1])),x[0],x[1]]
                            for x in self.belief]
                priority.sort()
                check = priority[-1][1:]
                while(not self.update_prob(check)):
                        priority = [[x[0]*(1-self.map.get_terrain(x[1])),x[0],x[1]]
                            for x in self.belief]
                        priority.sort()
                        check = priority[-1][1:]
                #print('Done')

        def strategy3(self):
                check = self.agent
                while(not self.update_prob(check)):
                        #print(check)
                        check = self.utility(self.agent[1],self.belief)
        
        def update_prob(self,check):
                iprior,check_cell = check
                if self.map.query(check_cell):
                        #game over
                        print('Done')
                        return(True)
                terrain = self.map.get_terrain(check_cell)
                denominator = (iprior*terrain+(1-iprior))
                now = []
                for prior,cell in self.belief:
                        curr = prior/denominator
                        if cell == check_cell:
                                curr*=terrain
                        now.append([curr,cell])
                self.belief = now
                self.belief.sort()
                return(False)

        def utility(self,location,belief):
                #return [prob , (x,y)]

                #immediate utility
                immediate = []
                for prob,cell in self.belief:
                        terrain = self.map.get_terrain(cell)
                        dist = abs(location[0]-cell[0]) + abs(location[1]-cell[1])
                        util = 100*21*terrain*prob - (1+dist) * (1-terrain*prob)
                        immediate.append([util,prob,cell])
                immediate.sort()
                return(immediate[-1][1:])
'''
s1 = []
s2 = []
for i in range(100):
        start = timeit.default_timer()
        a = Agent(10,1)
        a.run()
        s1.append(timeit.default_timer()-start)

        start = timeit.default_timer()
        b = Agent(10,2)
        b.run()
        s2.append(timeit.default_timer()-start)

print(sum(s1)/len(s1))
print(sum(s2)/len(s1))
'''

a = Agent(10,3)
a.run()
