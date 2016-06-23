from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pprint
pp = pprint.PrettyPrinter(width=200)

def get_pair():
    fp1 = r"dataset\survey\PerceivedStressScalePre.csv"
    d1= np.genfromtxt(fp1, delimiter=',', dtype=None, unpack=True, names=True)
    ids = [x[0] for x in d1]
    x1 = [x[1] for x in d1]
    
    #########################################################
    
    fp2 = r"dataset\survey\BigFivePre.csv"
    d2= np.genfromtxt(fp2, delimiter=',', dtype=None, unpack=True, names=True)
    #print d2
    
    #bigfive = np.genfromtxt(fp2, delimiter=',', dtype=None, unpack=True, skip_header=1, usecols=(1,2,3,4,5))
    #print np.corrcoef(bigfive)
    x2 = []
    for x in d2:
        if x[0] in ids:
            x2.append(x[4])
            
    #########################################################
    
    fp3 = r'result\feature\conver_dur.csv'
    d3 = np.genfromtxt(fp3, delimiter=',', dtype=None, unpack=True, skip_header=1, usecols=(0,1))
    x3 = []
    for x in d3:
        if 'u%02d' % x[0] in ids:
            x3.append(x[1])
    
    #########################################################

    fp4 = r'dataset\education\grades.csv'
    d4 = np.genfromtxt(fp4, delimiter=',', dtype=None, unpack=True, skip_header=1, usecols=(0,1))
    
    response = x1
    feature = x2
    
    return (feature, response)


def regress(x, y):
    x = sm.add_constant(x)
    mod = sm.OLS(y, x)
    res = mod.fit()
    print res.summary()
    
def pearson(x, y):
    print
    print "Pearson Correlation:"
    print pearsonr(x, y)
    
def plot(x, y):
    plt.plot(x, y, 'ro')
    plt.show()
        
if __name__ == '__main__':
    (x, y) = get_pair()
    regress(x, y)
    pearson(x, y)
    plot(x, y)


    