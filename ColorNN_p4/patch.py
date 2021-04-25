import numpy as np
import matplotlib.pyplot as plt
import kmeans as k
import copy
from operator import itemgetter

#returns a list of all patches in left side of image
def patchify(img):
	r, c, _ = img.shape
	bound = c // 2
	patches = []
	for row in range(r):
		if row == 0 or row == r-1:
			continue
		for col in range(bound-1):
			if col == 0:
				continue
			patches.append(build_patch(img, row, col))
	return patches

#returns a 9-item list of pixel values that describe a patch.
def build_patch(img, r, c):
	flat_patch = []
	vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
	for v in vectors:
		p_r = v[0] + r
		p_c = v[1] + c
		pix_val = img[p_r][p_c]
		flat_patch.append(pix_val)
	return flat_patch

#returns indices for six most similar patches
def similar_patch(patch, patches):
	patches_np = np.array(patches)
	patch_np = np.array(patch)
	norms = np.linalg.norm(patch_np - patches_np, axis=2)
	patch_norm = []
	for i in range(len(patches)):
		patch_norm.append((norms[i].sum(), i))
	patch_norm.sort()
	six_sim = patch_norm[:6]
	six_sim = [ind for (_, ind) in six_sim]
	return six_sim

#returns color to color pixel
def color_lookup(five_color, patch_ind):
	r, c, _ = five_color.shape
	bound = c // 2
	counts = {}
	for ind in patch_ind:
		row, col = lookup_coord(ind, bound)
		rgb = five_color[row][col]
		clr = (rgb[0], rgb[1], rgb[2])
		if clr in counts:
			counts[clr] += 1
		else:
			counts[clr] = 1
	clr_cnt = list(counts.items())
	clr_cnt.sort(key=itemgetter(1), reverse=True)
	chsn_clr = None
	if len(clr_cnt) > 1 and clr_cnt[0][1] == clr_cnt[1][1]:
		#no majority
		r, c = lookup_coord(patch_ind[0], bound)
		chsn_clr = five_color[r][c]
	else:
		#majority
		chsn_clr = list(clr_cnt[0][0])
	return chsn_clr


#returns row, col coordinate corresponding to flattened index
def lookup_coord(ind, bound):
	row = ind // bound
	col = ind % bound
	return row, col

