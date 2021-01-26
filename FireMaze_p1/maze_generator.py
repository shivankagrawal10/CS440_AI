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

    def check_valid(self,coordinate):
        if(coordinate[0]<0 or coordinate[1]<0)or(coordinate[0]>=self.dim or coordinate[1]>=self.dim):
            return -1
        elif(self.maze[coordinate[0]][coordinate[1]]==1):
            return 1
        return 0

    def DFS(self,start:(int,int),end:(int,int)):
        stack=[]
        visited={}
        stack.insert(0,start)
        visited[start]=1
        while stack :
            curr=stack.pop(0)
            if(curr==end):
                return 1
            moves=[(curr[0]+1,curr[1]),(curr[0]-1,curr[1]),(curr[0],curr[1]+1),(curr[0],curr[1]-1)]
            for move in moves:
                check=self.check_valid(move)
                if(check==0):
                    if(move not in visited):
                        stack.insert(0,move)
                        visited[move]=1
            print(stack)
        return 0

    def BFS(self,start:(int,int),end:(int,int)):
        stack=[]
        visited={}
        stack.insert(0,start)
        visited[start]=1
        while stack :
            curr=stack.pop(0)
            if(curr==end):
                return 1
            moves=[(curr[0]+1,curr[1]),(curr[0]-1,curr[1]),(curr[0],curr[1]+1),(curr[0],curr[1]-1)]
            for move in moves:
                check=self.check_valid(move)
                if(check==0):
                    if(move not in visited):
                        stack.append(move)
                        visited[move]=1
            print(stack)
        return 0    
first=maze()
first.make_maze(5,0.2)
print(first.maze)
first.BFS((0,0),(first.dim-1,first.dim-1))