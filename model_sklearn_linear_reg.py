import os
import numpy as np
from sklearn import linear_model
from pprint import pprint
from model_sklearn_lasso import lasso

'''
------------------
baseline - mean as prediction (10 fold):
extra:0.5483
agrbl:0.4666
consc:0.5648
neuro:0.5070
openn:0.2822
------------------
linear reg
extra:0.3495 (end_var, num_day, bluetooth_daytime) reduced 36.3% from baseline
      0.3678 (end_var, num_day)
      0.4104 (len_var, end_var, num_day, bluetooth_daytime)
agrbl:0.4382 (bluetooth_total)
consc:0.4539 (start_var, day_entropy, piazza_questions) %19.6 from baseline
      0.4576 (start_var, piazza_question) (selected by forward selection)
neuro:0.4192 (end_var, bluetooth_daytime), 17.3% from baseline
      0.4399 (end_var)
openn:0.2660 (bluetooth_evening), 5.7% from baseline
------------------
linear reg + L2 (nested cross valid):
extra:0.3920
consc:0.4576
neuro:0.4333
openn:0.2760
-----------------
linear reg + L1 (cross valid):
extra: 0.4027
agrbl: 0.4382
consc: 0.4539
neuro: 0.4185
openn: 0.2659

'''

def linear_reg(x_train, y_train, x_test, y_test, degree):
#     x_train = poly_basis_trans(x_train, degree)
#     pseudo_inv = np.linalg.inv(np.dot(np.transpose(x_train), x_train))
#     pseduo_inv = np.dot(pseudo_inv, np.transpose(x_train))
#     w = np.dot(pseduo_inv, y_train)
#     print "cofficients w: %s" % w.T 
#     train_err = np.mean((np.dot(x_train, w) - y_train) ** 2)
#     print "training mse: %s" % train_err
#     x_test = poly_basis_trans(x_test, degree)
#     test_err = np.mean((np.dot(x_test, w) - y_test) ** 2)
#     print "test mse: %s" % test_err
    pass

def my_linear_reg(x_train, y_train, x_test, y_test):
    x_train = np.c_[np.ones(len(x_train)), x_train]
    pseudo_inv = np.linalg.inv(np.dot(x_train.T, x_train))
    w = np.dot(np.dot(pseudo_inv, x_train.T), y_train)
    print  w
    x_test = np.c_[np.ones(len(x_test)), x_test]
    predict = np.dot(x_test, w)
    #print predict
    test_mse = np.mean((predict - y_test) ** 2)
    return test_mse

def sklearn_linear_reg(x_train, y_train, x_test, y_test):
    reg = linear_model.LinearRegression()
    reg.fit(x_train, y_train)
    print reg.coef_, reg.intercept_
    predict = reg.predict(x_test)
    test_mse = np.mean((predict - y_test) ** 2)
    return test_mse
    
def sklearn_lasso_test(x_train, y_train, x_test, y_test):
    reg = linear_model.Lasso(alpha=0.0001)
    reg.fit(x_train, y_train)
    print reg.coef_, reg.intercept_
    
    
def mean_as_prediction(y, y_mean, err_type): 
    err = 0.0
    
    if err_type == 'mse':
        err = np.mean((y - y_mean)**2)
    elif err_type == 'mae':
        err = np.mean(np.fabs(y - y_mean))
    return err

def linear_reg_cv(x, y, fold):
    test_mses = []
    for k in range(fold):
        print 'fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        #test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mse')
        #test_mse = my_linear_reg(x_train, y_train, x_test, y_test)
        test_mse = sklearn_linear_reg(x_train, y_train, x_test, y_test)
        
        test_mses.append(test_mse)   
    pprint(test_mses)
    avg_test_mse = np.mean(test_mses)
    print "average test mse: %f" % avg_test_mse
    
if __name__ == '__main__':
    #iris = datasets.load_iris()
    #boston = datasets.load_boston()
#     fp = os.path.join('dataset', 'survey', 'BigFivePre_oncampus.csv')
#     data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
#     for i in range(5):
#         print np.var(data[:, i+1])
    
    #fp = os.path.join('result', 'feature', 'all_features_extra.csv')
    fp = os.path.join('result', 'feature', 'all_features_all_traits.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)
    #x = data[:, [8,16,19]]
    #print x
    x = data[:, 1:-5]
    #print x
    y = data[:,-1]
    linear_reg_cv(x, y, fold=10)
    