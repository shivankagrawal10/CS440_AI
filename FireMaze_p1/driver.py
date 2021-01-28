import maze_generator as mg
import matplotlib.pyplot as plt
import timeit

def problem1(dim,p):
    first=mg.maze()
    first.make_maze(dim,p)

def problem2():
    X=[]
    Y=[]
    dim=70
    times=50
    i=0
    while i<=1:
        success=0
        X.append(i)
        for x in range(times):
            first.make_maze(dim,i)
            success+=first.DFS((0,0),(first.dim-1,first.dim-1))
        i+=0.01
        print(float(success/times))
        Y.append(float(success/times))
    plt.scatter(X,Y) #Remember to to lable this graph    
    plt.show()

def problem3():
    dim = 50
    times = 10
    p = 0
    first = mg.maze()
    X = []
    Y = []
    while p <= 1:
        a_sum = 0
        b_sum = 0
        for x in range(times):
            first.make_maze(dim,p)
            a_sum += first.Astar((0,0),(dim-1,dim-1))
            b_sum += first.BFS((0,0),(dim-1,dim-1))
        X.append(p)
        Y.append(b_sum/times-a_sum/times)
        p+=.01
    plt.scatter(X,Y)
    plt.show()

problem3()


'''
input vs time

import matplotlib.pyplot as plt
X=[]
Y=[]
for x in range(700,801,5):
    first.make_maze(x,.2)
    start = timeit.default_timer()
    first.DFS((0,0),(first.dim-1,first.dim-1))
    stop = timeit.default_timer()
    print(f'dim: {x},Time: {stop - start}')
    X.append(x)
    Y.append(stop-start)
    plt.plot(X,Y)
    plt.draw()
    plt.pause(0.01)
plt.show()
'''
