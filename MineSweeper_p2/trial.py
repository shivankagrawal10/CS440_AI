import driver
import time
import matplotlib.pyplot as plt

def runner(dim, trials):
	X = []
	Y1 = []
	p = 0
	#Y2 = []
	while p <= 1:
		g1_avg = 0
		g2_avg = 0
		for i in range(trials):
			time_seed = time.time()
			g1 = driver.MS_Game(dim, 1, p=p, seed=time_seed)
			g2 = driver.MS_Game(dim, 2, p=p, seed=time_seed)
			g1.run()
			g2.run()
			g1_avg += g1.score
			g2_avg += g2.score
			time.sleep(1)
		g1_avg /= trials
		g2_avg /= trials
		X.append(p)
		Y1.append(g2_avg - g1_avg)
		print("Finished dim", p)
		p += .01
	plt.scatter(X,Y1)
	plt.show()


runner(5, 30)

