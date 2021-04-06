import numpy as np

class Map:
	def __init__(self, dim):
		grid = self.create_grid(dim)

	def create_grid(self, dim):
		grid = np.zeros((dim, dim))
		for i in range(dim):
			for j in range(dim):
				

