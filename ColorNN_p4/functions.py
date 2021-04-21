import numpy as np
import matplotlib.pyplot as plt


def color_to_bw(img):
    flat_img = np.array(img.reshape(-1, 3))
    for pix in range(len(flat_img)):
        r, g, b = flat_img[pix]
        grey = .21 * r + .72 * g + .07 * b
        flat_img[pix] = grey
    return flat_img.reshape(img.shape)


