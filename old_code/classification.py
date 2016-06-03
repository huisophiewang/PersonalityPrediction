from sklearn import datasets
from sklearn import svm
from sklearn import linear_model
from sklearn import cross_validation

import numpy as np




def clf_logit(X, Y):
    clf = linear_model.LogisticRegression()
    model = clf.fit(X, Y)
    model.score(X, Y)


def clf_svm(X, Y):
    print np.unique(Y)
    
    model = svm.SVC()
    print model.fit(X[:-1], Y[:-1])  
    print model.predict(X[-1:])
    print Y[-1]

if __name__ == '__main__':
#     iris = datasets.load_iris()
#     print iris.data.shape
#     clf_svm(iris.data, iris.target)

    fp = r"data\matrix_data\logit\wifi_features_extra.csv" 
    data = np.genfromtxt(fp, delimiter=",", dtype=float)
    print data.shape
    n = data.shape[0]
    m = data.shape[1]
    #fold = 5
    fold = 25
    test_data = np.empty([n/fold, m])
    train_data = np.empty([n-n/fold, m])
    
    X = data[:,:-2]
    Y = data[:,-1]
    
    clf = linear_model.LogisticRegression()
    #clf = svm.SVC(kernel='linear')
    
#     print clf.fit(X[:-1], Y[:-1])  
#     print clf.predict(X[-1:])
#     print Y[-1]

    ss = cross_validation.ShuffleSplit(25, n_iter=5, test_size=0.2, random_state=0)
    for train_index, test_index in ss:
        print("%s %s" % (train_index, test_index))
    
    scores = cross_validation.cross_val_score(clf, X, Y, cv=ss, n_jobs=-1)
    print scores
    print scores.mean()
    
    
