import numpy as np
import math
import warnings

warnings.filterwarnings("error")

def w_tplus(w, x, y, alpha):
	#print("W", w)
	#print("X", x)
	#print(dL(w,x,y))
	#input()
	return w - alpha * dL(w, x, y)

def dL(w, x, y):
	dot = np.dot(w, x)
	#print("DOT",dot)
	#input()
	ret = (sigmoid(dot)-y)*x
	#ret = (2)*(y - (1*sigmoid(dot)))*(-1)*(1)*(sigmoid(dot))*(1 - sigmoid(dot))*x
	#print("DL",ret) 
	return ret

def sigmoid(z):
	coeff = None
	try:
		coeff = math.e**(-z)
	except:
		if z > 0:
			print("too big")
			return 1

		if z < 0:
			print("too little")
			return 0
	#print("Coeff",coeff)
	#print(1 / (1 + coeff))
	return 1 / (1 + coeff)

def L(w, x, y):
	dot = np.dot(w, x)
	return abs(y - (1*sigmoid(dot)))*255



