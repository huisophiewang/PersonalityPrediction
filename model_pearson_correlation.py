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



def regress(x, y):
    x = sm.add_constant(x)
    mod = sm.OLS(y, x)
    res = mod.fit()
    print res.summary()
    

def plot(x, y):
    plt.plot(x, y, 'ro')
    plt.show()
        
if __name__ == '__main__':
    #get_pair()
#     regress(x, y)
#     pearson(x, y)
#     plot(x, y)
    #pearson_all_features()
    
    feature_name = 'conver_freq'
    feature_name = 'nearby_daily'
    
    pearson_single_feature(feature_name)
    



    