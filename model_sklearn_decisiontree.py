import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from pprint import pprint

'''
decision tree regression:
extra: 0.5380 (depth=3)
agrbl: 0.5495 (depth=3)
consc: 0.5728 (depth=3)
neuro: 0.5351 (depth=2)
openn: 0.3149 (depth=1)

# decision tree + ada boosting:
# extra: 0.4251 (depth=2)
# consc: 0.5306 (depth=1)
# neuro: 

random forest regression:
extra: 0.4536
agrbl: 0.5138
consc: 0.6620
neuro: 0.5255
openn: 0.3658
'''

def example():
    iris = datasets.load_iris()
    print iris
    clf = DecisionTreeClassifier(max_depth=0,criterion="entropy") # construct a decision tree.
    clf.fit(iris.data,iris.target)  # train it on the dataset
    #dot_file = tree.export_graphviz(clf.tree_, out_file='tree_d1.dot', feature_names=iris.feature_names)  #export the tree to .dot file

def dec_tree(x_train, y_train, x_test, y_test):
    reg = DecisionTreeRegressor(max_depth=3, random_state=0)
    #reg = AdaBoostRegressor(DecisionTreeRegressor(max_depth=15, random_state=0),n_estimators=300, random_state=0)
    #reg = RandomForestRegressor(random_state=0)
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
    fp = os.path.join('result', 'feature', 'all_features_all_traits.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:, 1:-5]
    y = data[:,-1]
    dec_tree_cv(x, y, fold=10)
    
    