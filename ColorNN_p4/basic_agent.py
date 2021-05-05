#for handling image rgb array
import numpy as np
#for visualizing image
import matplotlib.pyplot as plt
#to create 9x1 vector of grayscale values surrounding center
import patch as p
#convert image to gray
import gray as g
#reduce image to k colors
import k_means
#allows single core threading
import threading
#allows multiprocessor threading
from multiprocessing import Process,Manager
import multiprocessing as mp
#for saving image
from PIL import Image

#from numba import jit, cuda

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
		self.threads = 1

	def run(self):
		self.img = np.array(plt.imread(self.img_path))
		self.new_img = self.img.copy()
		#print(self.img)
		#img = Image.fromarray(self.new_img, 'RGB')
		#self.new_img = np.array(img.resize((40,80)))
		#self.new_img.save("small_test.png")
		#plt.imshow(self.new_img)
		#plt.show()
		clustered = k_means.k_means(5,self.new_img)
		
		self.five_color = clustered.run() #fc.five_color(self.img_path) 
		self.clustered_img = clustered.clustered_rbg
		self.gray_img = g.color_to_gray(self.img_path)
		#self.gray_img = g.color_to_gray(self.img_path)
		self.rows, self.cols, _ = self.clustered_img.shape
		self.div_line = self.cols // 2
		self.patches = p.patchify(self.gray_img)
		#print(self.patches)
		self.new_img[:,self.div_line:,:] = self.gray_img[:,self.div_line:,:]
		#indexes = np.random.choice(np.arrange(self.patches.shape[0]),1000)
		#self.patches = self.patches[indexes]
		#plt.imshow(self.new_img)
		#plt.show()
		#print(self.new_img)
		t=[]
		temp = mp.Array("i",self.new_img.flatten())
		#print(self.new_img.dtype)
		#initializing thread for each core
		for cores in range(self.threads):
			print(cores)
			#t.append(threading.Thread(target=self.thread_color,args=()))
			pr=Process(target=self.thread_color,args=(self.rows_complete,temp))
			t.append(pr)
			pr.start()
			self.rows_complete += 1
		for thr in t:
			thr.join()
		self.new_img = np.array(temp,np.uint8).reshape(self.new_img.shape)
		plt.imshow(self.new_img)
		plt.show()
		img = Image.fromarray(self.new_img, 'RGB')
		img.save("clust_mount_final.jpg")
		return self.new_img

	#@jit(target="cuda")
	#@jit(nopython=True, parallel=True)
	def thread_color(self,rows_complete,temp):
		#temp_rgb = np.array(temp,np.uint8).reshape(self.new_img.shape)
		while(rows_complete < (self.rows-1)):
			#temp_rgb = np.array(temp,np.uint8).reshape(self.new_img.shape)
			row = rows_complete
			if row == 0 or row >= (self.rows-1):
				break
			rows_complete += self.threads
			col = self.div_line
			while col < self.cols - 1:
				patch = p.build_patch(self.gray_img, row, col)
				six_sim = p.similar_patch(patch, self.patches)
				new_clr = p.color_lookup(self.clustered_img, six_sim)
				#print(type(patch))
				#print(patch)
				#print(six_sim)
				#print(new_clr)
				#print(self.new_img[row,col-1,:])
				#self.new_img[row,col,:] = new_clr
				#temp_rgb [row,col,:] = new_clr
				for i in range(3):
					temp [np.ravel_multi_index((row,col,i),(self.rows,self.cols,3))] = new_clr[i]
				#print(self.new_img[row,col,:])
				col += 1
				#print("Colored pixel", row, ",", col)
			#print(self.new_img[row,:,:])
			#temp = mp.Array("i",temp_rgb.flatten())
			print(f"Row: {row} | Progress {row / self.rows}")
		#print(self.new_img)
		
b_agent = basic_agent('mountains.jpg')
#b_agent = basic_agent('small_test.jpg')
b_agent.run()