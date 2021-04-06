import numpy as np
import random
import constants

class Map:
	def __init__(self, dim):
		self.grid = self.create_grid(dim)
		self.dim = dim

	def create_grid(self, dim):
		grid = np.zeros((dim, dim))
		for i in range(dim):
			for j in range(dim):
				p = random.random()
				if p < constants.flat_cell_prob:
					grid[i][j] = constants.flat
				elif p < constants.hill_cell_prob:
					grid[i][j] = constants.hilly
				elif p < constants.forest_cell_prob:
					grid[i][j] = constants.forested
				elif p < constants.maze_of_caves_prob:
					grid[i][j] = constants.maze_of_caves
		return grid

	def print_map(self):
		printable = ""
		for i in range(self.dim):
			for j in range(self.dim):
				printable += str(int(self.grid[i][j])) + " "

			printable += "\n"
		print(printable)

test = Map(10)
test.print_map()

				

