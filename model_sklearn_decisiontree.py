import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor
from pprint import pprint


def example():
    iris = datasets.load_iris()
    print iris
    clf = DecisionTreeClassifier(max_depth=2,criterion="entropy") # construct a decision tree.
    clf.fit(iris.data,iris.target)  # train it on the dataset
    #dot_file = tree.export_graphviz(clf.tree_, out_file='tree_d1.dot', feature_names=iris.feature_names)  #export the tree to .dot file

def dec_tree(x_train, y_train, x_test, y_test):
    reg = DecisionTreeRegressor(max_depth=3, random_state=0)
    reg.fit(x_train, y_train)
    predict = reg.predict(x_test)
    test_mse = np.mean((predict - y_test) ** 2)
    return test_mse

def dec_tree_cv(x, y, fold):
    test_mses = []
    for k in range(fold):
        print 'fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        #test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mae')
        #test_mse = my_linear_reg(x_train, y_train, x_test, y_test)
        test_mse = dec_tree(x_train, y_train, x_test, y_test)
        
        test_mses.append(test_mse)   
    pprint(test_mses)
    avg_test_mse = np.mean(test_mses)
    print "average test mse: %f" % avg_test_mse
    
    
if __name__ == '__main__':
    #example()
    fp = os.path.join('result', 'feature', 'all_features_consc.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:, 1:-1]
    y = data[:,-1]
    dec_tree_cv(x, y, fold=10)
    
    