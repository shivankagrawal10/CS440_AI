import numpy as np
import random
import heapq
import math
import firemaze as mg
import constants
import copy

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

	def run(self):
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
		self.start_fire()
		plan = []
		#print("Start grid")
		#print(self.maze.grid)
		while self.agent != self.end:
			plan = self.generate_plan(self.strategy, plan)
			if not plan:
					break
			plan = self.execute_plan(self.strategy, plan)
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
			plan, _ =  self.maze.Marco_Polo_Future(self.agent, self.end)
		elif strategy == constants.STRATEGY_5:
			plan, _ = self.maze.CTF(self.agent, self.end)
		return plan

	def execute_plan(self, strategy, plan):
		times = 0
		if strategy == constants.STRATEGY_1:
				times = len(plan) - 1
		elif strategy == constants.STRATEGY_2 or strategy == constants.STRATEGY_5:
				times = 1
		elif strategy == constants.STRATEGY_3 or strategy == constants.STRATEGY_4:
				times = self.maze.dist_to_nearest_fire(plan[0])
		elif strategy == constants.STRATEGY_5:
				times = self.maze.dist_to_nearest_fire(plan[0])
				if times <= 1:
					#print("Switching")
					_ , best_first_step = self.simulation()
					plan, _ = self.maze.Astar(best_first_step, self.end)
					if best_first_step != self.agent:
						plan.insert(0, self.agent)
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
				#if self.maze.grid[curr[0]][curr[1]] == constants.FIRE or (self.maze.dist_to_nearest_fire(curr)<=1 and (y,x) != self.end):
					#print(f'{plan}:resetting')
					#plan = []
			else:
				break
			new_grid = self.advance_fire()
			#print(new_grid)
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
				plan, _ = self.maze.ADAAC(self.agent, self.end)
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
		neighbors = self.maze.get_neighbors(self.agent,self.maze.is_open)
		for n in list(neighbors):
				p = self.get_probability(n)
				if p > best[0]:
						best = (p, n)
		return best

	def get_probability(self, start: (int, int)):
		success = 0
		for i in range(5):
			sim = copy.deepcopy(self)
			sim.strategy = constants.STRATEGY_1
			sim.agent = start
			sim.maze.grid[start[0]][start[1]] = constants.AGENT
			sim.advance_fire()
			if sim.run():
					success += 1
		return (success / 5)


	def Sims(self):
		neighbors = self.maze.get_neighbors(self.agent, self.maze.is_open)
		forks = []
		i = 0
		while True:
			try:
				neighbor = next(neighbors)
				forks.append(experiment(self.maze.dim, self.maze.p, self.q, self.agent, self.end, constants.STRATEGY_2))
				forks[i].maze.grid = self.maze.clone_grid()
				old_y, old_x = forks[i].agent
				new_y, new_x = neighbor
				forks[i].maze.grid[old_y][old_x] = constants.OPEN
				forks[i].maze.grid[new_y][new_x] = constants.AGENT
				forks[i].agent = neighbor
				forks[i].start = neighbor
				forks[i].maze.fireloc = self.maze.fireloc #THIS WILL NEED TO CHANGE IF STRAT 3
				forks[i].switch = True
				i = i + 1
			except StopIteration:
				break
		success_rates = [0, 0, 0, 0]
		for i, fork in enumerate(forks):
			maze_start_state = fork.maze.clone_grid()
			agent_start_state = fork.agent
			for j in range(21):
				success_rates[i] += fork.man_run()
				fork.maze.grid = maze_start_state.clone_grid()
				fork.agent = agent_start_state
		highest_sr = 0
		highest_sr_index = 0
		for i, sr in enumerate(success_rates):
			if sr >= highest_sr:
				highest_sr = sr
				highest_sr_index = i
		return forks[highest_sr_index].maze.Astar(forks[highest_sr_index].start, self.end)

#exp = experiment(10, .2, .2, (0, 0), (9, 9), 4)
#exp.man_run()



#exp = experiment(5,.2,.2,(0,0),(4,4),3)
#print(exp.simulation())
