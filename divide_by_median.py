import os
import numpy as np

def divide(trait):
    input_fp = os.path.join('result', 'feature', 'all_features_fp_%s.csv' % trait)
    data = np.genfromtxt(input_fp, delimiter=",", dtype=float, names=True)
    header = data.dtype.names
    data = data.view((float, len(data.dtype.names)))
    
    #print data
    print ','.join(header)
    
    # print data.shape
    # print data['extra']
    md = np.median(data[:,-1])
    print md
    #y = (data[:,-1] > md).astype(int)
    y = (data[:,-1] >= md).astype(int)
    if trait == 'agrbl':
        y = (data[:,-1] < md).astype(int)
    print y
    
    new_data = np.append(data[:,:-1], np.array([y]).T, axis=1)
    #print new_data
    
    output_fp = os.path.join('result', 'feature', 'all_features_fp_%s_cls.csv' % trait)
    np.savetxt(output_fp, new_data, fmt='%1.3f', delimiter=",", header=','.join(header))
    
if __name__ == '__main__':
    divide(trait='agrbl')