import firemaze as mg
import firemaze_runner as mr
import matplotlib.pyplot as plt
import timeit
import numpy as np
import constants
import random
#generate and print maze
#size dim, obstacle probability p, and fire spread q
def problem1(dim, p, q):
    maze = mg.maze(dim, p, q)
    print(maze.grid)

#generate plot of obstacle density versus success
def problem2():
    X = []
    Y = []
    dim = 100
    times = 100
    i = 0
    #get success for obstacle density (0,1) with .01 step
    while i <= 1:
        success = 0
        X.append(i)
        for x in range(times):
            maze = mg.maze(dim, i, 0)
            found_path = maze.DFS((0,0),(maze.dim - 1, maze.dim - 1))
            if found_path:
                success += 1
        i += 0.01
        Y.append(float(success / times))
    plt.scatter(X, Y)
    plt.title("DFS dim = 100 trials = 100")
    plt.xlabel("Obstacle Density P") 
    plt.ylabel("Probability that S can be reached from G")
    plt.show()

#generate plot of obstacle density p versus nodes explored by BFS - A*
def problem3():
    dim = 60
    times = 100
    p = 0
    X = []
    Y = []
    #get success for obstacle density (0,1) at step .01
    while p <= 1:
        a_sum = 0
        b_sum = 0
        for x in range(times):
            maze = mg.maze(dim, p, 0)
            _ , nodes_A_visits = maze.Astar((0, 0), (dim - 1, dim - 1))
            _ , nodes_B_visits = maze.BFS((0, 0), (dim - 1, dim - 1))
            a_sum += nodes_A_visits
            b_sum += nodes_B_visits
        X.append(p)
        Y.append((b_sum / times) - (a_sum / times))
        p += .01
    plt.scatter(X, Y)
    plt.title("BFS vs A* dim = 60 trials = 100")
    plt.xlabel("Obstacle Density P")
    plt.ylabel("Average Number of Nodes Explored by BFS - Average Number of Nodes Explored By A*")
    plt.show()

#find max dimensions that can be solved in roughly 60 seconds for DFS, BFS, A*
def problem4():
    X = ['DFS', 'BFS', 'A*']
    Y = [0, 0, 0]
    for i in range(3):
        dim = 1000
        step = 300
        p = .3
        q = 0
        begin = (0, 0)
        #loop ends if algorithm takes over 60 seconds and step is <= 1
        #step is added to dimensions if time < 60 else step is cut in half and subtracted from dimension
        while True:
            end = (dim - 1, dim - 1)
            maze = mg.maze(dim, p, q)
            start = timeit.default_timer()
            if i == 0:
                
                solvable = maze.DFS(begin, end)
            elif i == 1:
                solvable, _ = maze.BFS(begin, end)
            else:
                solvable, _ = maze.Astar(begin, end)
            stop = timeit.default_timer()
            if not solvable:
                continue
            if stop - start > 60:
                if step <= 1:
                    break
                else:
                    dim -= step
                    step = int(step / 2)
                    dim += step
            else:
                Y[i] = dim
                dim += step
    ypos = np.arrange(len(X))
    plt.xticks(ypos, X)
    plt.bar(ypos, Y)
    plt.xlabel('Search Method')
    plt.ylabel('Largest Dimension Solved in Under a Minute')
    plt.show()

#generate success rate of strategies for various q at p = .3
def problem_6():
    dim = 25
    p = .3
    qincr= 0.05
    seed = random.randint(0,100)
    trials = 50
    start = (0, 0)
    end = (dim - 1, dim - 1)
    avg = []
    fig, ax = plt.subplots()
    #create scatter for each strategy
    for strategy, color in [(1, 'tab:blue'), (2, 'tab:orange'), (3, 'tab:green')]:
        rg=random.Random(seed)
        #random.seed(seed)
        q = 0
        X = []
        Y = []
        #test q from 0 to 1 at step of .05
        while q <= 1:
            num_success = 0
            for x in range(trials):
                success = False
                while True: 
                    exp = mr.experiment(dim, p, q, start, end, strategy,seed=rg.randint(0,100))
                    fire_coords = exp.start_fire()
                    if exp.maze.DFS(start,end) and exp.maze.DFS(fire_coords,start):
                        break
                success = exp.run(0) 
                if success:
                    num_success += 1
            Y.append(num_success / trials)
            X.append(q)
            q += qincr
        ax.scatter(X, Y, c=color, label=strategy, alpha=1)
        avg.append(sum(Y)/len(Y))
    print(avg)
    plt.xlabel('Flammability Quotient ')
    plt.ylabel('Average Strategy Success Rate')
    ax.legend()
    ax.grid(True)
    plt.show()

problem4()
