import numpy as np
import random
class maze():

    def make_maze(self,dim : int, p : float):
        self.maze=np.zeros((dim,dim))
        for i in range(dim):
            for j in range(dim):
                if (not i == 0 and j == 0) and (not i == dim-1 and not j == dim-1)
                    and random() <= p:
                    self.maze[i][j] = 1
        print(self.maze)

first=maze()
first.make_maze(2,2)
