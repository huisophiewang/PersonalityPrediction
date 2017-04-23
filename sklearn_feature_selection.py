
import os
import numpy as np
from sklearn import linear_model
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import KFold
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest, SelectFromModel
from sklearn.feature_selection import chi2, f_regression, mutual_info_regression
from sklearn.feature_selection import RFE, RFECV




    
def sklearn_logistic_reg(x_train, y_train, x_test, y_test):
    clf = linear_model.LogisticRegression(penalty='l1')
    #clf = svm.SVC(C=lam, kernel='rbf')
    
    
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    #print acc
    return acc

    
def wrapper_method(x, y):
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)
    x = data[:, 1:-1]
    y = data[:,-1]
    # create a base classifier used to evaluate a subset of attributes
    #estimator = LogisticRegression()
    estimator = SVC(kernel="linear")
    
    # create the RFE model and select 3 attributes
    # selector = RFE(model, 3)
    selector = RFECV(estimator, step=1, cv=5)
    # summarize the selection of the attributes
    selector = selector.fit(x, y)
    print(selector.support_)
    print(selector.ranking_)


    x = data[:, [1,3,6,9]]
    #print x
    y = data[:,-1]
    
    fold = len(x)
    accs = []
    for k in range(fold):
        #print 'fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        #test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mae')
        #test_mse = my_linear_reg(x_train, y_train, x_test, y_test)
        acc = sklearn_logistic_reg(x_train, y_train, x_test, y_test)
        accs.append(acc)
    avg_acc = np.mean(accs)
    print avg_acc
    
           
def filter_method(fp):
#     iris = load_iris()
#     X, y = iris.data, iris.target
#     print X
#     print y
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)
    x = data[:, 1:-1]
    y = data[:,-1]
    
    fr = open(fp, 'rU')
    header = fr.readline().split(',')
    fr.close()
    header = np.array(header)
    #print header
    # metric: regression: f_regression, mutual_info_regression
    #         classification: chi2, f_classif, mutual_info_classif
    selector = SelectKBest(mutual_info_regression, k=9)
    selector.fit(x,y)

    index = selector.get_support(indices=True)
    print header[index+1]
    
    print selector.scores_
    print selector.pvalues_
    #x_new = SelectKBest(f_regression, k=4).fit_transform(x, y)
    #print x_new
    
def embeded_method(fp):
    
#     iris = load_iris()
#     x, y = iris.data, iris.target
#     lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(x, y)
#     print lsvc.coef_
#     model = SelectFromModel(lsvc, prefit=True)
#     print model.get_support(indices=False)
#     x_new = model.transform(x)
    
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:, 1:-1]
    y = data[:,-1]
    
#     lasso = linear_model.Lasso().fit(x,y)
#     print lasso.coef_
#     model = SelectFromModel(lasso, prefit=True)
#     print model.get_support(indices=False)
    
    # select stable features using randomized logistic reg + L1
    selector = linear_model.RandomizedLogisticRegression().fit(x,y)
    #print selector.scores_
    print selector.get_support(indices=False)
    



if __name__ == '__main__':
    fp = os.path.join('result', 'feature', 'all_features_fp_extra_cls_all.csv')
    
    #wrapper_method(fp)
    #filter_method(fp)
    embeded_method(fp)

    



