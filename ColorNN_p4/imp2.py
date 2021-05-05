import gradient as gr
import numpy as np
import matplotlib.pyplot as plt
import patch as p
import gray as g
from numpy.random import default_rng
import math

class improved_agent:

	def __init__(self, img_path, minalpha, maxalpha, epochs):
		self.img_path = img_path
		self.minalpha = minalpha
		self.maxalpha = maxalpha
		self.epochs = epochs
		self.rng = default_rng()
		self.clr_img = np.array(plt.imread(self.img_path))
		self.gray_img = g.color_to_gray(self.img_path)
		self.red_model = self.build_model(0)
		self.green_model = self.build_model(1)
		self.blue_model = self.build_model(2)

	def build_model(self, r_g_b_ind):
		rows, cols, _ = self.clr_img.shape
		w_t = np.zeros(55)
		w_tplus = np.zeros(55)
		for i in range(55):
			w_tplus[i] =  10 * self.rng.random() - 5
			if w_tplus[i] == 0:
				w_tplus[i] = 1
		i = 0
		losses = []
		min_loss = 1
		s = 0
		e = 0
		runs = 0
		while i < 10000000:
			#calculating new weights
			w_t = np.array(w_tplus)
			r = self.rng.integers(1, high=rows-1)
			c = self.rng.integers(1, high=(cols // 2))
			patch = p.build_patch(self.gray_img, r, c)
			#x = [np.max(a) for a in patch]
			x = [((np.max(a) - 128) / 255) for a in patch]
			x.insert(0, 1)
			#x = np.array(x)
			x = gr.quad(x)
			y = self.clr_img[r][c][r_g_b_ind]
			y = (y - 128) / 255
			alpha = self.minalpha + (1/2) * (self.maxalpha - self.minalpha) * (1 + np.cos((e/self.epochs) * math.pi))
			w_tplus = gr.w_tplus(w_t, x, y, alpha)

			if (w_tplus - w_t).sum() == 0:
				print("No change")
			#else:
			#	print((w_tplus - w_t).sum())
			#input()

			#checking loss
			r = self.rng.integers(1, high=rows-1)
			c = self.rng.integers(1, high=(cols // 2))
			patch = p.build_patch(self.gray_img, r, c)
			x = [((np.max(a) - 128) / 255) for a in patch]
			#x = [((np.max(a) - 128) / 255) for a in x ]
			x.insert(0, 1)
			x = gr.quad(x)
			#x = np.array(x)
			y = self.clr_img[r][c][r_g_b_ind]
			y = (y - 128) / 255
			loss = gr.L(w_tplus, x, y)
			#print(loss)
			s += loss
			if e == self.epochs:
				s /= self.epochs
				losses.append(s)
				s = 0
				e = 0
				print(losses[-1])
				print(w_tplus)
				if min_loss > losses[-1]:
					min_loss = losses[-1]
					i = -1
				#self.alpha *= .999
			i += 1
			e += 1
			runs += 1
			#print("Iteration", i, "complete.")
		print("Done building model", r_g_b_ind)
		return w_tplus

	def run(self):
		rows, cols, _ = self.clr_img.shape
		div_line = cols // 2
		print(self.red_model)
		print(self.green_model)
		print(self.blue_model)
		input()
		for row in range(rows):
			if row == 0 or row == rows-1:
				continue
			col = div_line
			while col < cols - 1:
				patch = p.build_patch(self.gray_img, row, col)
				x = [(np.max(a) - 128) / 255 for a in patch]
				#x = [((np.max(a) - 128) / 255) for a in x ]
				x.insert(0, 1)
				#x = np.array(x)
				x = gr.quad(x)
				r = int(128 + 255 * (gr.sigmoid(np.dot(self.red_model, x)) - .5))
				g = int(128 + 255 * (gr.sigmoid(np.dot(self.green_model, x)) - .5))
				b = int(128 + 255 * (gr.sigmoid(np.dot(self.blue_model, x)) - .5))
				#if (row % 10 == 0):
				#	print(r)
				#	print(g)
				#	print(b)
				#	input()
				self.clr_img[row][col] = np.array([r,g,b])
				col += 1
				print("Colored pixel", row, ",", col)
			print("Progress", row / rows)
		plt.imsave("imp_mount.jpg", self.clr_img)
		plt.imshow(self.clr_img)
		plt.show()
		return self.clr_img

impr_agent = improved_agent("mountains.jpg", .01, 2, 200000)
impr_agent.run()