import gradient as gr
import numpy as np
import matplotlib.pyplot as plt
import patch as p
import gray as g
from numpy.random import default_rng
from multiprocessing import Process,Manager
import multiprocessing as mp
#for saving image
from PIL import Image
class improved_agent:

	def __init__(self, img_path, alpha):
		self.img_path = img_path
		self.alpha = alpha
		self.rng = default_rng()
		self.clr_img = np.array(plt.imread(self.img_path))
		self.new_img = np.empty((1,1))
		self.gray_img = g.color_to_gray(self.img_path)
		self.red_model = self.build_model(0)
		self.green_model = self.build_model(1)
		self.blue_model = self.build_model(2)
		self.rows = 0
		self.cols = 0
		self.rows_complete = 1

		self.threads = 40

	def build_model(self, r_g_b_ind):
		self.rows, self.cols, _ = self.clr_img.shape
		w_t = np.zeros(10)
		w_tplus = np.full(10, 1)
		i = 1
		L_inc = 0
		losses = []
		chang = []
		time = []
		s = 0
		while i < 1000:
			#calculating new weights
			w_t = np.array(w_tplus)
			r = self.rng.integers(1, high=self.rows-1)
			c = self.rng.integers(1, high=(self.cols // 2))
			#print("Chose", r, c)
			x = p.build_patch(self.gray_img, r, c)
			#x = [np.max(a) for a in x ]
			x = [((np.max(a) - 128) / 255) for a in x ]
			#x = [(np.array(x).mean() - 128) / 255]
			#print(x)
			x.insert(0, 1)
			#print(x)
			x = np.array(x)
			y = self.clr_img[r,c,r_g_b_ind]
			y = (y - 128) / 255
			#print(w_t)
			w_tplus = gr.w_tplus(w_t, x, y, self.alpha)
			#print(w_tplus)
			#print(w_tplus - w_t)
			if (w_tplus - w_t).sum() == 0:
				print("No change")
			#else:
			#	print((w_tplus - w_t).sum())
			#input()

			#checking loss
			r = self.rng.integers(1, high=self.rows-1)
			c = self.rng.integers(1, high=(self.cols // 2))
			x = p.build_patch(self.gray_img, r, c)
			#x = [np.max(a) for a in x ]
			x = [((np.max(a) - 128) / 255) for a in x ]
			#x = [(np.array(x).mean() - 128) / 255]
			x.insert(0, 1)
			x = np.array(x)
			y = self.clr_img[r,c,r_g_b_ind]
			y = (y - 128) / 255
			old_loss = gr.L(w_t, x, y)
			new_loss = gr.L(w_tplus, x, y)
			s += new_loss
			if i % 300000 == 0:
				s /= 300000
				losses.append(s)
				s = 0
				print((losses[-1] * 255) + 128)
				print(w_tplus)
				#self.alpha *= .9
			if i % 300000 == 0 and i >= 600000:
				time.append(i / 300000)
				chang.append(losses[-1])
				#plt.scatter(time, chang)
				#plt.show()
			i += 1
			#print("Iteration", i, "complete.")
		print("Done building model", r_g_b_ind)
		input()
		return w_tplus

	def run(self):
		self.new_img = self.clr_img.copy()
	
		self.rows, self.cols, _ = self.clr_img.shape
		self.div_line = self.cols // 2
		
		self.new_img[:,self.div_line:,:] = self.gray_img[:,self.div_line:,:]
		#plt.imshow(self.new_img)
		#plt.show()
		#print(self.new_img)
		t=[]
		temp = mp.Array("i",self.clr_img.flatten())
		#initializing thread for each core
		for cores in range(self.threads):
			print(cores)
			#t.append(threading.Thread(target=self.thread_color,args=()))
			t.append(Process(target=self.thread_color,args=(self.rows_complete,temp)))
			t[-1].start()
			self.rows_complete += 1
		for thr in t:
			thr.join()
		self.clr_img = np.array(temp,np.uint8).reshape(self.new_img.shape)
		plt.imshow(self.new_img)
		plt.show()
		#img = Image.fromarray(self.new_img, 'RGB')
		#img.save("clust_mount_10.jpg")
		return self.clr_img

	
	def thread_color(self,rows_complete,temp):
		#temp_rgb = np.array(temp,np.uint8).reshape(self.new_img.shape)
		while(rows_complete < self.rows-1):
			#temp_rgb = np.array(temp,np.uint8).reshape(self.new_img.shape)
			row = rows_complete
			if row == 0 or row >= self.rows-1:
				break
			rows_complete += self.threads
			col = self.div_line
			while col < self.cols - 1:
				x = p.build_patch(self.gray_img, row, col)
				x = [(np.max(a) - 128)/255 for a in x ]
				x.insert(0, 1)
				x = np.array(x)
				r = int(round(np.dot(self.red_model, x) *255 + 128)) 
				g = int(round(np.dot(self.green_model, x)*255 + 128))
				b = int(round(np.dot(self.blue_model, x)*255 + 128))
				temp [np.ravel_multi_index((row,col,0),(self.rows,self.cols,3))] = abs(r)
				temp [np.ravel_multi_index((row,col,1),(self.rows,self.cols,3))] = abs(g)
				temp [np.ravel_multi_index((row,col,2),(self.rows,self.cols,3))] = abs(b)
				print((r,g,b))
				col += 1
				print("Colored pixel", row, ",", col)
			print("Progress", row / self.rows)
			

	'''
	def run(self):
		
		for row in range(rows):
			if row == 0 or row == rows-1:
				continue
			col = div_line
			while col < cols - 1:
				x = p.build_patch(self.gray_img, row, col)
				x = [(np.max(a) - 128) for a in x ]
				x.insert(0, 1)
				x = np.array(x)
				r = int(round(np.dot(self.red_model, x)))
				g = int(round(np.dot(self.green_model, x)))
				b = int(round(np.dot(self.blue_model, x)))
				self.clr_img[row][col] = np.array([r,g,b])
				col += 1
				print("Colored pixel", row, ",", col)
			print("Progress", row / rows)
		plt.imshow(self.clr_img)
		plt.show()
		return self.clr_img
	'''


#impr_agent = improved_agent("mountains.jpg", 1)
impr_agent = improved_agent("small_test.jpg", 1)
impr_agent.run()