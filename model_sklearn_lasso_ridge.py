import os
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from pprint import pprint


'''
old data:
baseline - mean_as_prediction:
MSE:
10 fold: 0.5637
n fold: 0.5818
MAE:
10 fold: 0.6212
n fold: 0.6292

baseline - linear regression
MSE:
10 fold: 0.7722

-------------------
LASSO
MSE:
all_heuristic_features_extra_old.csv
nested 10 fold: 0.5831
nested n fold: 0.4583
all_heuristic_features_extra_old.csv [1,2,6]
nested 10 fold: 0.5873
nested n fold: 0.4179

all_heuristic_features_extra.csv
nested 10 fold: 0.5878
nested n fold: 04187

all_freq_pat_support40_norm.csv
nested 10 fold: 0.5640
nested n fold: 0.6098
all_freq_pat_support40_norm.csv [3,49]
nested 10 fold: 0.5699
nested n fold: 0.4630

combined_all_extra.csv
nested 10 fold: 0.5696
nested n fold: 0.5475
-------------------
MAE:

all_heuristic_features_extra.csv
nested 10 fold: 0.6321
nested n fold: 0.5631
all_heuristic_features_extra.csv [1,2,6]
nested 10 fold: 0.6331
nested n fold: 0.4978

all_freq_pat_support40_norm.csv
nested 10 fold: 0.6199
nested n fold: 0.6685

combined_all_extra.csv
nested 10 fold: 0.6279
nested n fold: 0.5752
'''


def normalize_col(arr):
    means, stds = [], []
    result = np.zeros(arr.shape)
    for j in range(arr.shape[1]):
        cmean = np.mean(arr[:,j])
        means.append(cmean)
        cstd = np.std(arr[:,j])
        stds.append(cstd)
        result[:,j] = (arr[:,j]-cmean)/float(cstd)
    return result, means, stds


def linear_regression(x_tt, y_tt, x_hd, y_hd, lam, regularizer, err_type):
    #normalize x
    x_tt_norm, means, stds = normalize_col(x_tt)
    if regularizer == 'L1':
        clf = linear_model.Lasso(alpha=lam, fit_intercept=False)
    elif regularizer == 'L2':
        clf = linear_model.Ridge(alpha=lam, fit_intercept=False)
    
    clf.fit(x_tt_norm, y_tt)
    #print('Coefficients: \n', clf.coef_)
    x_hd_norm = np.zeros(x_hd.shape)
    for j in range(x_hd.shape[1]):
        x_hd_norm[:,j]=(x_hd[:,j]-means[j])/stds[j]
    #y_predict = np.dot(x_hd_norm, clf.coef_.T) + np.mean(y_tt)
    #print y_predict
    y_predict = clf.predict(x_hd_norm) + np.mean(y_tt) # equal as above
    if err_type == 'mse':
        err = np.mean((y_predict - y_hd) ** 2)
    elif err_type == 'mae':
        err = np.mean(np.fabs(y_predict - y_hd))
    #print("Mean squared error: %f" % mse)
    return err

def get_ymean_prediction_err(y_tt, y_hd, err_type):
    y_predict = np.mean(y_tt)
    #print y_predict
    #y_predict = clf.predict(x_hd_norm) + np.mean(y_tt) # equal as above
    if err_type == 'mse':
        err = np.mean((y_predict - y_hd) ** 2)
    elif err_type == 'mae':
        err = np.mean(np.fabs(y_predict - y_hd))
    return err
    
def linear_regression2(x_tt, y_tt, x_hd, y_hd, lam, regularizer, err_type):
    if regularizer == 'L1':
        print x_hd
        print y_hd
        model = linear_model.Lasso(alpha=lam)
        model.fit(x_tt, y_tt)
        predict = np.dot(x_hd, model.coef_) + model.intercept_
        print model.coef_
        #print lam
        print predict
    if err_type == 'mse':
        err = np.mean((predict - y_hd)**2)
    return err    


    
