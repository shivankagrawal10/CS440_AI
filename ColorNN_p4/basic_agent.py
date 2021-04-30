import numpy as np
import matplotlib.pyplot as plt
import patch as p
import gray as g
import k_means
from PIL import Image
	
class basic_agent:	
	def __init__(self, img_path):
		self.img_path = img_path
		self.rows_complete = 1
		self.div_lines = 0
		self.cols = 0
		self.rows = 0
		self.img = np.empty((1,1))
		self.new_img = np.empty((1,1))
		self.clr_img = np.empty((1,1))
		self.gray_img = np.empty((1,1))
		self.five_color = []
		self.patches = []
		#ensures 20 threads, change according to machine
		self.threads = 40

	def run(self,clusters=5):
		self.img = np.array(plt.imread(self.img_path))
		self.new_img = self.img.copy()
		clustered = k_means.k_means(clusters,self.new_img)
		
		self.five_color = clustered.run() 
		self.five_color = np.array(self.five_color).reshape(clusters,3)
		print(self.five_color)
		self.clustered_img = clustered.clustered_rbg
		self.gray_img = g.color_to_gray(self.img_path)
		self.rows, self.cols, _ = self.clr_img.shape
		self.div_line = self.cols // 2
		self.patches = p.patchify(self.gray_img)
		
		self.new_img[:,self.div_line:,:] = self.gray_img[:,self.div_line:,:]
		
		self.color_pixel()
		img = Image.fromarray(self.new_img, 'RGB')
		img.save(f"clust_mount_{len(self.five_color)}.jpg")
		return self.new_img

	def color_pixel(self):
		while(self.rows_complete < self.rows-1):
			row = self.rows_complete
			self.rows_complete +=1
			if row == 0 or row >= self.rows-1:
				break
			col = self.div_line
			while col < self.div_line+20:#self.cols - 1:
				patch = p.build_patch(self.gray_img, row, col)
				six_sim = p.similar_patch(patch, self.patches)
				new_clr = p.color_lookup(self.clust, six_sim)
				
				#print(self.new_img[row,col-1,:])
				#temp = [i for i in self.five_color[0]]
				
				self.new_img[row,col,:] = new_clr #np.array(temp)
				col += 1
				print("Colored pixel", row, ",", col)
			print(f"Row: {row} | Progress {row / self.rows}")
		
b_agent = basic_agent('mountains.jpg')
#b_agent = basic_agent('small_test.jpg')
b_agent.run()



'''
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

'''