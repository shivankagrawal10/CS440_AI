import numpy as np
import random
import heapq
import math
import maze_generator as mg
import constants

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

	def run(self):
		self.start_fire()
		plan = []
		while self.agent != self.end:
			input("Press any key to continue")
			print(self.maze.grid)
			plan = self.advance_agent(self.strategy, plan)
			print("Agent moves to", self.agent)
			if not plan:
				break
			new_grid = self.advance_fire()
			print("New Maze:")
			print(new_grid)
			y, x = self.agent
			if new_grid[y][x] == constants.FIRE:
				break
			self.maze.grid = new_grid
		if self.agent == self.end:
			print("Success")
		else:
			print("Failure")

	def advance_agent(self, strategy, plan):
		if strategy == constants.STRATEGY_1 and not plan:
			plan, _ = self.maze.BFS(self.agent, self.end)
		elif strategy == constants.STRATEGY_2:
			plan, _ = self.maze.BFS(self.agent, self.end)
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
					#print(i, ",", j, "has the following:")
					#print(self.q)
					#print(prob)
					if prob != 0 and random.random() <= prob:
						clone[i][j] = constants.FIRE
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

exp = experiment(5, .2 , 1, (0, 0), (4, 4), 1)
exp.run()


