import numpy as np
import random
import heapq
import math
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

    def Astar(self,start:(int,int),end:(int,int)):
        heap = []
        visited = {}
        heapq.heappush(heap,(0,start))
        visited[start] = 1
        temp = 0
        while heap:
            curr = heapq.heappop(heap)[1]
            moves = [(curr[0]+1,curr[1]),(curr[0],curr[1]+1),
                     (curr[0]-1,curr[1]),(curr[0],curr[1]-1)]
            for move in moves:
                if(move[0]<0 or move[1]<0 or move[0]>=self.dim or move[1]>=self.dim):
                    continue
                if(self.maze[move[0],move[1]] == 1):
                    continue
                if(move not in visited):
                    dist_traveled = move[0]+move[1]
                    dist_goal = math.sqrt((end[0]-move[0])**2 + (end[1]-move[1])**2)
                    heapq.heappush(heap,(dist_traveled+dist_goal,move))
                    visited[move] = 1
                if(move[0]==end[0] and move[1] == end[1]):
                    print('Found Solution')
                    return
            temp +=1
            if temp%200 == 0:
                print(heap[0])
        print('No Solution')

