import numpy as np
import random
import _map as m
import heapq as hq
import constants
import timeit
import copy

class Agent:
    def __init__(self, dim, strategy, input_map, drop_point):
        self.dim = dim
        self.map = input_map
        self.belief = []
        self.build_belief(dim)
        self.strategy = strategy
        self.agent_loc = drop_point
        self.belief = sorted(self.belief, key=lambda element: (element[0], -(abs(element[1][0] - self.agent_loc[0]) + abs(element[1][1] - self.agent_loc[1]))))
        self.dist_trav = 0
        self.num_searches = 0
        #print('Cell to find')
        #print(self.map.target_loc)
        #print('-------')

    def build_belief(self, dim):
        for i in range(dim):
            for j in range(dim):
                self.belief.append([1 / dim ** 2, (i, j)])

    def run(self):
        score = 0
        if self.strategy == 1:
            score = self.strategy1()
        elif self.strategy == 2:
            score = self.strategy2()
        elif self.strategy == 3:
            score = self.strategy3()
        elif self.strategy == 4:
            score = self.strategy4()
        return score

    def strategy1(self):
        check = self.belief[-1]
        t_found = False
        while not t_found:
            t_found, _ = self.update_prob(check)
            self.belief.sort(key=lambda element: (element[0], -(abs(element[1][0] - check[1][0]) + abs(element[1][1] - check[1][1]))))
            check = self.belief[-1]
            #print(check)
        return self.num_searches + self.dist_trav
        #print('Done')

    def strategy2(self):
        priority = [[x[0] * (1 - self.map.get_terrain(x[1])), x[0], x[1]]
                    for x in self.belief]
        priority.sort(key=lambda element: (element[0], -(abs(element[2][0] - self.agent_loc[0]) + abs(element[2][1] - self.agent_loc[1]))))
        check = priority[-1][1:]
        t_found = False
        while not t_found:
            t_found, _ = self.update_prob(check)
            priority = [[x[0] * (1 - self.map.get_terrain(x[1])),x[0],x[1]]
                for x in self.belief]
            priority.sort(key=lambda element: (element[0], -(abs(element[2][0] - check[1][0]) + abs(element[2][1] - check[1][1]))))
            check = priority[-1][1:]
        return self.num_searches + self.dist_trav
        #print('Done')

    def strategy3(self):
                check = [1/self.dim**2,(0,0)]
                while(not self.update_prob(check)):
                        #print(check)
                        check = self.utility(check[1],self.belief)
                return(self.num_searches + self.dist_trav)

    def strategy4(self):
        check = self.value()
        while(not self.update_prob(check)):
            check = self.value()
            #print(check)
        return self.num_searches + self.dist_trav

    def dumb_strat(self):
        priority = [[x[0] * (1 - self.map.get_terrain(x[1])), x[0], x[1]]
                    for x in self.belief]
        priority.sort(key=lambda element: (element[0], -(abs(element[2][0] - self.agent_loc[0]) + abs(element[2][1] - self.agent_loc[1]))))
        check = priority[-1][1:]
        t_found = False
        while not t_found:
            terrain = self.map.get_terrain(check[1])
            num_checks = 0
            if terrain == constants.flat:
                num_checks = 2
            elif terrain == constants.hilly:
                num_checks = 2
            elif terrain == constants.forested:
                num_checks = 4
            elif terrain == constants.maze_of_caves:
                num_checks = 10
            else:
                print('error')
            for i in range(num_checks):
                t_found, posterior = self.update_prob(check)
                if t_found:
                    break
                check = (posterior, check[1])
            priority = [[x[0] * (1 - self.map.get_terrain(x[1])),x[0],x[1]]
                for x in self.belief]
            priority.sort(key=lambda element: (element[0], -(abs(element[2][0] - check[1][0]) + abs(element[2][1] - check[1][1]))))
            check = priority[-1][1:]
            #print(self.num_searches + self.dist_trav)
        return self.num_searches + self.dist_trav

    def utility(self,location,belief):
                #return [prob , (x,y)]

                #immediate utility
                immediate = []
                for prob,cell in self.belief:
                        terrain = self.map.get_terrain(cell)
                        dist = abs(location[0]-cell[0]) + abs(location[1]-cell[1])
                        max_cost = max([self.dist(cell,(0,0)),
                                        self.dist(cell,(0,self.dim-1)),
                                        self.dist(cell,(self.dim-1,0)),
                                        self.dist(cell,(self.dim-1,self.dim-1))])
                        util = (self.dim*self.dim)*(self.dim*2+1)*(1-terrain)*prob - (1+dist) * (1-(1-terrain)*prob)
                        immediate.append([util,prob,cell])
                immediate.sort()
                return(immediate[-1][1:])
    def dist(self,start,end):
            return(abs(start[0]-end[0]) + abs(start[1]-end[1]))



    def update_prob(self,check):
        iprior,check_cell = check
        self.num_searches += 1
        self.dist_trav += abs(self.agent_loc[0] - check_cell[0]) + abs(self.agent_loc[1] - check_cell[1])
        #print(self.dist_trav)
        self.agent_loc = check_cell
        if self.map.query(check_cell):
            #game over
            return (True, iprior)
        terrain = self.map.get_terrain(check_cell)
        denominator = (iprior * terrain + (1 - iprior))
        now = []
        posterior = iprior
        for prior,cell in self.belief:
            curr = prior / denominator
            if cell == check_cell:
                curr *= terrain
                posterior = curr
            now.append([curr,cell])
        self.belief = now
        self.sanity_check()
        #print(self.belief)
        #print(check[1])
        #input()
        return(False, posterior)

    def min_cost(self):
        base = self.num_searches + self.dist_trav
        min_cost = np.Inf
        min_belief = None
        for belief in self.belief:
            dist_trav = abs(belief[1][0] - self.agent_loc[0]) + abs(belief[1][1] - self.agent_loc[1])
            p_success = (1 - self.map.get_terrain(belief[1])) * belief[0]
            p_fail = belief[0] * self.map.get_terrain(belief[1]) + (1 - belief[0])
            cost = (1 + dist_trav) + base + (p_success * base + p_fail * U_start)
            if U_start_step > U_max:
                U_max = U_start_step
                argmax = belief

    def value(self):
        min_cost = np.Inf
        min_belief = None
        for belief in self.belief:
            #print(belief)
            #input()
            belief_cost = self.cost(belief)
            #print(belief)
            if belief_cost < min_cost:
                min_cost = belief_cost
                min_belief = belief
        return min_belief

    def cost(self, belief):
        dist_trav = abs(belief[1][0] - self.agent_loc[0]) + abs(belief[1][1] - self.agent_loc[1])
        p_success = (1 - self.map.get_terrain(belief[1])) * belief[0]
        exp_future = self.dim ** 3
        cost = 1 + dist_trav + (1 - p_success) * exp_future
        #print(cost)
        #input()
        return cost

    def value_iteration(self):
        #input()
        Beta = .9
        U_start = -(self.num_searches + self.dist_trav)
        U_end = (self.map.dim ** 2) * 10 
        delta = 100
        belief = None
        iteration = 0
        while delta >= 100 or iteration == 100:
            U_max = np.NINF
            argmax = None
            for belief in self.belief:
                dist_trav = abs(belief[1][0] - self.agent_loc[0]) + abs(belief[1][1] - self.agent_loc[1])
                p_success = (1 - self.map.get_terrain(belief[1])) * belief[0]
                p_fail = belief[0] * self.map.get_terrain(belief[1]) + (1 - belief[0])
                U_start_step = -(1 + dist_trav) + Beta * (p_success * U_end + p_fail * U_start)
                if U_start_step > U_max:
                    U_max = U_start_step
                    argmax = belief
            delta = abs(U_start - U_max)
            U_start = U_max
            belief = argmax
            iteration += 1
        #print(U_start)
        #input()
        return belief

    def value_iteration2(self):
        beliefs = copy.deepcopy(self.belief)
        #input()
        Beta = .9
        U_start = 0
        U_end = -(self.num_searches + self.dist_trav)
        delta = 1
        belief = None
        iteration = 0
        while delta >= 1:
            U_min = np.Inf
            argmin = None
            for belief in beliefs:
                dist_trav = abs(belief[1][0] - self.agent_loc[0]) + abs(belief[1][1] - self.agent_loc[1])
                p_success = (1 - self.map.get_terrain(belief[1])) * belief[0]
                p_fail = belief[0] * self.map.get_terrain(belief[1]) + (1 - belief[0])
                U_start_step = (1 + dist_trav) + Beta * (p_success * U_end + p_fail * U_start)
                if U_start_step < U_min:
                    U_min = U_start_step
                    argmin = belief
            delta = abs(U_start - U_min)
            U_start = U_min
            belief = argmin
            iteration += 1
        #print(U_start)
        #input()
        return belief

    def sanity_check(self):
        total_prob = 0
        for belief in self.belief:
            total_prob += belief[0]
        if abs(total_prob - 1) > .01:
            print("Total prob is", total_prob)

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
