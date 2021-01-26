import maze_generator as mg
import matplotlib.pyplot as plt
X=[]
Y=[]
first=mg.maze()
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
plt.scatter(X,Y)    
plt.show()
'''
input vs time

import timeit
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