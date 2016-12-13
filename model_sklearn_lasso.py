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


'''
all_features_extra.csv
d=1: [2]
d=2: [2, 6] start_time_var, absent
d=3: [1, 2, 6] len_var, start_time_var, absent (*)
d=4: [1, 2, 6, 7], len_var, start_time_var, absent, late_time_var

all_freq_pat_support40.csv 
d=1: [44]
d=2: [3, 44] (*)
d=3: [3, 39, 44]
d=5: [3, 29, 39, 43, 44]
d=6: [1, 3, 29, 39, 43, 44]

all_freq_pat_support40.csv (normalized)
d=1: [3]
d=2: [3, 49] (*)
d=3: [3, 4, 49]
d=4: [3, 4, 48, 49]
d=5: [3, 4, 43, 48, 49]

all_freq_pat_support40_typed.csv
d=1: [2]
d=2: [2, 3]
d=3: [2, 3, 55]
d=4: [2, 3, 23, 55]
d=5: [2, 3, 12, 23, 55]
d=6: [2, 3, 12, 23, 32, 55]

combined_all_extra.csv
d=1: [2]
d=2: [2, 6]
d=3: [2, 6, 10]
d=4: [1, 2, 6, 10]
d=5: [1, 2, 6, 10, 11]
d=7: [1, 2, 6, 10, 11, 51, 55]
d=8: [1, 2, 6, 10, 11, 46, 51, 55]
'''

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
    
    print X_train_trans
    
#     regr = linear_model.LinearRegression()
#     regr.fit(X_train_trans, y_train)
#     print('Coefficients: \n', regr.coef_)
#     r2 = r2_score(y_train, regr.predict(X_train_trans))  
#     print('R squared: \n', r2)
#     X_test_trans = sfm.transform(X_test)
#     mse = np.mean((regr.predict(X_test_trans) - y_test) ** 2)
#     print("Test MSE: %.2f" % mse)
    
        
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
    lam_range = np.arange(0.01, 0.5, 0.01)
    for lam in lam_range:
        model = linear_model.Lasso(alpha=lam)
        model.fit(x, y)
        print model.coef_
        #print model.intercept_
        idx = []
        for i, c in enumerate(model.coef_):
            if c != 0.0:
                idx.append(i+1)  ## index starts from 1
        print idx
        predict = np.dot(x, model.coef_) + model.intercept_
        train_mse = np.sum((predict - y)**2)/len(y)
        print train_mse
        #train_mse = 
                
    
if __name__ == '__main__':
    iris = datasets.load_iris()
    boston = datasets.load_boston()
    
    fp = os.path.join('result', 'feature', 'all_heuristic_features_extra.csv')
    #fp = os.path.join('result', 'feature', 'all_freq_pat_support40_norm.csv')
    #fp = os.path.join('result', 'feature', 'all_freq_pat_support40_typed.csv')
    #fp = os.path.join('result', 'feature', 'combined_all_extra.csv')
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
    
    

     
    
