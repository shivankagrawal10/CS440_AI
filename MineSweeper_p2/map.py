import cell_status as cs
import cell_rep as cp

class map:

	def __init__(self, d: int, hints: [((int, int), int)]):
		self.d = d
		self._grid = []
		#SET UP COMPLETELY COVERED MAP
		for i in range(d):
			row = []
			for j in range(d):
				num_hidden = len(self.get_neighbor_coords((i, j)))
				new_cell = cp.cell(cs.Cell_Status.COVERED, None, 0, 0, num_hidden)
				row.append(new_cell)
			self._grid.append(row)
		#PROCESS HINTS
		for hint in hints:
			i, j = hint[0]
			clue = hint[1]
			cell = self._grid[i][j]
			cell.set_status(cs.Cell_Status.SAFE)
			cell.set_clue(clue)

		#UPDATE KNOWLEDGE BASE
		for i in range(d):
			for j in range(d):
				cell = self._grid[i][j]
				neighbors = self.get_neighbors((i, j))
				for neighbor in neighbors:
					if neighbor.get_status() is cs.Cell_Status.SAFE:
						cell.set_num_safe(cell.get_num_safe() + 1)
						cell.set_num_hidden(cell.get_num_hidden() - 1)

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

my_map = map(5, [((2, 2), 1)])
my_map.print_map()

