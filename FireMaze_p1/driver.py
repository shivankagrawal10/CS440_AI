first=maze()
n=10**3
'''
for i in range(1,n,5):
    first.make_maze(i,.2)
<<<<<<< HEAD
    #print(first.maze)
    first.DFS((0,0),(first.dim-1,first.dim-1))
'''
=======
    first.DFS((0,0),(first.dim-1,first.dim-1))
'''

'''
input vs time
'''
>>>>>>> 16ec85a17d39457db805d556a8ed94c0199358d9
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
<<<<<<< HEAD
plt.show()

=======
plt.show()
>>>>>>> 16ec85a17d39457db805d556a8ed94c0199358d9
