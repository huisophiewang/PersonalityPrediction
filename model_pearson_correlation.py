import os
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pprint
pp = pprint.PrettyPrinter(width=200)

def pearson_all_features():
#     fp1 = r"dataset\survey\PerceivedStressScalePre.csv"
#     d1= np.genfromtxt(fp1, delimiter=',', dtype=None, unpack=True, names=True)
#     print d1
#     ids = [x[0] for x in d1]
#     x1 = [x[1] for x in d1]
#     print x1
    
    fp = os.path.join('result', 'feature', 'all_features.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #print data
    
    y = data[:,15]
    print y
    for i in range(1, 13):
        print '----'
        print i+1
        x = data[:,i]
        print pearsonr(x, y)

def pearson_single_feature(feature_name):  
    fp = os.path.join('result', 'feature', '%s.csv' % feature_name)
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    #print data
    x = data[:,1]
    print x
    for i in range(2, 7):
        y = data[:, i]
        print pearsonr(x, y)
        
def pearson_multi_features(feature_names):
    fp = os.path.join('result', 'feature', '%s.csv' % '-'.join(feature_names))
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    data = data[:,1:]
    num = len(feature_names)
    for i in range(num):
        print '--------------------'
        print feature_names[i]
        x = data[:, i]
        for j in range(num, num+5):
            y = data[:, j]
            print pearsonr(x, y)
    
    

def trait_corr_matrix():
    fp = os.path.join('dataset', 'survey', 'BigFivePre.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    data = data[:,1:]

    corr = np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            corr[i,j] = pearsonr(data[:, i], data[:, j])[0]
    print corr


def regress(x, y):
    x = sm.add_constant(x)
    mod = sm.OLS(y, x)
    res = mod.fit()
    print res.summary()
    

        
if __name__ == '__main__':

    #pearson_all_features()
    #trait_corr_matrix()
    
    feature = 'conver_freq'
    feature = 'nearby_daily'
    feature = 'num_days_activity'
    #feature = 'num_days_audio'
    feature = 'len_var'
    feature = 'start_time_var'
    feature = 'end_time_var'
    feature = 'nearby_entropy'
    feature = 'nearby_timestamp'
    pearson_single_feature(feature)
    
#     features = ['early', 'late', 'absent'] 
#     features = ['days', 'views', 'contributions', 'questions', 'notes', 'answers']  
#     pearson_multi_features(features)



    