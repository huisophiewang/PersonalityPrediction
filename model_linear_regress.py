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
        
        

        
def plot_feature(feature):
    input_fp = os.path.join(CUR_DIR, 'result', 'feature', feature + '.csv')
    df = pandas.read_csv(input_fp)
    m_data = df.as_matrix()

    x = m_data[:,1]

    f, axarr = plt.subplots(5, sharex=True)
    
    for i in range(5):
        y = m_data[:,i+2]
        axarr[i].plot(x, y, 'ro')

    plt.show()
    
         
if __name__ == '__main__':
#     feature = 'feature_len_var'
#     feature = 'start_time_var'
#     feature = 'end_time_var'
    feature = 'conver_freq'
#     single_vrb(feature)
#     plot_feature(feature)
    
#     input_fp = os.path.join(CUR_DIR, 'result', 'feature', feature + '.csv')
#     df = pandas.read_csv(input_fp)
#     y, X = dmatrices('%s ~ %s' % ('extra', 'neuro'), data=df)
#     mod = sm.OLS(y, X)
#     res = mod.fit()
#     print res.summary()
    
    
    