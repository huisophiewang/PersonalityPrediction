import numpy as np
from numpy.linalg import inv
from numpy import nan

from utilities import LABELS
from utilities import replace_nan

# x_cols = [1,2,3]
# 
# 
# 
# data_x = np.loadtxt(fp, delimiter=",", skiprows = 1, usecols=x_cols)
# data_y = np.genfromtxt(fp, delimiter=",", skiprows = 1, usecols=y_cols)


def get_beta(train_data, y_col):
    train_x = train_data[:, [1,2,3]]
    train_x = np.insert(train_x, 0, 1, axis=1)
    train_y = train_data[:, y_col]

    inverse = inv(np.dot(np.transpose(train_x), train_x))
    beta = np.dot(inverse, np.dot(np.transpose(train_x), train_y))
    #print beta
    return beta
    
def get_mse(test_data, beta, y_col):
    test_x = test_data[:, [1,2,3]]
    test_x = np.insert(test_x, 0, 1, axis=1)
    test_y = test_data[:, y_col]
    #print test_y
    
    predict_y = np.dot(test_x, beta)
    #print predict_y
    
    mse = 0.0
    num = test_data.shape[0]
    for i in range(num):
        #print test_y[i], predict_y[i]
        mse += (predict_y[i] - test_y[i]) * (predict_y[i] - test_y[i])
        
    mse /= num
    #print "mse: " + str(mse)
    return mse



    
    
    
if __name__ == '__main__':
    fp = r"data\matrix_data\all_wifi_features.csv"
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)

    x_cols = [1,2,3]
    n = data.shape[0]
    m = data.shape[1]
    fold = 5
    test_data = np.empty([n/fold, m])
    train_data = np.empty([n-n/fold, m])
     
    y_cols = range(4, 19)
    for y_col in y_cols:
        print '================================================================'
        print LABELS[y_col-4]
        replace_nan(data, y_col)
         
        avg_mse = 0.0
        for j in range(fold):
            #print "fold %d" % j
            for i, x in enumerate(data):
                if i%fold == j:
                    test_data[i/fold] = data[i]
                else:
                    train_data[(i/fold)*(fold-1)+i%fold-1] = data[i]
          
            beta = get_beta(train_data, y_col)
            mse = get_mse(test_data, beta, y_col)
            avg_mse += mse
        avg_mse /= fold
        print "average mse: " + str(avg_mse)
    
    
    
    

    
            
            