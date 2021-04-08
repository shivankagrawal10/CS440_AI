import agent
import _map as m
import numpy as np

def test(trials, dim):
	avg1 = 0
	avg2 = 0
	avg3 = 0
	for t in range(trials):
		my_map = m.Map(dim)
		drop = get_drop_point(dim)
		agent1 = agent.Agent(dim, 1, my_map, drop)
		agent2 = agent.Agent(dim, 2, my_map, drop)
		agent3 = agent.Agent(dim, 3, my_map, drop)
		#ag1 = agent1.run()
		#print(ag1)
		#ag2 = agent2.run()
		#print(ag2)
		ag3 = agent3.run()
		print(ag3)
		avg1 += ag1
		avg2 += ag2
		avg3 += ag3
		print(t)
	avg1 /= trials
	avg2 /= trials
	avg3 /= trials
	print("Average for agent 1:", avg1)
	print("Average for agent 2:", avg2)
	print("Average for agent 3:", avg3)
def get_drop_point(dim):
    i = np.random.randint(0, high=dim)
    j = np.random.randint(0, high=dim)
    return (i, j)

test(10, 25)