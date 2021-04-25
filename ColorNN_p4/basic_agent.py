import numpy as np
import matplotlib.pyplot as plt
import patch as p
import kmeans as km
import five_color as fc
import gray as g
import k_means

class basic_agent:

	def __init__(self, img_path):
		self.img_path = img_path

	def run(self):
		clr_img = np.array(plt.imread(self.img_path))
		clustered = k_means.k_means('mountains.jpg')
		five_color = clustered.run() #fc.five_color(self.img_path) 
		gray_img = g.color_to_gray(self.img_path)
		rows, cols, _ = clr_img.shape
		div_line = cols // 2
		patches = p.patchify(gray_img)
		for row in range(rows):
			if row == 0 or row == rows-1:
				continue
			col = div_line
			while col < cols - 1:
				patch = p.build_patch(gray_img, row, col)
				six_sim = p.similar_patch(patch, patches)
				new_clr = p.color_lookup(five_color, six_sim)
				clr_img[row][col] = new_clr
				col += 1
				print("Colored pixel", row, ",", col)
			print("Progress", row / rows)
		plt.imshow(clr_img)
		plt.show()
		return clr_img

b_agent = basic_agent('dog_med.jpeg')
b_agent.run()

