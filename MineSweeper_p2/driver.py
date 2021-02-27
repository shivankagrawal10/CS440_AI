import Minefield as mf
import agent as ag
import constants
import numpy as np

class MS_Game:

	def __init__(self, dim: int, strategy: int, num_hints=2, p=.3, seed=-1):
		self._minefield = mf.Minefield(dim, p)
		starting_hints = self.get_starting_hints(num_hints)
		print("Starting hints are", starting_hints)
		self._agent = ag.agent(self._minefield, strategy, starting_hints)

	def get_open_cells(self, num_hints):
		open_cells = []
		for i in range(self._minefield.dim):
			for j in range(self._minefield.dim):
				if self._minefield.query((i, j), constants.OPEN):
					open_cells.append((i, j))
		num_hints = min(num_hints, len(open_cells))
		return self.randomchoice(open_cells, num_hints)

	def randomchoice(self, open_cells, num_hints):
		selection = []
		for i in range(num_hints):
			index = np.random.randint(0, high=(len(open_cells)-1))
			selection.append(open_cells.pop(index))
		return selection

	def get_starting_hints(self, num_hints):
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

