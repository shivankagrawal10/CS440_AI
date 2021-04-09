import agent_smith as agent
import _map_smith as m
import numpy as np

def test(trials, dim):
	avg1 = 0
	avg2 = 0
	avg3 = 0
	avg4= 0
	for t in range(trials):
		my_map = m.Map(dim)
		drop = get_drop_point(dim)
		agent1 = agent.Agent(dim, 1, my_map, drop,False)
		agent2 = agent.Agent(dim, 2, my_map, drop,False)
		agent3 = agent.Agent(dim, 3, my_map, drop,False)
		agent4 = agent.Agent(dim, 4, my_map, drop,False)
		ag1 = agent1.run()
		ag2 = agent2.run()
		ag3 = agent3.run()
		ag4 = agent4.run()
		avg1 += ag1
		avg2 += ag2
		avg3 += ag3
		avg4 += ag4
		print(t)
	avg1 /= trials
	avg2 /= trials
	avg3 /= trials
	avg4 /= trials
	print("Average for agent 1:", avg1)
	print("Average for agent 2:", avg2)
	print("Average for agent 3:", avg3)
	print("Average for agent 4:", avg4)
def get_drop_point(dim):
    i = np.random.randint(0, high=dim)
    j = np.random.randint(0, high=dim)
    return (i, j)

test(100, 10)
