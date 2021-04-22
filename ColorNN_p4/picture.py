import numpy as np
import matplotlib.pyplot as plt
import functions

img1 = plt.imread('mountains.jpg')
#img1 = plt.imread('scenery.jpg')
#img1 = plt.imread('dog.jpg')
plt.imshow(img1)
plt.show()

print(img1.shape)
print(img1)

bw = functions.color_to_bw(img1)
flat = img1.reshape(-1,3)
#plt.imshow(flat.reshape(img1.shape))
plt.imshow(bw)
plt.show()

