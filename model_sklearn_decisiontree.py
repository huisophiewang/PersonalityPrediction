from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import datasets
import subprocess



def example():
    iris = datasets.load_iris()
    print iris
    clf = DecisionTreeClassifier(max_depth=2,criterion="entropy") # construct a decision tree.
    clf.fit(iris.data,iris.target)  # train it on the dataset
    #dot_file = tree.export_graphviz(clf.tree_, out_file='tree_d1.dot', feature_names=iris.feature_names)  #export the tree to .dot file

if __name__ == '__main__':
    example()

    
    