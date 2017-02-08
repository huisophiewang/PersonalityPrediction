import os
import numpy as np
from sklearn import linear_model
from pprint import pprint
from model_sklearn_lasso import lasso

'''
baseline - mean_as_prediction:
MSE:
10 fold: 0.5637
n fold: 0.5818
MAE:
10 fold: 0.6212
n fold: 0.6292

all_heuristic_features_extra.csv
10 fold: 0.3810
n fold: 0.4170
all_heuristic_features_extra.csv [1,2,6]
10 fold: 0.3647
n fold: 0.4160

all_freq_pat_support40_norm.csv
10 fold: 63984
n fold: 1714

combined_all_extra.csv
10 fold: 18457
n fold: 5315

'''

def my_linear_reg(x_train, y_train, x_test, y_test):
    print x_test
    print y_test
    x_train = np.c_[np.ones(len(x_train)), x_train]
    pseudo_inv = np.linalg.inv(np.dot(x_train.T, x_train))
    w = np.dot(np.dot(pseudo_inv, x_train.T), y_train)
    print  w
    x_test = np.c_[np.ones(len(x_test)), x_test]
    predict = np.dot(x_test, w)
    print predict
    test_mse = np.mean((predict - y_test) ** 2)
    print "test mse: %s" % test_mse
    return test_mse



def sklearn_linear_reg(x_train, y_train, x_test, y_test):
    reg = linear_model.LinearRegression()
    reg.fit(x_train, y_train)
    print reg.coef_, reg.intercept_
    
def sklearn_lasso_test(x_train, y_train, x_test, y_test):
    reg = linear_model.Lasso(alpha=0.0001)
    reg.fit(x_train, y_train)
    print reg.coef_, reg.intercept_
    
def cv(x, y, fold):
    test_mses = []
    for k in range(fold):
        print 'fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        #lasso(x_train, y_train)
        #test_mse = sklearn_lasso_test(x_train, y_train, x_test, y_test)
        test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mse')
        test_mses.append(test_mse)   
    pprint(test_mses)
    avg_test_mse = np.mean(test_mses)
    print "average test mse: %f" % avg_test_mse
       
def mean_as_prediction(y, y_mean, err_type): 
    err = 0.0
    if err_type == 'mse':
        err = np.mean((y - y_mean)**2)
    elif err_type == 'mae':
        err = np.mean(np.fabs(y - y_mean))
        
    print err
    return err


    
if __name__ == '__main__':
    fp = os.path.join('result', 'feature', 'all_features_extra.csv') 
    #fp = os.path.join('result', 'feature', 'all_freq_pat_support40.csv')
    #fp = os.path.join('result', 'feature', 'all_freq_pat_support40_norm.csv')
    #fp = os.path.join('result', 'feature', 'combined_all_extra.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,1:-1]
    #x = data[:,[1,2,6]]
    #x = data[:,[3,44]]
    #x = data[:,[3, 4, 49]]
    #x = data[:,[1, 2, 6, 10]]
    y = data[:,-1] 
    #y = y/5.0
    cv(x, y, fold=10)
    
#     model = linear_model.Lasso(alpha=0.01)
#     model.fit(x, y)
#     print model.coef_


    
    

    
    