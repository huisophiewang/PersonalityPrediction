import numpy as np
from sklearn import datasets
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import r2_score



def lasso():  
    data_fp = r'result\feature\all_features.csv'
    data = np.genfromtxt(data_fp, delimiter=",", dtype=float, skip_header=1)
    # if random_state not specified, each run gives different result
    X_train, X_test, y_train, y_test = train_test_split(data[:,1:14], data[:,14], test_size=0.1, random_state=0)

    print X_train
    clf = linear_model.LassoCV()
    sfm = SelectFromModel(clf, threshold=0.00001)
    sfm.fit(X_train, y_train)
    
    # select 3 features using lasso
    X_train_trans = sfm.transform(X_train)
    n_features = X_train_trans.shape[1]
    while n_features > 3:
        sfm.threshold += 0.01
        print sfm.threshold
        X_train_trans = sfm.transform(X_train)
        n_features = X_train_trans.shape[1]
    print n_features
    print X_train_trans
    
    regr = linear_model.LinearRegression()
    regr.fit(X_train_trans, y_train)
    print('Coefficients: \n', regr.coef_)
#     r2 = r2_score(y_train, regr.predict(X_train_trans))  
#     print('R squared: \n', r2)
    X_test_trans = sfm.transform(X_test)
    mse = np.mean((regr.predict(X_test_trans) - y_test) ** 2)
    print("Mean squared error: %.2f" % mse)
    
    


    


if __name__ == '__main__':
    iris = datasets.load_iris()
    boston = datasets.load_boston()
    
    lasso()
