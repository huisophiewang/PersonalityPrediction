import math
import os
from pprint import pprint
import numpy as np

from utilities import get_y, z_score_normalize, replace_nan
from utilities import LABELS, CUR_DIR
from utilities import distance, edit_dist, KL_divergence

def RBF_weight(x1, x2):
    pass

def knn(train_data, test_data, k):
    # num of training instances
    n = train_data.shape[0]
    # num of featrues + 1
    p = train_data.shape[1]
    # num of test instances
    m = test_data.shape[0]
     
    # predict test data
    predict = np.empty((m,1))
    # distance from test instance to all training instances
    dist_mat = np.zeros((m,n))
     
    for i, x1 in enumerate(test_data):
        for j, x2 in enumerate(train_data):
            #dist_mat[i][j] = KL_divergence(x1, x2, p-1)
            dist_mat[i][j] = distance(x1, x2, p-1)
    
    mse = 0.0
    for i in range(m):
        predict = 0.0

        indices = np.argsort(dist_mat[i])
        
        # choose k neighbors
        for nb in indices[1:k+1]:
            predict += train_data[nb][p-1] 
            
        predict /= k
        
        y = test_data[i][p-1]
        #print y, predict
        
        mse += (y-predict)*(y-predict)
    
    mse /= m
    #print "mse: " + str(mse)
    
    return mse

    
def get_mean_mse(data):
    #print data
    
    n = data.shape[0]
    p = data.shape[1]
    mean = 0.0
    for i in range(n):
        mean += data[i][p-1]
    mean /= n
    #print mean
    
    mse = 0.0
    for i in range(n):
        mse += (data[i][p-1] - mean)*(data[i][p-1] - mean)
        
    #print mse
    mse /= n

    print "mean mse: " + str(mse)
    return mse
        

    
if __name__ == '__main__':
    for label in LABELS:
        print '================================================================'
        print label
        #fp = os.path.join(CUR_DIR, 'data', 'matrix_data', 'for_knn', 'freq_histogram',  label + '.csv')
        fp = os.path.join(CUR_DIR, 'data', 'matrix_data', 'for_knn', 'wifi_features',  label + '.csv')
        #data = np.loadtxt(fp, delimiter=",")
        data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
        replace_nan(data, 4)
        fold = 5
        n = data.shape[0]
        m = data.shape[1]
        test_data = np.empty([n/fold, m])
        train_data = np.empty([n-n/fold, m])
    
        k_mse = []  
        for k in range(1, n):
            #print "k: %d" % k
            avg_mse = 0.0
            for j in range(fold):
                #print "fold %d" % j
                for i, x in enumerate(data):
                    if i%fold == j:
                        test_data[i/fold] = data[i]
                    else:
                        train_data[(i/fold)*(fold-1)+i%fold-1] = data[i]
                       
                mse = knn(train_data, test_data, k)
    
                avg_mse += mse
            avg_mse /= fold
            k_mse.append((k, avg_mse))
            #print "average mse: " + str(avg_mse)
            
        k_mse = sorted(k_mse, key=lambda item:item[1])
        #pprint(k_mse)
        best = k_mse[0]
        print "best k: " + str(best[0])
        print "average mse: " + str(best[1])
        
        mean_mse = get_mean_mse(data)
        
        diff = mean_mse - avg_mse
        
        print "diff: " + str(diff)

            

    

