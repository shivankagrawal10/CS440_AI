import imp2 as i 
import basic_agent as b
import matplotlib.pyplot as plt
import numpy as np

def run_agents(img_path, min_alpha, max_alpha, epochs):
	basic = b.basic_agent(img_path)
	improved = i.improved_agent(img_path, min_alpha, max_alpha, epochs)
	final_basic = basic.run()
	final_improved = i.run()
	clr_img = np.array(plt.imread(img_path))
	rows, cols, _ = clr_img.shape
	div = cols // 2
	basic_performance = 0
	improved_performance = 0
	for row in range(rows):
		if row == 0 or row == rows-1:
			continue
		col = div
		while col < cols-1:
			clr_pix = np.array(clr_img[row][col])
			basic_pix = np.array(final_basic[row][col])
			improved_pix = np.array(final_improved[row][col])
			diff = clr_pix - basic_pix
			diff_b = np.array([i ** 2 for i in diff]).sum()
			diff = clr_pix - improved_pix
			diff_i = np.array([i ** 2 for i in diff]).sum()
			basic_performance += diff_b
			improved_performance += diff_i
			col += 1
	print("Difference between basic and improved agent:", basic_performance - improved_performance)
	if improved_performance < basic_performance:
		print("Improved agent wins with score:", improved_performance)
	elif basic_performance < improved_performance:
		print("Basic agent wins with score:", basic_performance)
	else:
		print("Tie")


