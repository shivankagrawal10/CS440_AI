import maze_generator as mg
import matplotlib.pyplot as plt
import timeit
import constants
'''
def problem1(dim,p):
    first = mg.maze(dim,p)

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
            first = mg.maze(dim,i)
            success+=first.DFS((0,0),(first.dim-1,first.dim-1))
        i+=0.01
        print(float(success/times))
        Y.append(float(success/times))
    plt.scatter(X,Y) #Remember to to lable this graph    
    plt.show()

def problem3():
    dim = 50
    times = 50
    p = 0
    X = []
    Y = []
    while p <= 1:
        a_sum = 0
        b_sum = 0
        for x in range(times):
            first = mg.maze(dim,p)
            a_sum += first.Astar((0,0),(dim-1,dim-1))
            b_sum += first.BFS((0,0),(dim-1,dim-1))
        X.append(p)
        Y.append(b_sum/times-a_sum/times)
        p+=.01
    plt.scatter(X,Y)
    plt.show()
  
def problem4.5():
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
            if exp1.maze.Astar((0,0),(dim-1,dim-1)) == constants.NO_PATH or exp1.maxe.Astar(fire_coords,(0,0))==constants.NO_PATH):
                continue
            success_1+=exp1.run()
            x+=1
        x = 0
        while x < 50:
            exp2 = experiment(dim, .3,q, (0, 0), (dim-1, dim-1), 2)
            fire_coords = exp2.start_fire()
            if exp2.Astar((0,0),(dim-1,dim-1)) == constants.NO_PATH or exp2.Astar(fire_coords,(0,0))==constants.NO_PATH):
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
            

problem3()
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
import matplotlib.pyplot as plt
X=[]
Y=[]
for x in range(800,1500,50):
    first=mg.maze(x,.3)
    start = timeit.default_timer()
    first.Astar((0,0),(first.dim-1,first.dim-1))
    stop = timeit.default_timer()
    print(f'dim: {x},Time: {stop - start}')
    X.append(x)
    Y.append(stop-start)
    #plt.plot(X,Y)
    #plt.draw()
    #plt.pause(0.01)
plt.plot(X,Y)
plt.show()
'''
