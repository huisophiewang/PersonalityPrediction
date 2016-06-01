import math
import os
import numpy as np
from numpy.linalg import inv
import statsmodels.api as sm
import pandas
from patsy.highlevel import dmatrices, dmatrix


from utilities import LABELS
from utilities import replace_nan

from sklearn import datasets
from sklearn import svm


# ignore overflow error
np.seterr(over='ignore')

def sigmoid(x, beta):
    z = np.dot(x, beta)[0]
    prob = 1.0 / (1.0 + np.exp(-z))
    return prob



def train(train_data, iterations=100):
    n = train_data.shape[0]
    
    train_x = train_data[:, :-1]
    train_x = np.insert(train_x, 0, 1, axis=1)
    
    train_y = np.array([train_data[:, -1]]).transpose() # numpy 1d array transpose, use [[]]
    prob_y = np.zeros((n, 1))
    
    p = train_x.shape[1]
    beta = np.zeros((p, 1))
    

    prev_lik = float("-inf")
    # Newton Ralphon update (matrix form) 
    # http://sites.stat.psu.edu/~jiali/course/stat597e/notes2/logit.pdf
    for k in range(iterations):
        #print '==========='
        #print "iteration %d: " % k
 
        # w - diagonal matrix of weights 
        w = np.zeros((n, n))
        for i in range(n):
            prob_y[i] = sigmoid(train_x[i], beta)
            w[i,i] = prob_y[i]*(1-prob_y[i])
     
        # Hessian Matrix  
        h = np.dot(np.transpose(train_x), np.dot(w, train_x))      
        #h -= 0.0001*np.identity(p)
        #print h
             
        # update beta
        delta = np.dot(np.transpose(train_x), (train_y-prob_y))
        beta += np.dot(inv(h), delta)
        #print beta
        
        # log likelihood
        lik = 0.0
        for i in range(n):
            z = np.dot(train_x[i], beta)[0]
            #print z
            lik += train_y[i][0]*z - np.log(1 + np.exp(z))     
        #print lik
        
        if lik - prev_lik < 0.000001:
            break

        prev_lik = lik
        
    return beta
    
def get_accuracy(test_data, beta):   
    n = test_data.shape[0]
    test_x = test_data[:, :-1]
    test_x = np.insert(test_x, 0, 1, axis=1)  
    test_y = np.array([test_data[:, -1]]).transpose()   
    
    count = 0.0
    for i in range(n):
        p = sigmoid(test_x[i], beta)
        #print test_x[i]
        #print p
        print test_y[i][0]
        if p >= 0.5:
            predict = 1.0
        else:
            predict = 0.0
        print predict
        if predict == test_y[i][0]:
            count += 1
        
    acc = count / n
    return acc

def my_logit(label):

    fp = r"data\matrix_data\logit\wifi_features_%s.csv" % label
    data = np.genfromtxt(fp, delimiter=",", dtype=float)
    print data.shape
    
    n = data.shape[0]
    m = data.shape[1]
    #fold = 5
    fold = 25
    test_data = np.empty([n/fold, m])
    train_data = np.empty([n-n/fold, m])
    
    
    avg_acc = 0.0
    for j in range(fold):
        print '============'
        print "fold %d" % j
        for i, x in enumerate(data):
            if i%fold == j:
                test_data[i/fold] = data[i]
            else:
                train_data[(i/fold)*(fold-1)+i%fold-1] = data[i]
        print test_data
        beta = train(train_data)
        print beta
        acc = get_accuracy(test_data, beta)
        print "accuracy is: " + str(acc)
        avg_acc += acc
    avg_acc /= fold
    print "average accuracy is: " + str(avg_acc)
        
def logit():
    fp = r"data\matrix_data\logit\wifi_features_extra.csv"
    df = pandas.read_csv(fp)
    y, X = dmatrices('extra ~ len_var + end_time_var + fq_home', data=df)
    mod = sm.Logit(y, X)
    res = mod.fit()
    print res.summary()
    

    

if __name__ == '__main__':
    my_logit("extra")
    
    #logit()
    

    

    
    
    