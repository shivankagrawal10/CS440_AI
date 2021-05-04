import numpy as np
import math

def f(w, x):
	return 1 * (((np.arctan(np.dot(w,x)))/math.pi) + .5)

def df(w, x):
	return (-1/math.pi) * (1/(1 + np.dot(w,x)**2)) * x

def dL(w, x, y):
	return ((2 * (y - f(w, x))) * df(w, x))

def w_tplus(w, x, y, alpha):
	return w - (alpha * dL(w,x,y))

def L(w, x, y):
	return abs(y - f(w, x))

