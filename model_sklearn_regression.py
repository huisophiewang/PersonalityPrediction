import os
import numpy as np
from sklearn import svm
from sklearn import linear_model
from sklearn import ensemble

def sklearn_reg(x_train, y_train, x_test, y_test, lam):
    reg = svm.SVR(C=lam, kernel='rbf')
    #reg = linear_model.Lasso(alpha=lam)
    #reg = linear_model.Ridge(alpha=lam)

    reg.fit(x_train, y_train)
    predict = reg.predict(x_test)
    test_mse = np.mean((predict - y_test) ** 2)
    return test_mse

def cross_validate(x, y, fold):
    lam_range = np.arange(0.001, 50.0, 0.01)
    lam_errs = []
    for lam in lam_range:
        errs = []
        for k in range(fold):
            #print 'fold: %d' % k
            hd_idx = np.arange(k, len(x), fold)
            x_test, y_test = x[hd_idx], y[hd_idx]
            x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
            #test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mae')
            #test_mse = my_linear_reg(x_train, y_train, x_test, y_test)
            err = sklearn_reg(x_train, y_train, x_test, y_test, lam)
            errs.append(err)
        avg_err = np.mean(errs)
        print "mse: %f " % avg_err
        lam_errs.append(avg_err)
    idx = np.argmin(lam_errs)
    best_lam = lam_range[idx]
    print "min mse: %f" % lam_errs[idx]
    print "best C: %f" % best_lam



if __name__ == '__main__':
    fp = os.path.join('result', 'feature', 'all_features_fp_agrbl_acii.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)

    x = data[:, 1:-1]
    y = data[:,-1]
    #cross_validate(x, y, fold=10)
    cross_validate(x, y, fold=len(x))