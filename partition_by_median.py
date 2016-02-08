import numpy as np
import os

from utilities import LABELS, replace_nan

fp = r"data\matrix_data\all_wifi_features.csv"
data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)

        
y_cols = range(4,19)

for col in y_cols:
    replace_nan(data, col)
    label = LABELS[col-4]  
    print '--------'
    print label
    
    output_fp = os.path.join('data', 'matrix_data', 'logit', "wifi_features_" + label + '.csv')
    fw = open(output_fp, 'a')
    
    median = np.median(data[:, col])
    print median
    
    for i in range(data.shape[0]):
        line = [str(x) for x in data[i][1:4].tolist()]
        #print type(data[i][col])
        if data[i][col] > median:
            label = 1
        else:
            label = 0
        line.append(str(label))
        fw.write(','.join(line) + '\n')
    fw.close()