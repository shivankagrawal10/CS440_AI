import numpy as np
import random
import constants

class Map:
    def __init__(self, dim):
        self.grid = self.create_grid(dim)
        self.target_loc = self.get_target_loc(dim)
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

    def get_target_loc(self, dim):
        i = np.random.randint(0, high=dim)
        j = np.random.randint(0, high=dim)
        return (i, j)

    def print_map(self):
        printable = ""
        for i in range(self.dim):
            for j in range(self.dim):
                printable += str(self.grid[i][j]) + " "
            printable += "\n"
        print(printable)

    def query(self, cell):
        answer = None
        terrain = self.get_terrain(cell)
        m_dist = abs(cell[0] - self.target_loc[0]) + abs(cell[1] - self.target_loc[1])
        within_diamond = m_dist <= 5
        if cell == self.target_loc:
            p = random.random()
            if terrain == constants.flat:
                if p < .1:
                    answer = False
                else:
                    answer = True
            elif terrain == constants.hilly:
                if p < .3:
                    answer = False
                else:
                    answer = True
            elif terrain == constants.forested:
                if p < .7:
                    answer = False
                else:
                    answer = True
            elif terrain == constants.maze_of_caves:
                if p < .9:
                    answer = False
                else:
                    answer = True
        else:
            answer = False
        return (answer, within_diamond)

    def get_terrain(self, cell):
        i, j = cell[0],cell[1]
        return self.grid[i][j]

    def move_target(self):
        vectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        t = self.target_loc
        moves = [(v[0] + t[0], v[1] + t[1]) for v in vectors]
        valid_moves = []
        for move in moves:
            if move[0] < self.dim and move[0] >= 0 and move[1] < self.dim and move[1] >= 0:
                valid_moves.append(move)
        i = np.random.randint(0, high=len(valid_moves))
        self.target_loc = valid_moves[i]
