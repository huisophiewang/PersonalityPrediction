import math
import numpy as np
from numpy.linalg import inv

from utilities import LABELS
from utilities import replace_nan



def sigmoid(x, beta):
    z = np.dot(x, beta)[0]
    prob = 1.0 / (1.0 + np.exp(-z))
    return prob



def train(train_data, y_col, iterations=100):
    n = data.shape[0]
    
    train_x = train_data[:, [1,2,3]]
    train_x = np.insert(train_x, 0, 1, axis=1)
    train_y = np.array([train_data[:, y_col]]).transpose() # numpy 1d array transpose, use [[]]
    prob_y = np.zeros((n, 1))
    
    p = train_x.shape[1]
    beta = np.zeros((p, 1))
    

    lik = 0.0
    prev_lik = 0.0
    # Newton Ralphon update (matrix form) 
    # http://sites.stat.psu.edu/~jiali/course/stat597e/notes2/logit.pdf

    # w - diagonal matrix of weights 
    w = np.zeros((n, n))
    for i in range(n):
        prob_y[i] = sigmoid(train_x[i], beta)
        w[i,i] = prob_y[i]
    #print w
    print prob_y
    print train_y - prob_y

    # Hessian Matrix  
    h = np.dot(np.transpose(train_x), np.dot(w, train_x))      
    #h -= 0.0001*np.identity(p)
    #print h
         
    # update beta
#     diff = (train_y-prob_y)
#     print diff.shape
#     delta = np.dot(np.transpose(train_x), diff)
#     print delta
#     beta += np.dot(inv(h), delta)
#     print beta
    
#     # log likelihood
#     for i in range(n):
#         z = np.dot(train_x[i], beta)
#         lik += train_y[i]*z - math.log(1 + math.exp(z))      
#     print lik
     
#     if lik - prev_lik < 0.000001:
#         break
#     else:
#         prev_lik = lik
    
        
        
        
if __name__ == '__main__':
    fp = r"data\matrix_data\all_wifi_features.csv"
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x_cols = [1,2,3]
    y_col = 4
    replace_nan(data, y_col)
    
#     fp = r"data.txt"
#     data = np.genfromtxt(fp, delimiter=" ", dtype=float)
#     print data
# #     x_cols = [1,2,3]
# #     y_col = 4
    
    train(data, y_col)
    
    
    