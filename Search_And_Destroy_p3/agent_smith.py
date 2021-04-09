import numpy as np
import random
import _map_smith as m
import constants
import math

class Agent:
    def __init__(self, dim, strategy, input_map, drop_point, bonus):
        self.dim = dim
        self.map = input_map
        self.belief = []
        self.build_belief(dim)
        self.strategy = strategy
        self.agent_loc = drop_point
        self.belief.sort(key=lambda element: (element[0], -(abs(element[1][0] - self.agent_loc[0]) + abs(element[1][1] - self.agent_loc[1]))))
        self.dist_trav = 0
        self.num_searches = 0
        self.bonus = bonus

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
            if self.bonus:
                self.map.move_target()
            self.belief.sort(key=lambda element: (element[0], -(abs(element[1][0] - check[1][0]) + abs(element[1][1] - check[1][1]))))
            check = self.belief[-1]
        return self.num_searches + self.dist_trav

    def strategy2(self):
        priority = self.get_priority()
        check = priority[-1][1:]
        t_found = False
        while not t_found:
            t_found, _ = self.update_prob(check)
            if self.bonus:
                self.map.move_target()
            priority = self.get_priority()
            check = priority[-1][1:]
        return self.num_searches + self.dist_trav

    def strategy3(self):
        check = self.agent
        while(not self.update_prob(check)):
            check = self.utility(self.agent[1],self.belief)

    def strategy4(self):
        priority = self.get_priority()
        check = priority[-1][1:]
        t_found = False
        while not t_found:
            exp_num_srch = math.ceil(1 / (1 - self.map.get_terrain(check[1])))
            for i in range(exp_num_srch):
                t_found, posterior = self.update_prob(check)
                if self.bonus:
                    self.map.move_target()
                if t_found:
                    break
                check = (posterior, check[1])
            priority = self.get_priority()
            check = priority[-1][1:]
        return self.num_searches + self.dist_trav

    def get_priority(self):
        priority = [[x[0] * (1 - self.map.get_terrain(x[1])), x[0], x[1]]
                    for x in self.belief]
        priority.sort(key=lambda element: (element[0], -(abs(element[2][0] - self.agent_loc[0]) + abs(element[2][1] - self.agent_loc[1]))))
        return priority

    def utility(self,location,belief):
        immediate = []
        for prob,cell in self.belief:
            terrain = self.map.get_terrain(cell)
            dist = abs(location[0]-cell[0]) + abs(location[1]-cell[1])
            util = 100*21*terrain*prob - (1+dist) * (1-terrain*prob)
            immediate.append([util,prob,cell])
        immediate.sort()
        return(immediate[-1][1:])

    def update_prob(self,check):
        iprior,check_cell = check
        self.num_searches += 1
        self.dist_trav += abs(self.agent_loc[0] - check_cell[0]) + abs(self.agent_loc[1] - check_cell[1])
        self.agent_loc = check_cell
        t_found, within_diamond = self.map.query(check_cell)
        if t_found:
            return (True, iprior)
        terrain = self.map.get_terrain(check_cell)
        denominator = (iprior * terrain + (1 - iprior))
        now = []
        posterior = iprior
        total_prob = 0
        for prior,cell in self.belief:
            curr = prior / denominator
            if cell == check_cell:
                curr *= terrain
                posterior = curr
            total_prob += curr
            now.append([curr,cell])
        now_prime = []
        for prior, cell in now:
            curr = prior / total_prob
            if cell == check_cell:
                posterior = curr
            now_prime.append([curr,cell])
        self.belief = now_prime
        if self.bonus:
            posterior = self.bonus_update(check_cell, within_diamond, iprior)
        self.sanity_check()
        return(False, posterior)

    def bonus_update(self, check_cell, within_diamond, iprior):
        posterior = None
        # Partition set into cells within diamond and those outside diamond
        in_diamond = set()
        out_diamond = set()
        cells = [belief[1] for belief in self.belief]
        for cell in cells:
            m_dist = abs(cell[0] - self.agent_loc[0]) + abs(cell[1] - self.agent_loc[1])
            if m_dist <= 5:
                in_diamond.add(cell)
            else:
                out_diamond.add(cell)
        #Calculate the total prior belief that target was in region it is actually not in
        t_prob = 0
        for belief in self.belief: 
            if within_diamond and belief[1] in out_diamond:
                t_prob += belief[0]
            elif not within_diamond and belief[1] in in_diamond:
                t_prob += belief[0]
        #Normalize non-zero beliefs
        new_belief = []
        zero_belief = []
        posterior = iprior
        total_belief = 0
        for belief in self.belief:
            new_prob = None
            if within_diamond:
                if belief[0] == 0 and belief[1] in in_diamond:
                    zero_belief.append(belief)
                    continue
                new_prob = 0 if belief[1] in out_diamond else belief[0] / abs(1 - t_prob)
            else:
                if belief[0] == 0 and belief[1] in out_diamond:
                    zero_belief.append(belief)
                    continue
                new_prob = 0 if belief[1] in in_diamond else belief[0] / abs(1 - t_prob)
            new_belief.append((new_prob, belief[1]))
            total_belief += new_prob
            if belief[1] == check_cell:
                posterior = new_prob
        #Normalize zero beliefs
        prob_left = 1 - total_belief if 1 - total_belief > 0 else 0
        num_left = len(zero_belief) if len(zero_belief) > 0 else 1
        prob_per_belief = prob_left / num_left if (prob_left - (prob_left / num_left)) > 0 else 0
        if prob_per_belief == 0:
            for belief in zero_belief:
                new_belief.append((prob_per_belief, belief[1]))
                if belief[1] == check_cell:
                    posterior = prob_per_belief
        else:
            for belief in zero_belief:
                new_belief.append((prob_per_belief, belief[1]))
                if belief[1] == check_cell:
                    posterior = prob_per_belief
                prob_left = prob_left - prob_per_belief if prob_left - prob_per_belief > 0 else 0
                num_left = num_left - 1 if num_left - 1 > 0 else 1
                prob_per_belief = prob_left / num_left if (prob_left - (prob_left / num_left)) > 0 else 0
        '''
        self.belief = new_belief
        return posterior

    def sanity_check(self):
        total_prob = 0
        for belief in self.belief:
            total_prob += belief[0]
        if abs(total_prob - 1) > .01:
            print("Total prob is", total_prob)
            input()

