import imp2 as i 
import basic_agent as b
import matplotlib.pyplot as plt
import numpy as np
import accuracy_measure as am

def run_agents(img_path, min_alpha, max_alpha, epochs):
	basic = b.basic_agent(img_path)
	improved = i.improved_agent(img_path, min_alpha, max_alpha, epochs)
	final_basic = basic.run()
	final_improved = i.run()
	clr_img = np.array(plt.imread(img_path))
	diff_bas = am.accuracy_measure(img_path, './clust_mount_5.jpg')
	diff_imp = am.accuracy_measure(img_path, './imp2_quad.jpg')
	print("Difference between basic and improved agent:", diff_bas - diff_imp)
	if diff_imp.sum() < diff_bas.sum():
		print("Improved agent wins with score:", diff_imp)
	elif diff_bas.sum() < diff_imp.sum():
		print("Basic agent wins with score:", diff_bas)
	else:
		print("Tie")

run_agents('mountains.jpg', .01, 1, 100000)


