import numpy as np
import random
import heapq
import math
import constants
import matplotlib.pyplot as plt
import matplotlib as mat

#The maze class represents a maze our agent is trying to traverse.
#Since the evolving shape of a maze is determined by its dimension (dim), 
#flammability rate (q), and obstacle density (p), our maze object stores each.
#The state of the maze is represented as a dim x dim grid of ints. Specifically,
#open cells are represented as 0s, blocked cells are represented as 1s, fire cells
#are represented as 2s, and a cell containing our agent is represented as a 3.
#For convenience, our maze object also stores the goal cell (end) and a list of the cells
#currently on fire (fireloc).

class maze:

	#The maze constructor.
	#@param Takes in an int for the maze's dimensions (dim), a float for the obstacle density (p),
	#and a float for the flammability rate (q).

	def __init__(self, dim: int, p: float, q: float,seed=-1):
		self.dim = dim
		self.end = (dim-1,dim-1)
		self.p = p
		self.q = q 
		self.seed = seed
		self.grid = self.make_grid(dim, p)
		self.fireloc=[]
		
	#Helper method for creating a grid. After generating the base grid with the help of numpy's zeros method,
	#for every cell in the grid, we generate a random number, and if the number is less than or equal to the 
	#obstacle density, we the cell is blocked. The start cell and end cell are set to open before the grid is
	#returned.
	#@param Takes in an int for the maze's dimensions (dim) and a float for the obstacle density (p).
	#@return Returns a numpy array representing the initial state of the maze.

	def make_grid(self, dim: int, p: float):
		if(self.seed != -1):
			rg = random.Random(self.seed)
		else:
			rg = random.Random()
		grid = np.zeros((dim, dim))
		for i in range(dim):
			for j in range(dim):
				if rg.random() <= p:
					grid[i][j] = constants.BLOCKED
		grid[0][0] = constants.OPEN
		grid[dim - 1][dim - 1] = constants.OPEN
		return grid

	#DFS is an implementation of the depth-first search algorithm.
	#The algorithm runs as follows:
		#Load the starting cell into the fringe.
		#While the fringe is not empty, pop the top cell off of the fringe.
		#Mark this cell as visited, and if this cell is the one to which we're looking for a path, return True.
		#Otherwise, get the four (cardinal direction) neighbors of this cell.
		#For each of these neighbors, if they haven't been visited or added to the fringe, add them to the fringe.
		#If the fringe empties, return False.
	#@param Take in an int-int tuple (start) representing the cell the search starts from, and an int-int tuple (end) 
	#representing the cell to which a path is sought.
	#@return Returns True if a path is found and False otherwise.

	def DFS(self, start: (int, int), end: (int, int)):
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

	#BFS is an implemetation of the breadth-first search algorithm.
	#The algorithm runs as follows:
		#Load the starting cell into the fringe.
		#While the fringe is not empty, do the following:
			#Dequeue the cell at the front of the fringe.
			#Mark this cell as visited, and if this cell is the one to which we're looking for a path, return a tuple storing the path to this cell
			#and the number of cells visited during the search.
			#Otherwise, get the four (cardinal direction) neighbors of this cell.
			#For each of these neighbors, if they haven't been visited or added to the fringe, enqueue them in the fringe and mark the current
			#cell as their predecessor.
		#If the fringe empties, return a tuple storing an empty list (to indicate there is no path) and the number of cells visited during the search.
	#@param Take in an int-int tuple (start) representing the cell the search starts from, and an int-int tuple (end) 
	#representing the cell to which a path is sought.
	#@return Returns a list of int-int tuples representing the cells that comprise the path and an int representing the number of cells visited.

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
		return ([], len(visited))

	#Astar is an implementation of the A* algorithm.
	#A* uses the following heurstic:
	#Let the priority of a cell be equal to the number of steps taken to get to the cell plus the euclidean distance from this cell to the end cell.
	#The algorithm runs as follows:
		#Load the starting cell into the fringe with priority 0, a cost of 0 to reach it, and an undefined predecessor.
		#While the fringe is not empty, do the following:
			#Remove the cell with the smallest priority from the fringe.
			#If this cell has been visited, go to the next iteration.
			#Otherwise do the following:
				#Mark this cell as visited and record its predecessor.
				#If this cell is the one to which we're seeking a path, return a tuple storing the path to this cell
				#and the number of cells visited during the search.
				#Otherwise, do the follwing:
					#Get the four (cardinal direction) neighbors of this cell.
					#For each of these neighbors, if they haven't been visited, calculate the priority of the neighbor and add a tuple
					#to the fringe storing that neighbor's priority, and another tuple storing the number of steps taken to reach the neighbor,
					#the neighbor, and the neighbor's predecessor, which is the cell most recently removed from the fringe.
		#If the fringe empties, return a tuple storing an empty list (to indicate there is no path) and the number of cells visited during the search.
	#@param Take in an int-int tuple (start) representing the cell the search starts from, and an int-int tuple (end) 
	#representing the cell to which a path is sought.
	#@return Returns a list of int-int tuples representing the cells that comprise the path and an int representing the number of cells visited.

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
		return ([], len(visited))

	#Marco_Polo_Prob is an implementation of our own custom search algorithm.
	#Our algorithm uses the following heuristic:
	#Let the priority of a cell be equal to the product of 1 less the probability that a path from this cell
	#to the end cell can be successfully traversed and the sum of the number of steps taken to reach this cell and
	#the euculidean distance from this cell to the end cell less the distance from this cell to the nearest fire cell.
	#The algorithm runs as follows:
		#Load the starting cell into the fringe with priority 0, a cost of 0 to reach it, and an undefined predecessor.
		#While the fringe is not empty, do the following:
			#Remove the cell with the smallest priority from the fringe.
			#If this cell has been visited, go to the next iteration.
			#Otherwise do the following:
				#Mark this cell as visited and record the its predecessor.
				#If this cell is the one to which we're seeking a path, return a tuple storing the path to this cell
				#and the number of cells visited during the search.
				#Otherwise, do the follwing:
					#Get the four (cardinal direction) neighbors of this cell.
					#For each of these neighbors, if they haven't been visited, calculate the priority of the neighbor and add a tuple
					#to the fringe storing that neighbor's priority, and another tuple storing the number of steps taken to reach the neighbor,
					#the neighbor, and the neighbor's predecessor, which is the cell most recently removed from the fringe.
		#If the fringe empties, return a tuple storing an empty list (to indicate there is no path) and the number of cells visited during the search.
	#@param Take in an int-int tuple (start) representing the cell the search starts from, and an int-int tuple (end) 
	#representing the cell to which a path is sought.
	#@return Returns a list of int-int tuples representing the cells that comprise the path and an int representing the number of cells visited.

	def Marco_Polo(self, start : (int, int), end : (int, int)):
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
								dist_to_fire = self.dist_to_nearest_fire(neighbor)
								priority = move_cost + self.get_dist_to(end, neighbor) - dist_to_fire
								heapq.heappush(fringe, (priority, (move_cost, neighbor, curr)))
						except StopIteration:
							break
		return ([], len(visited))

	def Marco_Polo_Prob(self, start : (int, int), end : (int, int),neighbor_prob={} ):
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
								dist_to_fire = self.dist_to_nearest_fire(neighbor)
								try:
									priority = (1-neighbor_prob[neighbor])*(move_cost + self.get_dist_to(end, neighbor) - dist_to_fire)
									#priority = ((self.get_fire_prob(neighbor)*self.dim)+(move_cost + self.get_dist_to(end, neighbor) - dist_to_fire))
								except:	
									priority = (self.get_fire_prob(neighbor)+1)*(move_cost + self.get_dist_to(end, neighbor) - dist_to_fire)
									#priority = move_cost + self.get_dist_to(end, neighbor) - dist_to_fire
								heapq.heappush(fringe, (priority, (move_cost, neighbor, curr)))
						except StopIteration:
							break
		return ([], constants.NO_PATH)

	#Helper method to generate an animation showing the movement of our agent and the fire 
	#within a maze.

	def maze_visualize(self, agent, grid,show):
		cmap = mat.colors.LinearSegmentedColormap.from_list("", ["skyblue","gray","red","white"])
		plt.imshow(grid,cmap)
		plt.draw()
		if(show==0):
			plt.pause(.5)
		elif(show==1):
			plt.pause(3)
		elif(show==2):
			plt.pause(0.1)
			plt.clf()
		elif(show==3):
			plt.pause(.3)
			plt.clf()
	#Helper method that finds and returns the fire cell nearest to a given position
	#@param Takes an int-int tuple (curr) representing the cell for which we wish to find the nearest fire cell.
	#@return Returns an int-int tuple representing the nearest fire cell.
	def nearest_fire(self, curr:(int, int)):
		return min(self.fireloc, key = lambda x: abs(x[1] - curr[1]) + abs(x[0] - curr[0]))

	#Helper method that finds and returns the manhattan distance from a given cell to the
	#nearest fire celll.
	#@param Takes an int-int tuple (curr) representing the cell for which we wish to find the manhattan distance to the nearest fire cell.
	#@return Returns an int representing the manhattan distance from the given cell to the nearest fire cell.

	def dist_to_nearest_fire(self, curr: (int, int)):
		fire = self.nearest_fire(curr)
		dist = abs(fire[1] - curr[1]) + abs(fire[0] - curr[0])
		return dist

	#Helper method to find if a given coordinate is a cell within a maze's grid or not.
	#@param Takes an int-int tuple (coordinate) representing a coordinate.
	#@return Returns True if the coordinate is a cell within the maze's grid and False otherwise.
		
	def valid_cell(self, coordinate: (int, int)):
		if ((coordinate[0] < 0 or coordinate[1] < 0) 
		or (coordinate[0] >= self.dim or coordinate[1] >= self.dim)):
			return False
		else:
			return True

	#Helper method to find if a given coordinate is an open cell within a maze's grid or not.
	#@param Takes an int-int tuple (coordinate) representing a coordinate.
	#@return Returns True if the coordinate is an open cell within the maze's grid and False otherwise.

	def is_open(self, coordinate: (int, int)):
		valid_cell = self.valid_cell(coordinate)
		y, x = coordinate
		if valid_cell and self.grid[y][x] != constants.BLOCKED and self.grid[y][x] != constants.FIRE:
			return True
		else:
			return False

	#Helper method to find if a given coordinate is a fire cell within a maze's grid or not.
	#@param Takes an int-int tuple (coordinate) representing a coordinate.
	#@return Returns True if the coordinate is a fire cell within the maze's grid and False otherwise.

	def on_fire(self, coordinate: (int, int)):
		valid_cell = self.valid_cell(coordinate)
		y, x = coordinate
		if valid_cell and self.grid[y][x] == constants.FIRE:
			return True
		else:
			return False 

	#Helper method to find the neighboring cells for a given cell that meet some condition.
	#@param Takes an int-int tuple (curr) representing a cell and a function (predicate) that determines if a condition is met.
	#@returns Returns a lazy-iterator of tuples that represent neighboring cells that meet the condition.

	def get_neighbors(self, curr : (int, int), predicate):
		x = curr[1]
		y = curr[0]
		neighbors = filter(predicate, [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)])
		return neighbors

	#Helper method to find the euclidean distance from a given start cell to a given end cell.
	#@param Takes an int-int tuple (end) representing the end cell and another int-int tuple (start) representing the start cell.
	#@return Returns a float representing the calculated euclidean distance from the start cell to the end cell.

	def get_dist_to(self, end : (int, int), start : (int, int)):
		goal_x = end[1]
		goal_y = end[0]
		start_x = start[1]
		start_y = start[0]
		euclid_dist = math.sqrt((goal_y - start_y) ** 2 + (goal_x - start_x) ** 2)
		return euclid_dist

	#Helper method to build a list representing the path from some starting cell to a given end cell.
	#The method back-tracks through a dictionary of predecessors in order to construct this list.
	#@param Takes an int-int tuple (end) representing the cell for which a path is sought and a dictionary of cells (predecessors)
	#where the keys are cells and the values are their predecessors.
	#@return Returns a list of int-int tuples representing a path from some start cell to a given end cell.

	def build_path(self, end : (int, int), predecessors):
		path = [end]
		prev = predecessors[end]
		while prev != constants.UNDEFINED:
			path.insert(0, prev)
			prev = predecessors[prev]
		return path

	#Helper method that clones a grid, which represents a state of the maze.
	#@return Returns a numpy array representing the clone.

	def clone_grid(self):
		clone = np.zeros((self.dim, self.dim))
		for i in range(self.dim):
			for j in range(self.dim):
				clone[i][j] = self.grid[i][j]
		return clone

	#Helper method to calculate the probability that a given cell has of catching on fire.
	#@param Takes an int-int tuple (cell) representing a cell.
	#@return Returns a float representing the probability that the cell has of catching on fire.

	def get_fire_prob(self, cell : (int, int)):
		neighbors = self.get_neighbors(cell, self.on_fire)
		k = 0
		while True:
			try:
				_ = next(neighbors)
				k = k + 1
			except StopIteration:
				break
		prob = 1 - (1 - self.q) ** k
		return prob
