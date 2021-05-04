import numpy as np
import math
import warnings

warnings.filterwarnings("error")

def w_tplus(w, x, y, alpha):
	return w - alpha * dL(w, x, y)

def dL(w, x, y):
	dot = np.dot(w, x)
	sig = sigmoid(dot)
	return (2)*(y + .5 - (1*sig))*(-1)*(1)*(sig)*(1 - sig)*x

def sigmoid(z):
	coeff = None
	try:
		coeff = math.e**(-z)
	except:
		if z > 0:
			return 1

		if z < 0:
			return 0
	return 1 / (1 + coeff)

def L(w, x, y):
	dot = np.dot(w, x)
	return abs(y + .5 - (1*sigmoid(dot)))

def quad(x):
	quad = [i**2 for i in x]
	for i in range(len(x)):
		j = i + 1
		while j < len(x):
			quad.append(x[i] * x[j])
			j += 1
	return np.array(quad)



