import math
from pprint import pprint
import numpy as np

from utilities import get_y, z_score_normalize
from utilities import LABELS
from utilities import distance, edit_dist, KL_divergence


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
            dist_mat[i][j] = KL_divergence(x1, x2, p-1)
    
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
    #print mse
    
    return mse

    
def get_mse(data):
    #print data
    
    n = data.shape[0]
    p = data.shape[1]
    mean = 0.0
    for i in range(n):
        #print data[i][p-1]
        mean += data[i][p-1]
    mean /= n
    #print mean
    
    mse = 0.0
    for i in range(n):
        mse += (data[i][p-1] - mean)*(data[i][p-1] - mean)
        
    #print mse
    mse /= n
    
    print mse
        

if __name__ == '__main__':
    for label in LABELS:
        print '==============='
        print label
        fp = r"data\matrix_data\for_knn\freq_histogram_" + label + '.csv' 
        data = np.loadtxt(fp, delimiter=",")
        get_mse(data)
    
        k_accs = []
        fold = 5
        for k in range(1, 20, 2):
            print k
            avg_mse = 0.0
            for j in range(fold):
                #print 'fold ' + str(j)
      
                train_data = []
                test_data = []
                  
                for i, x in enumerate(data):
                    if i%fold == j:
                        test_data.append(data[i].tolist())
                    else:
                        train_data.append(data[i].tolist())
                       
                mse = knn(np.array(train_data), np.array(test_data), k)
    
                avg_mse += mse
            avg_mse /= fold
            print "average mse: " + str(avg_mse)

            

    

