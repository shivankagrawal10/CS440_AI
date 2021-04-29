import numpy as np
import matplotlib.pyplot as plt
import patch as p
#import kmeans as km
#import five_color as fc
import gray as g
import k_means
import threading
from multiprocessing import Process

class basic_agent:

	def __init__(self, img_path):
		self.img_path = img_path
		self.rows_complete = 1
		self.div_lines = 0
		self.cols = 0
		self.rows = 0
		self.img = np.empty((1,1))
		self.clr_img = np.empty((1,1))
		self.gray_img = np.empty((1,1))
		self.five_color = []
		self.patches = []
		self.threads = 20

	def run(self):
		_, subp = plt.subplots()
		self.img = np.array(plt.imread(self.img_path))
		clustered = k_means.k_means(5,self.img)
		self.five_color = clustered.run() #fc.five_color(self.img_path) 
		self.clr_img = clustered.clustered_rbg
		self.gray_img = g.color_to_gray(self.img_path)
		self.rows, self.cols, _ = self.clr_img.shape
		#self.cols = cols
		self.div_line = self.cols // 2
		self.patches = p.patchify(self.gray_img)
		#for row in range(rows):
		t=[]
		subp.imshow(self.clr_img)
		plt.draw()
		plt.pause(1)
		for cores in range(self.threads):
			print(cores)
			#t.append(threading.Thread(target=self.thread_color,args=()))
			t.append(Process(target=self.thread_color,args=()))
			t[-1].start()
			self.rows_complete += 1
		for thr in t:
			thr.join()
		#plt.imshow(self.clr_img)
		#plt.show()
		return self.clr_img

	def thread_color(self):
		while(self.rows_complete < self.rows-1):
			row = self.rows_complete
			if row == 0 or row >= self.rows-1:
				break
			self.rows_complete += self.threads
			col = self.div_line
			while col < self.cols - 1:
				patch = p.build_patch(self.gray_img, row, col)
				six_sim = p.similar_patch(patch, self.patches)
				new_clr = p.color_lookup(self.five_color, six_sim)
				#print(new_clr)
				self.clr_img[row,col,:] = new_clr
				col += 1
				#print("Colored pixel", row, ",", col)
				plt.imshow(self.clr_img)
			if(self.rows_complete % self.threads == self.threads-1):
				plt.draw()
				plt.pause(5)
			print(f"Row: {row} | Progress {row / self.rows}")

b_agent = basic_agent('mountains.jpg')
b_agent.run()

