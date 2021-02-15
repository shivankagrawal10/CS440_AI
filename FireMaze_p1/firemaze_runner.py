import numpy as np
import random
import heapq
import math
import firemaze as mg
import constants
import copy
import matplotlib.pyplot as plt
import timeit

class experiment:
    def __init__(self, dim : int, p : float, q : float, start : (int, int), end : (int, int), strategy):
        self.maze = mg.maze(dim, p, q)
        self.q = q
        self.start = start
        self.end = end
        y, x = start
        self.agent = (y, x)
        self.maze.grid[y][x] = constants.AGENT
        self.strategy = strategy
        self.switch = False
        self.neighbor_prob={}

    def run(self):
        if not self.maze.fireloc:
                self.start_fire()
        plan = []
        while self.agent != self.end:
            plan = self.advance_agent(self.strategy, plan)
            if not plan:
                break
            new_grid = self.advance_fire()
            y, x = self.agent
            if new_grid[y][x] == constants.FIRE:
                break
            self.maze.grid = new_grid
        if self.agent == self.end:
            return True
        else:
            return False

    def man_run(self):
        if not self.maze.fireloc:
                self.start_fire()
        plan = []
        #print("Start grid")
        #print(self.maze.grid)
        while self.agent != self.end:
            #self.maze.maze_visualize(self.agent,self.maze.grid,0)
            #input("Press any key to continue")
            #print(self.maze.grid)
            plan = self.generate_plan(self.strategy, plan)
            if not plan:
                break
            plan = self.execute_plan(self.strategy, plan)
        #print(self.maze.grid)
        #self.maze.maze_visualize(self.agent,self.maze.grid,1)
        if self.agent == self.end:
            #print("Success")
            return True
        else:
            #print("Failure")
            return False

    def generate_plan(self, strategy, plan):
        if self.maze.grid[self.agent[0]][self.agent[1]] == constants.FIRE:
            return []
        if strategy == constants.STRATEGY_1 and not plan:
            plan, _ = self.maze.Astar(self.agent, self.end)
        elif strategy == constants.STRATEGY_2:
            plan, _ = self.maze.Astar(self.agent, self.end)
        elif strategy == constants.STRATEGY_3:
            plan, _ = self.maze.Marco_Polo(self.agent, self.end)
        elif strategy == constants.STRATEGY_4:
            plan, _ =  self.maze.Marco_Polo(self.agent, self.end)
        elif strategy == constants.STRATEGY_5:
            plan, _ = self.maze.CTF(self.agent, self.end)
        return plan

    def execute_plan(self, strategy, plan):
        times = 0
        switch = False
        if strategy == constants.STRATEGY_1:
            times = len(plan) - 1
        elif strategy == constants.STRATEGY_2 or strategy == constants.STRATEGY_5:
            times = 1
        elif strategy == constants.STRATEGY_3:
            times = self.maze.dist_to_nearest_fire(plan[0])//2
            if times == 0:
                times = 1
        elif strategy == constants.STRATEGY_4:
            if not switch:
                times = (self.maze.dist_to_nearest_fire(plan[0]))-1
            if times <= 1:
                switch = True
                best_prob , best_first_step = self.simulation()
                plan,_ = self.maze.Marco_Polo_Prob(self.agent, self.end,self.neighbor_prob)
                times=5
        for i in range(times):
            #print(plan)
            #input("Step?")
            if self.agent == self.end: 
                plan = []
                break
            if plan:
                curr = plan.pop(0)
                y, x = plan[0]
                if self.maze.grid[y][x] == constants.FIRE:
                    plan = []
                    break
                else:
                    old_y, old_x = self.agent
                    new_y, new_x = self.agent = plan[0]
                    self.maze.grid[old_y][old_x] = constants.OPEN
                    self.maze.grid[new_y][new_x] = constants.AGENT
            else:
                break
            new_grid = self.advance_fire()
            y, x = self.agent
            self.maze.grid = new_grid
            if new_grid[y][x] == constants.FIRE:
                    plan = []
                    break
        return plan


    def advance_agent(self, strategy, plan):
        if strategy == constants.STRATEGY_1 and not plan:
            plan, _ = self.maze.Astar(self.agent, self.end)
        elif strategy == constants.STRATEGY_2:
            plan, _ = self.maze.Astar(self.agent, self.end)
        elif strategy == constants.STRATEGY_3:
            plan, _ = self.maze.Marco_Polo(self.agent,self.end)
            #plan, _ = self.maze.ADAAC(self.agent, self.end)
        elif strategy == constants.STRATEGY_4:
            plan, _ = self.maze.Marco_Polo(self.agent,self.end)
        if plan:
            plan.pop(0)
            y, x = plan[0]
            if self.maze.grid[y][x] == constants.FIRE:
                plan = []
            else:
                old_y, old_x = self.agent
                new_y, new_x = self.agent = plan[0]
                self.maze.grid[old_y][old_x] = constants.OPEN
                self.maze.grid[new_y][new_x] = constants.AGENT
        return plan

    def advance_fire(self):
        clone = self.maze.clone_grid()
        for i in range(self.maze.dim):
            for j in range(self.maze.dim):
                if clone[i][j] != constants.FIRE and clone[i][j] != constants.BLOCKED:
                    prob = self.maze.get_fire_prob((i, j))
                    if prob != 0 and random.random() <= prob:
                        clone[i][j] = constants.FIRE
                        self.maze.fireloc.append((i,j))
        return clone

    def start_fire(self):
        open_cells = []
        for i in range(self.maze.dim):
            for j in range(self.maze.dim):
                if self.maze.grid[i][j] == constants.OPEN:
                    open_cells.append((i, j))
        y, x = random.choice(open_cells)
        self.maze.grid[y][x] = constants.FIRE
        self.maze.fireloc.append((y,x))
        return ((y,x))

    def simulation(self):
        best = (0, self.agent)
        neighbors = list(self.maze.get_neighbors(self.agent,self.maze.is_open))
        if len(neighbors) == 1:
            return (0,neighbors[0])
        for n in neighbors:
                p = self.get_probability(n)
                self.neighbor_prob[n]=p
                if p > best[0]:
                    best = (p, n)
                    if best[0] >= .95:
                        return best
        return best

    def get_probability(self, start: (int, int)):
        success = 0
        times=20
        for i in range(times):
            sim = experiment(self.maze.dim,self.maze.p,self.q,
                             start,self.end,constants.STRATEGY_3)
            sim.maze.grid = self.maze.grid
            sim.maze.fireloc = self.maze.fireloc
            sim.advance_fire()
            if sim.run():
                success += 1
        return (success / times)
