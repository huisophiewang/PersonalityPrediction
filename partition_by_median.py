import numpy as np
import os

from utilities import LABELS, replace_nan



        


def split_y(data, col):    

    replace_nan(data, col)
    print data[:, col]
    median = np.median(data[:, col])
    print median
    
    for i in range(data.shape[0]):
        print '========='
        print data[i,[3,7,8]]
        print data[i, col]
        
        if data[i][col] > median:
            print 1
        else:
            print 0
    
    label = LABELS[col-16] 
    output_fp = os.path.join('data', 'matrix_data', 'logit', "wifi_features_" + label + '.csv')
    fw = open(output_fp, 'a')
      
    for i in range(data.shape[0]):
        line = [str(x) for x in data[i,[3,7,8]].tolist()]
        #print type(data[i][col])
        if data[i][col] > median:
            y = 1
        else:
            y = 0
        line.append(str(y))
        fw.write(','.join(line) + '\n')
    fw.close()
    
    
if __name__ == '__main__': 
    fp = r"data\matrix_data\all_wifi_features.csv"
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    
    y_cols = range(16, 21)
    print y_cols
    
#     for col in y_cols:     
#         label = LABELS[col-16]  
#         print '--------'
#         print label
        
    split_y(data, 16)