import os

import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas
import patsy
from patsy.highlevel import dmatrices, dmatrix

from utilities import CUR_DIR, LABELS

def single_vrb(feature):

    input_fp = os.path.join(CUR_DIR, 'data', 'matrix_data', 'feature_' + feature + '.csv')
    
    df = pandas.read_csv(input_fp)
    print df

    for i in range(len(LABELS)):
        
        print "#####################################################################################################"
        print LABELS[i]
    
        y, X = dmatrices('%s ~ %s' % (LABELS[i], feature), data=df)
        mod = sm.OLS(y, X)
        res = mod.fit()
        print res.summary()
        
def multi_vrb():
    input_fp = os.path.join(CUR_DIR, 'data', 'matrix_data', 'all_wifi_features.csv')
    df = pandas.read_csv(input_fp)
    print df
    for i in range(len(LABELS)):
         
        print "#####################################################################################################"
        print LABELS[i]
     
        y, X = dmatrices('%s ~ edit_dist + start_time_var + end_time_var' % LABELS[i], data=df)
        mod = sm.OLS(y, X)
        res = mod.fit()
        print res.summary()
        
def test_in_multi_vrb():
    input_fp = os.path.join(CUR_DIR, 'data', 'matrix_data', 'all_wifi_features.csv')
    df = pandas.read_csv(input_fp)
    print df
    
#     print "#####################################################################################################"
#     y_extra, X_extra = dmatrices('extra ~ edit_dist + end_time_var', data=df)
#     mod_extra = sm.OLS(y_extra, X_extra)
#     res_extra = mod_extra.fit()
#     print res_extra.summary()
#     
#     print "#####################################################################################################"
#     y_neuro, X_neuro = dmatrices('neuro ~ edit_dist + end_time_var', data=df)
#     mod_neuro = sm.OLS(y_neuro, X_neuro)
#     res_neuro = mod_neuro.fit()
#     print res_neuro.summary()
    
    print "#####################################################################################################"
    y, X = dmatrices('activity ~ edit_dist + end_time_var', data=df)
    mod = sm.OLS(y, X)
    res = mod.fit()
    #res.predict()
    print res.summary()
    #print res.resid()
    
    #fig = plt.figure(figsize=(12,8))
    fig = sm.graphics.plot_regress_exog(res, "end_time_var")
    
    plt.show()

if __name__ == '__main__':
    feature = 'len_var'
    single_vrb(feature)

    #multi_vrb()
    #test_in_multi_vrb()