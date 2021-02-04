import numpy as np
import random
import heapq
import math
import constants

class maze:

	def __init__(self, dim : int, p : float, q : float):
		self.dim = dim
		self.p = p #Probability of blockers
		self.q = q #Flammability factor
		self.grid = np.zeros((dim, dim))
		self.fireloc=[]
		#random.seed(123)
		for i in range(dim):
			for j in range(dim):
				if random.random() <= p:
					self.grid[i][j] = constants.BLOCKED
		self.grid[0][0] = constants.OPEN
		self.grid[dim - 1][dim - 1] = constants.OPEN

	def DFS(self, start : (int,int), end : (int, int)):
		fringe = []
		visited = {}
		fringed = {}
		fringe.append(start)
		fringed[start] = True
		while fringe:
			curr = fringe.pop()
			del fringed[curr]
			visited[curr] = True
			if curr == end:
				return True
			else:
				neighbors = self.get_neighbors(curr, self.is_open)
				while True:
					try:
						neighbor = next(neighbors)
						if neighbor not in visited and neighbor not in fringed:
							fringe.append(neighbor)
							fringed[neighbor] = True
					except StopIteration:
						break        
		return False

	def Astar(self, start : (int, int), end : (int, int)):
		fringe = []
		visited = {}
		predecessors = {}
		heapq.heappush(fringe, (0, (0, start, constants.UNDEFINED)))
		while fringe:
			_, (cost, curr, pred) = heapq.heappop(fringe)
			if curr in visited:
				continue
			else:
				visited[curr] = True
				predecessors[curr] = pred
				if curr == end:
					path = self.build_path(end, predecessors)
					return (path, len(visited))
				else:
					neighbors = self.get_neighbors(curr, self.is_open)
					while True:
						try:
							neighbor = next(neighbors)
							if neighbor not in visited:
								move_cost = cost + 1
								priority = move_cost + self.get_dist_to(end, neighbor)
								heapq.heappush(fringe, (priority, (move_cost, neighbor, curr)))
						except StopIteration:
							break
		return ([], constants.NO_PATH)

	def BFS(self, start : (int, int), end : (int, int)):
		fringe = []
		visited = {}
		fringed = {}
		predecessors = {}
		predecessors[start] = constants.UNDEFINED
		fringe.append(start)
		fringed[start] = True
		while fringe:
			curr = fringe.pop(0)
			del fringed[curr]
			visited[curr] = True
			if curr == end:
				path = self.build_path(end, predecessors)
				return (path, len(visited))
			else:
				neighbors = self.get_neighbors(curr, self.is_open)
				while True:
					try:
						neighbor = next(neighbors)
						if neighbor not in visited and neighbor not in fringed:
							fringe.append(neighbor)
							fringed[neighbor] = True
							predecessors[neighbor] = curr
					except StopIteration: 
						break
		return ([], constants.NO_PATH)

	def ADAAC(self, start : (int, int), end : (int, int)):
		fringe = []
		visited = {}
		predecessors = {}
		heapq.heappush(fringe, (0, (0, start, constants.UNDEFINED)))
		while fringe:
			_, (travel_cost, curr, pred) = heapq.heappop(fringe)
			if curr in visited:
				continue
			else:
				visited[curr] = True
				predecessors[curr] = pred
				if curr == end:
					path = self.build_path(end, predecessors)
					return (path, len(visited))
				else:
					neighbors = self.get_neighbors(curr, self.is_open)
					while True:
						try:
							neighbor = next(neighbors)
							if neighbor not in visited:
								move_cost = cost + 1
								priority = move_cost + self.get_dist_to(end, neighbor) + self.get_fire_cost(neighbor)
								heapq.heappush(fringe, (priority, (move_cost, neighbor, curr))) 
						except StopIteration:
							break
		return ([], constants.NO_PATH)
	
	def Hot_Astar(self, start : (int, int), end : (int, int)):
		'''
		fringe = []
		visited = {}
		predecessors = {}
		heapq.heappush(fringe, (0, (0, start, constants.UNDEFINED)))
		while fringe:
			_, (cost, curr, pred) = heapq.heappop(fringe)
			if curr in visited:
				continue
			else:
				visited[curr] = True
				predecessors[curr] = pred
				if curr == end:
					path = self.build_path(end, predecessors)
					return (path, len(visited))
				else:
					neighbors = self.get_neighbors(curr, self.is_open)
					while True:
						try:
							neighbor = next(neighbors)
							if neighbor not in visited:
								move_cost = cost + 1
								priority = move_cost + self.get_dist_to(end, neighbor)
								heapq.heappush(fringe, (priority, (move_cost, neighbor, curr)))
						except StopIteration:
							break
		return ([], constants.NO_PATH)
		'''
		curr=start
		nei=get_neighbors(curr,self.is_open)
		curr=nearest_fire(curr)
		print(curr)
		return get_neighbors(curr,self.is_open)
	
	def nearest_fire(self,start:(int,int)):
		return min(self.fireloc,key=lambda x: abs(x[1]-start[1])+abs(x[0]-start[0]))

	def valid_cell(self, coordinate):
		if ((coordinate[0] < 0 or coordinate[1] < 0) 
		or (coordinate[0] >= self.dim or coordinate[1] >= self.dim)):
			return False
		else:
			return True

	def is_open(self, coordinate):
		valid_cell = self.valid_cell(coordinate)
		y, x = coordinate
		if valid_cell and self.grid[y][x] != constants.BLOCKED and self.grid[y][x] != constants.FIRE:
			return True
		else:
			return False

	def on_fire(self, coordinate):
		valid_cell = self.valid_cell(coordinate)
		y, x = coordinate
		if valid_cell and self.grid[y][x] == constants.FIRE:
			return True
		else:
			return False 

	def get_neighbors(self, curr : (int, int), predicate):
		x = curr[1]
		y = curr[0]
		neighbors = filter(predicate, [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)])
		return neighbors

	def get_dist_to(self, end : (int, int), start : (int, int)):
		goal_x = end[1]
		goal_y = end[0]
		start_x = start[1]
		start_y = start[0]
		euclid_dist = math.sqrt((goal_y - start_y) ** 2 + (goal_x - start_x) ** 2)
		return euclid_dist

	def build_path(self, end : (int, int), predecessors):
		path = [end]
		prev = predecessors[end]
		while prev != constants.UNDEFINED:
			path.insert(0, prev)
			prev = predecessors[prev]
		return path

	def clone_grid(self):
		clone = np.zeros((self.dim, self.dim))
		for i in range(self.dim):
			for j in range(self.dim):
				clone[i][j] = self.grid[i][j]
		return clone

	def get_fire_prob(self, move : (int, int)):
		neighbors = self.get_neighbors(move, self.on_fire)
		k = 0
		prob = 0
		while True:
			try:
				_ = next(neighbors)
				k = k + 1
			except StopIteration:
				break
		if k != 0:
			prob = 1 - (1 - self.q) ** k
		return prob

#first = maze(100, 0.3)
#print(first.maze)
#dfs = first.DFS((0, 0), (first.dim - 1, first.dim - 1))
#bfs = first.BFS((0, 0), (first.dim - 1, first.dim - 1))
#astar = first.Astar((0,0), (first.dim - 1, first.dim - 1))

#print(dfs)
#print(bfs)
#print(len(bfs[0]))
#print(astar)
#print(len(astar[0]))