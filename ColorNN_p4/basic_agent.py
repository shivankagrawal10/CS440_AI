import numpy as np
import matplotlib.pyplot as plt
import patch as p
import kmeans as km
import five_color as fc
import gray as g
import k_means
import threading

class basic_agent:

	def __init__(self, img_path):
		self.img_path = img_path
		self.rows_complete = 1
		self.div_lines = 0
		self.cols = 0
		self.rows = 0
		self.clr_img = np.empty()

	def run(self):
		self.clr_img = np.array(plt.imread(self.img_path))
		clustered = k_means.k_means('mountains.jpg')
		five_color = clustered.run() #fc.five_color(self.img_path) 
		gray_img = g.color_to_gray(self.img_path)
		self.rows, self.cols, _ = clr_img.shape
		#self.cols = cols
		self.div_line = cols // 2
		patches = p.patchify(gray_img)
		#for row in range(rows):
		t=[]
		for cores in range(8):
			t.append( threading.Thread(target=self.thread_color(),args=()) )
			t[-1].start()
		for thr in t:
			thr.join()
		plt.imshow(self.clr_img)
		plt.show()
		return self.clr_img

	def thread_color(self):
		while(self.rows_complete != self.rows-1):
			row = self.rows_complete
			if row == 0 or row == rows-1:
				break
			self.rows_complete += 1
			col = self.div_line
			while col < self.cols - 1:
				patch = p.build_patch(gray_img, row, col)
				six_sim = p.similar_patch(patch, patches)
				new_clr = p.color_lookup(five_color, six_sim)
				clr_img[row][col] = new_clr
				col += 1
				print("Colored pixel", row, ",", col)
			print("Progress", row / rows)

b_agent = basic_agent('dog_med.jpeg')
b_agent.run()

