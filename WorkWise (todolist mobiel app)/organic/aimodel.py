import numpy as np
from sklearn import linear_model


def cost(x):
    m = A.shape[0]
    return 0.5/m * np.linalg.norm(A.dot(x)-b, 2)**2

def grad(x):
    m = A.shape[0]
    return 1/m * A.T.dot(A.dot(x)-b)

def check_grad(x):
    eps = 1e-4
    g = np.zeros_like(x)
    for i in range(len(x)):
        x1 = x.copy()
        x2 = x.copy()
        x1[i] += eps
        x2[i] -= eps
        g[i] = (cost(x1) - cost(x2)) / (2*eps)
    g_grad = grad(x)
    if np.linalg.norm(g - g_grad) > 1e-5:
        print("WARNING :: ERROR GRADIENT FUNCTION")

def gradient_descent(coef_init, learning_rate, iteration):
    coef_lists = [coef_init]
    m = A.shape[0]
    for i in range(iteration):
        coef_new = coef_lists[-1] - learning_rate*grad(coef_lists[-1])
        if np.linalg.norm(grad(coef_new))/len(coef_new) < 0.5: # when to stop GD
         	break
        coef_lists.append(coef_new)
    return coef_lists
#Data
A = [0,5,8,3,6,7,4,9,2,6,5,8,4,7,3,6,5,9,2,6,7,4,8,5,3,6,7,4,9,2,6,5,8,3,6,7,4,9,2,6,5,8,4,7,3,6,5,9,2,6,7,4,8,5,3,6,7,4,9,2,6,5,8,3,6,7,4,9,2,6,5,8,4,7,3,6,5,9,2,6,7,4,8,5,3,6,7,4,9,2,6,5,8,3,6,7,4,9,2,6,5,8,4,7,3,6,5,9]
b = [0,80,75,100,83.33,100,50,88.89,50,50,40,87.5,100,71.43,66.67,66.67,100,66.67,100,16.67,57.14,25,25,60,33.33,100,85.71,75,77.78,50,33.33,60,62.5,100,100,100,50,88.89,50,50,40,87.5,100,71.43,66.67,66.67,100,66.67,100,16.67,57.14,25,25,60,33.33,100,85.71,75,77.78,50,33.33,60,62.5,100,100,100,50,88.89,50,50,40,87.5,100,71.43,66.67,66.67,100,66.67,100,16.67,57.14,25,25,60,33.33,100,85.71,75,77.78,50,33.33,60,62.5,100,100,100,50,88.89,50,50,40,87.5,100,71.43,66.67,66.67,100,66.67]

#Change Dimension
A = np.array([A]).T
b = np.array([b]).T
# Draw data
ones = np.ones_like(A,dtype = np.int8)
A = np.concatenate((A,ones),axis = 1)

#Train Model
lr = linear_model.LinearRegression()
lr.fit(A,b)
#print(lr.coef_[0][0])
#print(lr.intercept_)
coef_init = np.array([[1.],[2.]])
#check_grad(coef_init)
#Gradien descent
learning_rate = 0.0001
iteration = 100
#coef_list = gradient_descent(coef_init, learning_rate, iteration)

#TEST

class get_efficiency:
    def get_eff(self, x):
        try:
            HST = lr.coef_[0][0]*x + lr.intercept_
            return round(HST[0])
        except Exception as e:
            print(e)
