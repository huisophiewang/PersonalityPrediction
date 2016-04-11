import os

import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas
import patsy
from patsy.builtins import Q
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
        
        
def write_single_vrb_to_txt(input_fp, output_dir, feature):    
    df = pandas.read_csv(input_fp)

    for i in range(len(LABELS)):
        #response = 'activity'
        response = LABELS[i]
        y, X = dmatrices('%s ~ Q("%s")' % (response, feature), data=df)
        mod = sm.OLS(y, X)
        res = mod.fit()
    
        if res.pvalues[1] <= 0.05:
            output_folder = os.path.join(output_dir, response)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            fw = open(os.path.join(output_folder, 'summary_' + feature + '.txt'), 'a')
            fw.write("#####################################################################################################\n")
            fw.write(response + '\n')
            sum = str(res.summary())
            fw.write(sum + '\n')
            fw.close()
            
def freq_pattern():
    folder = 'days30_support20'
    input_dir = os.path.join(CUR_DIR, 'data', 'matrix_data', 'freq_pattern', folder)
    output_dir = output_fp = os.path.join(CUR_DIR, 'data', 'summary', 'feature selection', folder)
    for file in os.listdir(input_dir):
        if not file.startswith("feature_"):
            continue
         
        #file = 'feature_baker-berry.csv'
        input_fp = os.path.join(input_dir, file)    
        feature = file[8:-4]
        print feature
        write_single_vrb_to_txt(input_fp, output_dir, feature)
        

if __name__ == '__main__':
    #feature = 'edit_dist'
    #single_vrb(feature)

    #multi_vrb()
    
    freq_pattern()

    

    