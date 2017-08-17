import os
from pprint import pprint
import numpy as np
import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier  #GBM algorithm
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn import svm

from util import TRAITS
    

def tune(x, y):
    param_test1 = {'n_estimators':range(1,30,1), 'learning_rate':[0.1, 0.15, 0.2, 0.25,0.3]}
    gsearch1 = GridSearchCV(estimator = AdaBoostClassifier(random_state=0),
                            param_grid = param_test1, scoring='accuracy',cv=10)

#     param_test1 = {'n_estimators':range(1,30,1),'learning_rate':[0.001, 0.01, 0.1, 0.2, 0.3], 'max_depth':[2,3,4]}
#     gsearch1 = GridSearchCV(estimator = GradientBoostingClassifier(random_state=0), 
#                             param_grid = param_test1, scoring='accuracy',cv=10)

#     param_test1 = {'C':np.arange(0.001, 2.0, 0.01)}
#     gsearch1 = GridSearchCV(estimator= svm.SVC(kernel='rbf'),
#                             param_grid = param_test1, scoring='accuracy',cv=10)
    
    gsearch1.fit(x,y)
    pprint(gsearch1.grid_scores_)
    print gsearch1.best_params_
    print gsearch1.best_score_
    
def sklearn_gradient_boost(x_train, y_train, x_test, y_test, p0, p1, p2):

    #clf = AdaBoostClassifier(n_estimators= p1, learning_rate=p2)
    clf = GradientBoostingClassifier(n_estimators= p1, learning_rate=p2, max_depth=p0)
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    #print acc
    return acc


def cross_validate(x, y, fold):
    p0_range = [1,2,3,4]
#     p1_range = range(1,15,2)
#     p2_range = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25 ]
    p1_range = range(1,20,1)
    p2_range = np.arange(0.001, 1.5, 0.01)
    para_accs = np.zeros((len(p0_range), len(p1_range), len(p2_range)))
    for a, p0 in enumerate(p0_range):
        for i, p1 in enumerate(p1_range):
            for j, p2 in enumerate(p2_range):
                accs = []
                for k in range(fold):
                    hd_idx = np.arange(k, len(x), fold)
                    x_test, y_test = x[hd_idx], y[hd_idx]
                    x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
                    acc = sklearn_gradient_boost(x_train, y_train, x_test, y_test, p0, p1, p2)
                    accs.append(acc)
                avg_acc = np.mean(accs)
                #print avg_acc
                para_accs[a][i][j] = avg_acc
    print para_accs
    print np.amax(para_accs)
    
if __name__ == '__main__':
    for trait in ['consc']:
        print '------------------------'
        print trait
        fp = os.path.join('result', 'feature', 'all_features_fp_%s_cls_acii_test1.csv' % trait)
        data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
        #np.random.shuffle(data)
    
        x = data[:, 1:-1]
        y = data[:,-1]
        
        #tune(x, y)
        
        cross_validate(x, y, len(x))
    

    
#     cls = GradientBoostingClassifier()
#     cls = AdaBoostClassifier()
#     print cls
#     cls.fit(x, y)
#     prediction = cls.predict(x)
#     train_acc = metrics.accuracy_score(y, prediction)
#     print train_acc
    
    
    
#     cv_score = cross_val_score(cls, x, y, cv=len(x), scoring='accuracy')
#     print cv_score
    
