import gradient as gr
import numpy as np
import matplotlib.pyplot as plt
import patch as p
import gray as g
from numpy.random import default_rng
import math
from PIL import Image

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
		min_loss = 1
		s = 0
		e = 0
		while i < 2500000:
			#calculating new weights
			w_t = np.array(w_tplus)
			r = self.rng.integers(1, high=rows-1)
			c = self.rng.integers(1, high=(cols // 2))
			patch = p.build_patch(self.gray_img, r, c)
			x = [int(np.max(a)) for a in patch]
			x.insert(0, 1)
			x = gr.quad(x)
			x = [((a - (255**2/2)) / 255**2) for a in x]
			x = np.array(x)
			y = self.clr_img[r][c][r_g_b_ind]
			y = (y - 128) / 255
			alpha = self.minalpha + (1/2) * (self.maxalpha - self.minalpha) * (1 + np.cos((e/self.epochs) * math.pi))
			w_tplus = gr.w_tplus(w_t, x, y, alpha)

			#checking loss
			r = self.rng.integers(1, high=rows-1)
			c = self.rng.integers(1, high=(cols // 2))
			patch = p.build_patch(self.gray_img, r, c)
			x = [int(np.max(a)) for a in patch]
			x.insert(0, 1)
			x = gr.quad(x)
			x = [((a - (255**2/2)) / 255**2) for a in x]
			x = np.array(x)
			y = self.clr_img[r][c][r_g_b_ind]
			y = (y - 128) / 255
			loss = gr.L(w_tplus, x, y)
			#print(loss)
			s += loss
			if e == self.epochs:
				s /= self.epochs
				if min_loss > s:
					min_loss = s
					i = -1
				print(i)
				print(s)
				s = 0
				e = 0
			i += 1
			e += 1
		print("Done building model", r_g_b_ind)
		return w_tplus

	def run(self):
		rows, cols, _ = self.clr_img.shape
		div_line = cols // 2
		for row in range(rows):
			if row == 0 or row == rows-1:
				continue
			col = div_line
			while col < cols - 1:
				patch = p.build_patch(self.gray_img, row, col)
				x = [int(np.max(a)) for a in patch]
				x.insert(0, 1)
				x = gr.quad(x)
				x = [((a - (255**2/2)) / 255**2) for a in x]
				x = np.array(x)
				r = int(128 + 255 * (gr.sigmoid(np.dot(self.red_model, x)) - .5))
				g = int(128 + 255 * (gr.sigmoid(np.dot(self.green_model, x)) - .5))
				b = int(128 + 255 * (gr.sigmoid(np.dot(self.blue_model, x)) - .5))
				self.clr_img[row][col] = np.array([r,g,b])
				col += 1
				print("Colored pixel", row, ",", col)
			print("Progress", row / rows)
		img = Image.fromarray(self.clr_img, 'RGB')
		img.save(r"imp2_quad.jpg")
		plt.imshow(self.clr_img)
		plt.show()
		return self.clr_img

impr_agent = improved_agent("mountains.jpg", .01, 2, 200000)
impr_agent.run()