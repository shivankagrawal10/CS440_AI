import cell_status as cs
import cell_rep as cp

class Map:

	def __init__(self, d: int, hints: [((int, int), int)]):
		self.d = d
		self._grid = []
		self.covered = set()
		self.safes = set()
		self.mines = set()
		#SET UP COMPLETELY COVERED MAP
		for i in range(d):
			row = []
			for j in range(d):
				num_hidden = len(self.get_neighbor_coords((i, j)))
				new_cell = cp.cell(cs.Cell_Status.COVERED, None, 0, 0, num_hidden, (i, j))
				row.append(new_cell)
				self.covered.add((i, j))
			self._grid.append(row)
		#PROCESS HINTS
		for hint in hints:
			self.covered.remove(hint[0])
			self.safes.add(hint[0])
			i, j = hint[0]
			clue = hint[1]
			cell = self._grid[i][j]
			cell.set_status(cs.Cell_Status.SAFE)
			cell.set_clue(clue)
			neighbors = self.get_neighbors((i, j))
			for neighbor in neighbors:
				neighbor.set_num_safe(neighbor.get_num_safe() + 1)
				neighbor.set_num_hidden(neighbor.get_num_hidden() - 1)

	def get_neighbor_coords(self, coordinate: (int, int)):
		vectors = [(-1, -1),(-1, 0),(-1, 1),
					(0, -1),       (0, 1),
					(1, -1), (1, 0), (1, 1)]
		neighbor_coords = []
		for vector in vectors:
			candidate_i = coordinate[0] + vector[0] 
			candidate_j = coordinate[1] + vector[1]
			if candidate_i >= 0 and candidate_i < self.d and candidate_j >= 0 and candidate_j < self.d:
				neighbor_coords.append((candidate_i, candidate_j))
		return neighbor_coords
						
	def get_neighbors(self, coordinate: (int, int)):
		neighbor_coords = self.get_neighbor_coords(coordinate)
		neighbors = []
		for cood in neighbor_coords:
			neighbors.append(self._grid[cood[0]][cood[1]])
		return neighbors

	def print_map(self):
		realized_grid = []
		for i in range(self.d):
			row = []
			for j in range(self.d):
				cell = self._grid[i][j]
				status = cell.get_status()
				symbol = None
				if status == cs.Cell_Status.COVERED:
					symbol = '?'
				elif status == cs.Cell_Status.MINE:
					symbol = 'x'
				elif status == cs.Cell_Status.SAFE:
					symbol = str(cell.get_clue())
				row.append(symbol)
			realized_grid.append(row)
		for i in range(self.d):
			realized_grid[i] = " ".join(realized_grid[i])
		realized_grid = "\n".join(realized_grid)
		print(realized_grid)

	def get_cell(self, coord: (int, int)):
		if coord[0] >= 0 and coord[0] < self.d and coord[1] >= 0 and coord[1] < self.d:
			return self._grid[coord[0]][coord[1]]
		else:
			return None