def lambda_cv(x_train, y_train, fold, regularizer, err_type):
    lam_range = [1.0]
    #lam_range = [0.15]
    if regularizer == 'L1':
        lam_range = [0.0]
        lam_range = np.arange(0.0, 0.5, 0.01)
    elif regularizer == 'L2':
        lam_range = np.arange(0.0, 150, 1.0)
        #lam_range = [10 ** j for j in range(-5, 6)]

    lam_errs = []
    for lam in lam_range:
        #print "lambda is %f" % lam
        fold_errs = []
        for k in range(fold):
            #print 'fold: %d' % k
            hd_idx = np.arange(k, len(x_train), fold)
            x_hd, y_hd = x_train[hd_idx], y_train[hd_idx]
            x_tt, y_tt = np.delete(x_train, hd_idx, axis=0), np.delete(y_train, hd_idx, axis=0)
            err = linear_regression(x_tt, y_tt, x_hd, y_hd, lam, regularizer, err_type)
            fold_errs.append(err)
        lam_errs.append(np.mean(fold_errs))
    pprint(lam_errs)
    idx = np.argmin(lam_errs)
    #print idx
    best_lam = lam_range[idx]
    print "best lambda %f" % best_lam
    #plot_mse(lam_range, lam_errs,fold)
    return best_lam

def linear_reg_cv(x, y, fold, regularizer, err_type):
    test_errs = []
    for k in range(fold):
        print 'outer fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        fold2 = len(x_train)
        fold2=fold
        best_lam = lambda_cv(x_train, y_train, fold2, regularizer, err_type)
        #best_lam = 0.0
        test_err = linear_regression(x_train, y_train, x_test, y_test, best_lam, regularizer, err_type)
        test_errs.append(test_err)   
        
    pprint(test_errs)
    avg_test_err = np.mean(test_errs)
    print "average test err: %f" % avg_test_err
        
def mean_as_prediction_cv(x, y, fold, err_type):
    test_errs = []
    for k in range(fold):
        print 'outer fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)

        test_err = get_ymean_prediction_err(y_train, y_test, err_type)
        test_errs.append(test_err)   
        
    pprint(test_errs)
    avg_test_err = np.mean(test_errs)
    print "average test err: %f" % avg_test_err
    
def plot_mse(lam_range, hd_mse, fold):
    plt.title('holdout_mse vs lambda, fold=%d' % fold)
    plt.xlabel('log(lambda)')
    plt.ylabel('holdout_mse')
    plt.plot(np.log10(lam_range), hd_mse, color = 'red')
    #plt.plot(lam_range, hd_mse, color = 'red')
    #plt.plot(np.log10(lam_range), tt_mse, color = 'blue')
    plt.show()       
    
def test_mean(y): 
    # 0.5573
    y_mean = np.mean(y)
    mse = 0.0
    for yi in y:
        mse += (yi-y_mean)*(yi-y_mean)
    #print mse
    #print len(y)
    print mse/len(y)
    

    
if __name__ == '__main__':

    #fp = os.path.join('result', 'feature', 'all_heuristic_features_extra.csv')
    #fp = os.path.join('result', 'feature', 'all_features_extra.csv')
    #fp = os.path.join('result', 'feature', 'all_features_consc.csv')
    #fp = os.path.join('result', 'feature', 'all_features_neuro.csv')
    fp = os.path.join('result', 'feature', 'all_features_openn.csv')
    #fp = os.path.join('result', 'feature', 'all_freq_pat_support40.csv')
    #fp = os.path.join('result', 'feature', 'all_freq_pat_support40_typed.csv')
    #fp = os.path.join('result', 'feature', 'all_freq_pat_support40_norm.csv')
    #fp = os.path.join('result', 'feature', 'combined_all_extra.csv')
    
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)
    x = data[:,1:-1]
    #x = data[:,[3,49]]
    y = data[:,-1:]    
    #y = y/5.0
    #x = np.genfromtxt('pca95_all_freq_pat_support40.csv', delimiter=",", dtype=float)
    #x = np.genfromtxt('pca95_all_features_extra.csv', delimiter=",", dtype=float)
    #test_mse_cv(x, y, fold=10, regularizer='L1')
    
    #test_mean(y)
    
    #y_scale = y / 4.0 - 0.25
    #print np.max(y)
    #print np.min(y)
    #y_scale = (y - np.min(y))/(np.max(y)-np.min(y))
#     print y_scale
#     print len(y_scale)
#     test_mean(y_scale)

    #mean_as_prediction_cv(x, y, fold=10, err_type='mse')
    
    linear_reg_cv(x, y, fold=10, regularizer='L2', err_type='mse')

    
    

    
    
    
    