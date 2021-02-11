import firemaze as mg
import firemaze_runner as mr
import matplotlib.pyplot as plt
import timeit
import numpy as np
import constants

def problem1(dim, p, q):
    maze = mg.maze(dim, p, q)
    print(maze.grid)

def problem2():
    X = []
    Y = []
    dim = 70
    times = 100
    i = 0
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
    plt.xlabel("Obstacle Density P") 
    plt.ylabel("Probability that S can be reached from G")
    plt.show()

def problem3():
    dim = 50
    times = 100
    p = 0
    X = []
    Y = []
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
    plt.xlabel("Obstacle Density P")
    plt.ylabel("Average Number of Nodes Explored by BFS - Average Number of Nodes Explored By A*")
    plt.show()
 
def problem45():
    dim = 50
    times = 50
    q = 0
    X = []
    Y1 = []
    Y2 = []
    while q <= 1:
        success_1 = 0
        success_2 = 0
        x = 0
        while x < 50:
            exp1 = experiment(dim, .3,q, (0, 0), (dim-1, dim-1), 1)
            fire_coords = exp1.start_fire()
            if exp1.maze.Astar((0,0),(dim-1,dim-1)) == constants.NO_PATH or exp1.maxe.Astar(fire_coords,(0,0))==constants.NO_PATH:
                continue
            success_1+=exp1.run()
            x+=1
        x = 0
        while x < 50:
            exp2 = experiment(dim, .3,q, (0, 0), (dim-1, dim-1), 2)
            fire_coords = exp2.start_fire()
            if exp2.Astar((0,0),(dim-1,dim-1)) == constants.NO_PATH or exp2.Astar(fire_coords,(0,0))==constants.NO_PATH:
                continue
            success_1+=exp2.run()
            x+=1
        X.append(q)
        Y1.append(success_1/times)
        Y2.append(success_2/times)
        q+=.01
    plt.scatter(X,Y1)
    plt.scatter(X,Y2)
    plt.show()  

def problem4():
    X = ['DFS', 'BFS', 'A*']
    Y = [0, 0, 0]
    for i in range(3):
        dim = 100
        step = 500
        p = .3
        q = 0
        begin = (0, 0)
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
                print("Solved dim", dim, "in", stop - start, "with", i)
                Y[i] = dim
                dim += step
    ypos = np.arrange(len(X))
    plt.xticks(ypos, X)
    plt.bar(ypos, Y)
    plt.xlabel('Search Method')
    plt.ylabel('Largest Dimension Solved in Under a Minute')
    plt.show()

def problem6():
    dim = 25
    p = .3
    q = 0
    trials = 20
    start = (0, 0)
    end = (dim - 1, dim - 1)
    X = []
    Y1 = []
    Y2 = []
    Y3 = []
    Y4 = []
    while q <= 1:
        y = [0, 0, 0]
        for x in range(trials):
            while True: 
                exp1 = mr.experiment(dim, p, q, start, end, 1)
                solvable = exp1.maze.DFS(start, end)
                if solvable:
                    break
            while True: 
                exp2 = mr.experiment(dim, p, q, start, end, 2)
                solvable = exp2.maze.DFS(start, end)
                if solvable:
                    break
            while True: 
                exp3 = mr.experiment(dim, p, q, start, end, 3)
                solvable = exp3.maze.DFS(start, end)
                if solvable:
                    break
            #while True: 
             #   exp4 = mr.experiment(dim, p, q, start, end, 4)
              #  solvable = exp4.maze.DFS(start, end)
               # if solvable:
                #    break
            success_1 = exp1.man_run()
            if success_1:
                y[0] += 1
            success_2 = exp2.man_run()
            if success_2:
                y[1] += 1   
            success_3 = exp3.man_run()
            if success_3:
                y[2] += 1
            #success_4 = exp4.man_run()
            #if success_4:
             #   y[3] += 1
        X.append(q)
        Y1.append(y[0] / trials)
        Y2.append(y[1] / trials)
        Y3.append(y[2] / trials)
        #Y4.append(y[3] / trials)
        q += .01

    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, c=c, s=s)
    plt.scatter(X, Y1, label = 'Strategy 1')
    plt.scatter(X, Y2, label = 'Strategy 2')
    plt.scatter(X, Y3, label = 'Strategy 3')
    #plt.scatter(X, Y4, label = 'Strategy 4')
    plt.xlabel('Flammability Quotient ')
    plt.ylabel('Average Strategy Success Rate')
    plt.show()

            
#problem1(5, .2, 0)
#problem2()
#problem3()
#problem4()
#problem6()

def problem_6():
    dim = 15
    p = .3
    trials = 10
    start = (0, 0)
    end = (dim - 1, dim - 1)
    avg = [0, 0, 0, 0]
    fig, ax = plt.subplots()
    i = 0
    for strategy, color in [(1, 'tab:blue'), (2, 'tab:orange'), (3, 'tab:green'), (4, 'tab:red')]:  #(5, 'tab:black')
        q = 0
        X = []
        Y = []
        while q <= 1:
            num_success = 0
            for x in range(trials):
                success = False
                if strategy == 1:
                    while True: 
                        exp1 = mr.experiment(dim, p, q, start, end, 1)
                        solvable = exp1.maze.DFS(start, end)
                        if solvable:
                            break
                    success = exp1.man_run()
                elif strategy == 2:
                    while True: 
                        exp2 = mr.experiment(dim, p, q, start, end, 2)
                        solvable = exp2.maze.DFS(start, end)
                        if solvable:
                            break
                    success = exp2.man_run()
                elif strategy == 3:
                    while True: 
                        exp3 = mr.experiment(dim, p, q, start, end, 3)
                        solvable = exp3.maze.DFS(start, end)
                        if solvable:
                            break
                    success = exp3.man_run()
                elif strategy == 4:
                    print(x)
                    while True: 
                        exp4 = mr.experiment(dim, p, q, start, end, 4)
                        solvable = exp4.maze.DFS(start, end)
                        if solvable:
                            break
                    success = exp4.man_run()
                #elif strategy == 5:
                 #   while True: 
                  #      exp5 = mr.experiment(dim, p, q, start, end, 5)
                   #     solvable = exp4.maze.DFS(start, end)
                    #    if solvable:
                     #       break
                    #success = exp5.man_run()
                if success:
                    num_success += 1
            Y.append(num_success / trials)
            X.append(q)
            q += .01
        ax.scatter(X, Y, c=color, label=strategy, alpha=.5)
        print("Finished strategy", strategy)
        avg[i] = sum(Y) / trials
        i += 1
    #plt.scatter(X, Y4, label = 'Strategy 4')
    plt.xlabel('Flammability Quotient ')
    plt.ylabel('Average Strategy Success Rate')
    ax.legend()
    ax.grid(True)
    plt.show()
    print(avg)

problem_6()
'''

# ASTAR (2300)
#BFS (2500)
# DFS(1000)
#input vs time
x=1000
first=mg.maze(x,.3)
start = timeit.default_timer()
first.DFS((0,0),(first.dim-1,first.dim-1))
stop = timeit.default_timer()
print(f'dim: {x},Time: {stop - start}')
'''
#import matplotlib.pyplot as plt
#X=[]
#Y=[]
#for x in range(800,1500,50):
#    first=mg.maze(x,.3)
 ### stop = timeit.default_timer()
    #print(f'dim: {x},Time: {stop - start}')
    #X.append(x)
   # Y.append(stop-start)
    #plt.plot(X,Y)
    #plt.draw()
    #plt.pause(0.01)
#plt.plot(X,Y)
#plt.show()

