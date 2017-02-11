import os
import numpy as np
from pprint import pprint
from sklearn import linear_model

def sklearn_logistic_reg(x_train, y_train, x_test, y_test):
    logreg = linear_model.LogisticRegression()
    logreg.fit(x_train, y_train)

    predict = logreg.predict(x_test)
    print predict
    print y_test
    
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    print acc
    return acc



def cross_validate(x, y, fold):
    accs = []
    for k in range(fold):
        print 'fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        #test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mae')
        #test_mse = my_linear_reg(x_train, y_train, x_test, y_test)
        acc = sklearn_logistic_reg(x_train, y_train, x_test, y_test)
        accs.append(acc)
    avg_acc = np.mean(accs)
    print avg_acc
        

    
if __name__ == '__main__':
    #fp = os.path.join('result', 'feature', 'all_features_extra_cls.csv')
    #fp = os.path.join('result', 'feature', 'all_features_consc_cls.csv')
    fp = os.path.join('result', 'feature', 'all_features_neuro_cls.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)

    x = data[:, 1:-1]
    #print x
    y = data[:,-1]
    cross_validate(x, y, fold=10)