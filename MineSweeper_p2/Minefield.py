import numpy as np
import random
import constants
import matplotlib.pyplot as plt
import matplotlib as mat
import cell_status as cs
import cell_rep as cp
from matplotlib.ticker import MultipleLocator
class Minefield:
    #The minefield constructor.
    #@param Takes in an int for the maze's dimensions (dim),

    def __init__(self, dim: int, p=.3, seed=-1):
        self.dim = dim
        self.p = p
        self.seed = seed
        #Field is array of 1s for mines and 0s for safe
        #use it to get clues for cells and check for cell type + visualization?
        self.num_mines = 0
        self.field = self.make_field(dim, self.p)
        self.set_graph()
        
    #Helper method for creating a grid. After generating the base grid with the help of numpy's zeros method,
    #for every cell in the grid, we generate a random number, and if the number is less than or equal to the 
    #obstacle density, the cell has a mine. 
    #@param Takes in an int for the maze's dimensions (dim) and a float for the obstacle density (p).
    #@return Returns a numpy array representing the initial state of the maze.

    def make_field(self, dim: int, p: float):
        if(self.seed != -1):
            rg = random.Random(self.seed)
        else:
            rg = random.Random()
        grid = np.zeros((dim, dim))
        for i in range(dim):
            for j in range(dim):
                if rg.random() <= p:
                    grid[i][j] = constants.BLOCKED
                    self.num_mines += 1
        return grid

    def get_neighbor_coords(self, coordinate: (int, int)):
        vectors = [(-1, -1),(-1, 0),(-1, 1),
                    (0, -1),       (0, 1),
                    (1, -1), (1, 0), (1, 1)]
        neighbor_coords = []
        for vector in vectors:
            candidate_i = coordinate[0] + vector[0] 
            candidate_j = coordinate[1] + vector[1]
            if candidate_i >= 0 and candidate_i < self.dim and candidate_j >= 0 and candidate_j < self.dim:
                neighbor_coords.append((candidate_i, candidate_j))
        return neighbor_coords

    def gen_clue(self, coordinate: (int, int)):
        neighbor_coords = self.get_neighbor_coords(coordinate)
        mine_count = 0
        for neigbor in neighbor_coords:
            if self.field[neigbor[0]][neigbor[1]] == constants.BLOCKED:
                mine_count += 1
        return mine_count

    def set_graph(self):
        self.extent = (0, self.field.shape[1], self.field.shape[0], 0)
        _, self.ax = plt.subplots()
        self.ax.xaxis.set_major_locator(MultipleLocator(1))
        self.ax.xaxis.tick_top()
        self.ax.yaxis.set_major_locator(MultipleLocator(1))

    #Helper method to generate an animation showing the movement of our agent and the fire 
    #within a maze.

    def maze_visualize(self,show):
        cmap = mat.colors.LinearSegmentedColormap.from_list("", ["white","red"])
        '''
        extent = (0, self.field.shape[1], self.field.shape[0], 0)
        _, ax = plt.subplots()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.xaxis.tick_top()
        ax.yaxis.set_major_locator(MultipleLocator(1))
        '''
        self.ax.imshow(self.field, extent=self.extent,cmap=cmap)
        self.ax.grid(color='black', linewidth=2,which='both')
        #ax.set_frame_on(False)
        #plt.imshow(self.field,cmap,)
        plt.draw()
        if(show==0):
            plt.ion()
            #plt.pause(.5)
        elif(show==1):
            plt.pause(3)
        elif(show==2):
            plt.pause(0.1)
            plt.clf()
        elif(show==3):
            plt.pause(.3)
            plt.clf()

    def print_minefield(self):
        printable = []
        for i in range(self.dim):
            row = self.field[i]
            str_row = []
            for i in range(len(row)):
                str_row.append(str(row[i]))
            printable.append(" ".join(str_row))
        print("\n".join(printable))

    def query(self, coord: (int, int), assertion):
        return self.field[coord[0]][coord[1]] == assertion