import numpy as np
from sklearn import datasets
from sklearn import linear_model
from sklearn.model_selection import train_test_split



def lasso():
    # We use the base estimator LassoCV since the L1 norm promotes sparsity of features.
    
    # if random_state not specified, each run gives different result
    #X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=0)
    #print X_test
    #print y_test
    data_fp = r'result\feature\all_features.csv'
    data = np.genfromtxt(data_fp, delimiter=",", dtype=float, skip_header=1)
    print data[0]
    print data[:,0]
    print data[1,1]
    print data[1][1]
    
    X_train, X_test, y_train, y_test = train_test_split(data[:,1:14], data[:,14], test_size=0.1, random_state=0)
    print X_test
    print y_test
    
    regr = linear_model.LinearRegression()
    
    # Train the model using the training sets
    regr.fit(X_train, y_train)
    
    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f" % np.mean((regr.predict(X_test) - y_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(X_test, y_test))
if __name__ == '__main__':
    iris = datasets.load_iris()
    boston = datasets.load_boston()
    X, y = boston['data'], boston['target']
    print X.shape
    print X