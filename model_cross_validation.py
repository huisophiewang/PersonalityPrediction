import os
import numpy as np
from sklearn import linear_model
from pprint import pprint

def linear_reg(x_train, y_train, x_test, y_test):
    x_train = np.c_[np.ones(len(x_train)), x_train]
    pseudo_inv = np.linalg.inv(np.dot(x_train.T, x_train))
    w = np.dot(np.dot(pseudo_inv, x_train.T), y_train)
    print  w
    x_test = np.c_[np.ones(len(x_test)), x_test]
    test_mse = np.mean((np.dot(x_test, w) - y_test) ** 2)
    print "test mse: %s" % test_mse
    return test_mse

def sklearn_linear_reg(x, y):
    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    print reg.coef_, reg.intercept_

    
def cv(x, y, fold):
    test_mses = []
    for k in range(fold):
        print 'fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        #fold2 = len(x_train)
        #fold2=10
        #best_lam = lambda_cv(x_train, y_train, fold2, regularizer)
        #test_mse = linear_regression(x_train, y_train, x_test, y_test, best_lam, regularizer)
        test_mse = linear_reg(x_train, y_train, x_test, y_test)
        test_mses.append(test_mse)   
    pprint(test_mses)
    avg_test_mse = np.mean(test_mses)
    print "average test mse: %f" % avg_test_mse
    
if __name__ == '__main__':
    fp = os.path.join('result', 'feature', 'all_features_extra.csv') 
    #fp = os.path.join('result', 'feature', 'all_freq_pat_support40.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,[1,2,6]]
    #x = data[:,[3,44]]
    #print x
    y = data[:,-1] 
    cv(x, y, fold=10)
    
#     model = linear_model.Lasso(alpha=0.01)
#     model.fit(x, y)
#     print model.coef_


    
    

    
    