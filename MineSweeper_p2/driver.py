import Minefield as mf
import agent as ag

class MS_Game:

	def __init__(self, dim: int, strategy: int, num_hints=2, p=.3, seed=-1):
		self._minefield = mf.Minefield(dim, p)
		starting_hints = self.get_starting_hints(num_hints)
		print("Starting hints are", starting_hints)
		self._agent = ag.agent(self._minefield, strategy, starting_hints)

	def get_open_cells(num_hints):
		open_cells = []
		for i in range(dim):
			for j in range(dim)
				if self._minefield.query((i, j), constants.OPEN):
					clue = self.gen
					open_cells.append((i, j))
		num_hints = min(num_hints, len(open_cells))
		return np.random.choice(open_cells, size=num_hints, replace=False)

	def get_starting_hints(num_hints)
		open_cells = self.get_open_cells(num_hints)
		hints = []
		for open_cell in open_cells:
			hints.append((open_cell, self._minefield.gen_clue(open_cell)))
		return hints

	def run(self):
		self._minefield.print_minefield()
		self._agent.play_game()


driver = MS_Game(5, 1)

driver.run()


