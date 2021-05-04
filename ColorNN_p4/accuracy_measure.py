import matplotlib.pyplot as plt
import numpy as np

def accuracy_measure(o_img_path,g_img_path):
    orig_img = np.array(plt.imread(o_img_path))
    gen_img = np.array(plt.imread(g_img_path))
    shape = orig_img.shape
    orig_img = orig_img[:,shape[1]//2:,:]
    gen_img = gen_img[:,shape[1]//2:,:]
    diff = (gen_img - orig_img)**2 /255
    print(f"red: {np.average(diff[:,:,0])}, green: {np.average(diff[:,:,1])}, blue: {np.average(diff[:,:,2])}")

accuracy_measure("mountains.jpg","clust_mount_10.jpg")