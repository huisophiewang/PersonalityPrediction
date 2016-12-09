import os
import numpy as np
from sklearn import datasets
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import r2_score
from itertools import cycle
import matplotlib.pyplot as plt
from pprint import pprint


def lasso_by_num(X_train, y_train, num):  
    # if random_state not specified, each run gives different result
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=0)

    print X_train
    # number of features = ycol-1 

    clf = linear_model.LassoCV()
    sfm = SelectFromModel(clf, threshold=0.00001)
    sfm.fit(X_train, y_train)

    # select 3 features using lasso
    X_train_trans = sfm.transform(X_train)
    n_features = X_train_trans.shape[1]
    while n_features > num:
        sfm.threshold += 0.01
        #print sfm.threshold
        X_train_trans = sfm.transform(X_train)
        n_features = X_train_trans.shape[1]
        
    #print n_features
    # num=4: len_var, start_time_var, absent, late_time_var
    # num=3: len_var, start_time_var, absent
    # num=2: len_var, start_time_var,
    '''
    d = 2: fp_sudikoff, fp_53_commons;north-main, (3, 44)
    d = 3: (3, 39, 44)
    d = 4: (
    d = 5: (3, 29, 39, 43, 44)
    d = 6: (1, 3, 29, 39, 43, 44)
    '''
    
    print X_train_trans
    
#     regr = linear_model.LinearRegression()
#     regr.fit(X_train_trans, y_train)
#     print('Coefficients: \n', regr.coef_)
#     r2 = r2_score(y_train, regr.predict(X_train_trans))  
#     print('R squared: \n', r2)
#     X_test_trans = sfm.transform(X_test)
#     mse = np.mean((regr.predict(X_test_trans) - y_test) ** 2)
#     print("Test MSE: %.2f" % mse)
    
    
def lassoCV_test(fp, ycol):
    
    # if random_state not specified, each run gives different result
    X_train, X_test, y_train, y_test = train_test_split(data[:,1:ycol], data[:,ycol], test_size=0.1, random_state=0)
    clf = linear_model.LassoCV()
    clf.fit(X_train, y_train)
    
def lasso_path_test(x, y):
    eps = 5e-3
    alphas, coefs, _ = linear_model.lasso_path(x, y, eps)

    print alphas
    print len(alphas)
    print coefs.shape
    print coefs[0].shape
    print len(coefs[0].T)
    print coefs[0].T[50]
    for i in coefs[0]:
        print i
        
def plot(X, y):
    
    #X /= X.std(axis=0)  # Standardize data (easier to set the l1_ratio parameter)
    
    # Compute paths
    
    eps = 5e-3  # the smaller it is the longer is the path

    alphas_lasso, coefs_lasso, _ = linear_model.lasso_path(X, y, eps)
    print alphas_lasso
    print coefs_lasso.shape
    
    for i in coefs_lasso.T:
        print i
    
    plt.figure(1)
    ax = plt.gca()
    
    colors = cycle(['r', 'g', 'b', 'c', 'm', 'y'])
    neg_log_alphas_lasso = -np.log10(alphas_lasso)

    for coef_l, c in zip(coefs_lasso, colors):
        l1 = plt.plot(neg_log_alphas_lasso, coef_l, c=c)
 
    
    plt.xlabel('-Log(alpha)')
    plt.ylabel('coefficients')
    plt.title('Lasso and Elastic-Net Paths')
    #plt.legend((l1[-1], l2[-1]), ('Lasso', 'Elastic-Net'), loc='lower left')
    plt.axis('tight')
    plt.show()
    
def lasso(x, y):
    lam_range = np.arange(0.01, 1.0, 0.01)
    for lam in lam_range:
        model = linear_model.Lasso(alpha=lam)
        model.fit(x, y)
        print model.coef_
    
if __name__ == '__main__':
    iris = datasets.load_iris()
    boston = datasets.load_boston()
    
    fp = os.path.join('result', 'feature', 'all_features_extra.csv')
    fp = os.path.join('result', 'feature', 'all_freq_pat_support40.csv')
    #pprint(open(fp, 'rU').readline().split(','))
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:, 1:-1]
    y = data[:,-1]
     
    lasso(x, y)
    #lasso_by_num(x, y, 1)

    #lasso(x, y, 51, num=4)
    #lasso(r'result\feature\freq_pat_extra.csv', 8)
    #lasso_path_test(x, y)
    
#     diabetes = datasets.load_diabetes()
#     x = diabetes.data
#     y = diabetes.target
#     print x.shape
#     print y.shape
    #plot(x, y)
    
    

     
    
