import numpy as np
import random
class maze():

    def make_maze(self,dim : int, p : float):
        self.maze=np.zeros((dim,dim))
        for i in range(dim):
            for j in range(dim):
                if random.random() <= p:
                    self.maze[i][j] = 1
        self.maze[0][0] = 0
        self.maze[dim-1][dim-1] = 0
        print(self.maze)

first=maze()
first.make_maze(5,.1)
