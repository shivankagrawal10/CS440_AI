import numpy as np
class maze():

    def make_maze(self,dim : int, p : float):
        self.maze=np.zeros((dim,dim))
        print(self.maze)

first=maze()
first.make_maze(2,2)