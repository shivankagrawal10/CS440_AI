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
        #print(cell)
        terrain = self.get_terrain(cell)
        if cell == self.target_loc:
            i, j = cell
            if i < 0 or j < 0 or i >= self.dim or j >= self.dim:
                print("Error")
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
        return answer

    def get_terrain(self, cell):
        i, j = cell[0],cell[1]
        #print('hi')
        #print(i)
        #print(j)
        return self.grid[i][j]


#test = Map(10)
#test.print_map()

                

