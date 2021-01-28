import numpy as np
import random
import heapq
import math
class maze():
    def __init__(self,dim : int, p : float):
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
            visited[curr]=1
            if(curr==end):
                return 1
            moves=[(curr[0]+1,curr[1]),(curr[0]-1,curr[1]),
                   (curr[0],curr[1]+1),(curr[0],curr[1]-1)]
            for move in moves:
                check=self.check_valid(move)
                if(check==0):
                    if(move not in visited):
                        stack.insert(0,move)
                        
        return 0

    def Astar(self,start:(int,int),end:(int,int)):
        heap = []
        visited = {}
        fringed = {}
        heapq.heappush(heap,(0,start))
        fringed[start] = 1
        while heap:
            curr = heapq.heappop(heap)[1]
            visited[curr] = 1
            moves = [(curr[0]+1,curr[1]),(curr[0],curr[1]+1),
                     (curr[0]-1,curr[1]),(curr[0],curr[1]-1)]
            for move in moves:
                check=self.check_valid(move)
                if(check==0):
                    if(move not in fringed):
                        fringed[move] = 1
                        dist_traveled = move[0]+move[1]
                        dist_goal = math.sqrt((end[0]-move[0])**2 + (end[1]-move[1])**2)
                        heapq.heappush(heap,(dist_traveled+dist_goal,move))    
                if(move==end):
                    return(len(visited))
        return(len(visited))

    def BFS(self,start:(int,int),end:(int,int)):
        queue=[]
        #solution=[]
        visited={}
        ancestors = {}
        queue.insert(0,start)
        #solution.append(f'{start}')
        ancestors[start]=1
        while queue :
            curr=queue.pop(0)
            visited[curr] = 1
            if(curr==end):
                #rem=solution[0]
                #solution.append(f'{rem},{move}')
                #print(f'Shortest BFS path: {solution[0]}')
                ptr = curr
                while not ptr  == 1:
                    #print(ptr)
                    ptr = ancestors[ptr]
                return len(visited)
            moves=[(curr[0]+1,curr[1]),(curr[0]-1,curr[1]),
                   (curr[0],curr[1]+1),(curr[0],curr[1]-1)]
            for move in moves:
                check=self.check_valid(move)
                if(check==0):
                    if(move not in ancestors):
                        ancestors[move]=curr
                        queue.append(move)
                        #rem=solution[0]
                        #solution.append(f'{rem},{move}')
                        
            #solution.pop(0)
        return len(visited)    
#first= maze(25,0.2)
#print(first.maze)
#print(first.BFS((0,0),(first.dim-1,first.dim-1)))
#print(first.Astar((0,0),(first.dim-1,first.dim-1)))
