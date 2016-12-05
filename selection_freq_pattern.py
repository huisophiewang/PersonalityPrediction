import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas
import patsy
from patsy.builtins import Q
from patsy.highlevel import dmatrices, dmatrix

from util import CUR_DIR, TRAITS

def freq_pat_selection():
    input_dir = os.path.join(CUR_DIR, 'result', 'feature', 'freq_pat', 'support40')
    output_dir = os.path.join(CUR_DIR, 'result', 'feature', 'freq_pat_select', 'support40')
    for file in os.listdir(input_dir):
        input_fp = os.path.join(input_dir, file)    
        feature = file[:-4]
        #print feature
        df = pandas.read_csv(input_fp)
        for i in range(len(TRAITS)):
            response = TRAITS[i]
            #print response
            #y, X = dmatrices('%s ~ %s' % (response, feature), data=df)
            y, X = dmatrices('%s ~ Q("%s")' % (response, feature), data=df)
            mod = sm.OLS(y, X)
            res = mod.fit()
            if res.pvalues[1] <= 0.1:
                output_folder = os.path.join(output_dir, response)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                output_fp = os.path.join(output_folder, feature + '.txt')
                fw = open(output_fp, 'a')
                fw.write("#####################################################################################################\n")
                fw.write(response + '\n')
                fw.write(str(res.summary()) + '\n')
                fw.close()
                
if __name__ == '__main__':
    freq_pat_selection()
    