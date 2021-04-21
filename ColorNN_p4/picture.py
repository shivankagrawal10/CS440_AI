import numpy as np
import matplotlib.pyplot as plt

img1 = plt.imread('dog.jpg')
plt.imshow(img1)


print(img1.shape)
print(img1)

flat = img1.reshape(-1,3)
plt.imshow(flat.reshape(img1.shape))

