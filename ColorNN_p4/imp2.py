import gradient as gr
import numpy as np
import matplotlib.pyplot as plt
import patch as p
import gray as g
from numpy.random import default_rng

class improved_agent:

	def __init__(self, img_path, alpha):
		self.img_path = img_path
		self.alpha = alpha
		self.rng = default_rng()
		self.clr_img = np.array(plt.imread(self.img_path))
		self.gray_img = g.color_to_gray(self.img_path)
		self.red_model = self.build_model(0)
		self.green_model = self.build_model(1)
		self.blue_model = self.build_model(2)

	def build_model(self, r_g_b_ind):
		rows, cols, _ = self.clr_img.shape
		w_t = np.zeros(10)
		w_tplus = np.full(10, 1)
		i = 1
		while i < 1000000:
			w_t = np.array(w_tplus)
			r = self.rng.integers(1, high=rows-1)
			c = self.rng.integers(1, high=(cols // 2))
			p = p.build_patch(self.gray_img, r, c)
			x = [((np.max(a) - 128) / 255) for a in p ]
