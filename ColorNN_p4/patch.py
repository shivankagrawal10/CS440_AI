import numpy as np
import matplotlib.pyplot as plt
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
    return np.array(patches)

#returns a 9-item list of pixel values that describe a patch.
def build_patch(img, r, c):
    vectors = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]])
    coords = vectors+[r,c]
    return img[coords[:,0],coords[:,1]]

def build_big_patch(img,r,c):
    x = img[r-2:r+3,c-2:c+3,:]
    return x.reshape(25,3)

#returns indices for six most similar patches
def similar_patch(patch, patches):
    norms = np.linalg.norm(patch - patches, axis=2)
    print(norms)
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

