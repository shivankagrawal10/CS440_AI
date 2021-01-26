import numpy as np
import random
class maze():

    def make_maze(self,dim : int, p : float):
        self.dim=dim
        self.p=p
        self.maze=np.zeros((dim,dim))
        #random.seed(123)
        for i in range(dim):
            for j in range(dim):
                if random.random() <= p:
                    self.maze[i][j] = 1
        self.maze[0][0]=0
        self.maze[dim-1][dim-1]=0
        #print(self.maze)

    def DFS(self,start:(int,int),end:(int,int)):
        stack=[]
        visited={}
        stack.insert(0,start)
        visited[start]=1
        while stack :
            curr=stack.pop(0)
            if(curr[0]==end[0] and curr[1]==end[1]):
                #print('Found Solution')
                return 1
            for move in range(-1,2,2):
                temp=(curr[0]+move,curr[1]) #needs work
                if(temp[0]<0 or temp[1]<0)or(temp[0]>=self.dim or temp[1]>=self.dim):
                    pass
                elif(self.maze[temp[0]][temp[1]]==1):
                    continue
                else:
                    if(temp not in visited):
                        stack.insert(0,temp)
                        visited[temp]=1
            for move in range(-1,2,2):
                temp=(curr[0],curr[1]+move) #needs work
                if(temp[0]<0 or temp[1]<0)or(temp[0]>=self.dim or temp[1]>=self.dim):
                    pass
                elif(self.maze[temp[0]][temp[1]]==1):
                    continue
                else:
                    if(temp not in visited):
                        stack.insert(0,temp)
                        visited[temp]=1
            #print(stack)
        return 0
