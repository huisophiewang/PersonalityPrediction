import os
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from pprint import pprint


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


def linear_regression(x_tt, y_tt, x_hd, y_hd, lam, regularizer):
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
    y_predict = np.dot(x_hd_norm, clf.coef_.T) + np.mean(y_tt)
    #print y_predict
    #y_predict = clf.predict(x_hd_norm) + np.mean(y_tt) # equal as above
    mse = np.mean((y_predict - y_hd) ** 2)
    #print("Mean squared error: %f" % mse)
    return mse
        
               
def lambda_cv(x_train, y_train, fold, regularizer):
    lam_range = [1.0]
    #lam_range = [0.15]
    if regularizer == 'L1':
        lam_range = np.arange(0.01, 1.0, 0.01)
    elif regularizer == 'L2':
        lam_range = np.arange(1.0, 150, 1.0)
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
            print y_tt
            mse = linear_regression(x_tt, y_tt, x_hd, y_hd, lam, regularizer)
            fold_errs.append(mse)
        lam_errs.append(np.mean(fold_errs))
    pprint(lam_errs)
    idx = np.argmin(lam_errs)
    #print idx
    best_lam = lam_range[idx]
    print "best lambda %f" % best_lam
    #plot_mse(lam_range, lam_errs,fold)
    return best_lam

def test_mse_cv(x, y, fold, regularizer):
    test_mses = []
    for k in range(fold):
        print 'outer fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        fold2 = len(x_train)
        #fold2=10
        best_lam = lambda_cv(x_train, y_train, fold2, regularizer)
        test_mse = linear_regression(x_train, y_train, x_test, y_test, best_lam, regularizer)
        test_mses.append(test_mse)   
    pprint(test_mses)
    avg_test_mse = np.mean(test_mses)
    print "average test mse: %f" % avg_test_mse
        

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
    print mse
    print len(y)
    print mse/len(y)
    


if __name__ == '__main__':
    #fp = 'pca_all_freq_pat_support40.csv'
    fp = os.path.join('result', 'feature', 'all_freq_pat_support40.csv')
    fp = os.path.join('result', 'feature', 'all_features_extra.csv')
    
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,1:-1]
    y = data[:,-1:]    
    #x = np.genfromtxt('pca95_all_freq_pat_support40.csv', delimiter=",", dtype=float)
    #x = np.genfromtxt('pca95_all_features_extra.csv', delimiter=",", dtype=float)
    #test_mse_cv(x, y, fold=10, regularizer='L1')
    
    #test_mean(y)
    
    

    
    
    
    