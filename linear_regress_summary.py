import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas
import patsy
from patsy.builtins import Q
from patsy.highlevel import dmatrices, dmatrix

from util import CUR_DIR, traits

def single_vrb(feature):

    input_fp = os.path.join(CUR_DIR, 'result', 'feature', feature + '.csv')
    
    df = pandas.read_csv(input_fp)
    print df

    for i in range(len(traits)):
        
        print "#####################################################################################################"
        print traits[i]

        y, X = dmatrices('%s ~ %s' % (traits[i], feature), data=df)
        mod = sm.OLS(y, X)
        res = mod.fit()
        print res.summary()
        
        
    m_data = df.as_matrix()
    x = m_data[:,1]
    y = m_data[:,2]
    plt.plot(x, y, 'ro')
    plt.show()
        

        
if __name__ == '__main__':
    feature = 'wifi_features'
    single_vrb(feature)