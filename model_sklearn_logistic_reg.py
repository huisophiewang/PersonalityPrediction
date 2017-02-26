import os
import numpy as np
from pprint import pprint
from sklearn import linear_model
from sklearn import svm

'''
logistic 10 fold:
extra: 83.3%
agrbl: 59.2%
consc: 53.3%
neuro: 63.3%
openn: 58.3%

n fold
extra: 79.4%
consc: 58.8%
neuro: 64.7%
openn: 47.1%

SVM 
10 fold
extra: 71.7%
consc: 51.7%
neuro: 67.5%
openn: 51.7%

n fold
extra: 70.6%
consc: 58.8%
neuro: 73.5%
openn: 47.1%


'''

def sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam):
    clf = linear_model.LogisticRegression(C=lam)
    #clf = svm.SVC(C=lam)
    
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    #print acc
    return acc



def cross_validate(x, y, fold):
    lam_range = np.arange(0.01, 20, 0.1)
    lam_accs = []
    for lam in lam_range:
        accs = []
        for k in range(fold):
            #print 'fold: %d' % k
            hd_idx = np.arange(k, len(x), fold)
            x_test, y_test = x[hd_idx], y[hd_idx]
            x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
            #test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mae')
            #test_mse = my_linear_reg(x_train, y_train, x_test, y_test)
            acc = sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam)
            accs.append(acc)
        avg_acc = np.mean(accs)
        print "accuracy: %f " % avg_acc
        lam_accs.append(avg_acc)
    idx = np.argmax(lam_accs)
    best_lam = lam_range[idx]
    print "max accuracy: %f" % lam_accs[idx]
    print "best C: %f" % best_lam
        

    
if __name__ == '__main__':
    fp = os.path.join('result', 'feature', 'all_features_fp_openn_cls.csv')
    #fp = os.path.join('result', 'feature', 'all_features_all_traits_cls.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)

    x = data[:, 1:-1]
    #print x
    y = data[:,-1]
    #cross_validate(x, y, fold=10)
    #cross_validate(x, y, fold=len(x))
    print np.sum(y) 
    print len(y)
    