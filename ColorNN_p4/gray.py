import numpy as np
import matplotlib.pyplot as plt

def color_to_gray(img_path):
	clr_img = plt.imread(img_path)
	flat_img = np.array(clr_img.reshape(-1, 3))
	for pix in range(len(flat_img)):
		r, g, b = flat_img[pix]
		grey = .21 * r + .72 * g + .07 * b
		flat_img[pix] = grey
	return flat_img.reshape(clr_img.shape)