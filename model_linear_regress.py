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
        print "#####################################################################################"
        print traits[i]
        y, X = dmatrices('%s ~ %s' % (traits[i], feature), data=df)
        mod = sm.OLS(y, X)
        res = mod.fit()
        print res.summary()
        
def multi_vrb(feature_names, trait):
    file_name = '-'.join(feature_names) + '.csv'
    input_fp = os.path.join(CUR_DIR, 'result', 'feature', file_name)
    df = pandas.read_csv(input_fp)
    print df
    
    for feature in feature_names:
        print "#####################################################################################"
        print feature
        y, X = dmatrices('%s ~ %s' % (trait, feature), data=df)
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

def plot_multi_feature(feature_names, trait):    
    file_name = '-'.join(feature_names) + '.csv'
    input_fp = os.path.join(CUR_DIR, 'result', 'feature', file_name)
    df = pandas.read_csv(input_fp)

    y = df[trait]
    f, axarr = plt.subplots(len(feature_names), sharex=True)
    for i, feature in enumerate(feature_names):
        x = df[feature]
        axarr[i].plot(x, y, 'ro')
    plt.show()
    
def plot_y():
    fr = open(r'dataset\survey\BigFivePre.csv', 'rU')
    fr.readline()
    
    all_y = [[],[],[],[],[]]
    for line in fr.readlines():
        items = line.strip('\n').split(",")
        for idx, item in enumerate(items[1:]):
            #print idx, item
            all_y[idx].append(float(item))
     
    f, axarr = plt.subplots(5, sharex=True)
    for i in range(5):
        y = all_y[i]
        axarr[i].set_ylabel(traits[i])
        axarr[i].hist(y)
    plt.show()
        
           
if __name__ == '__main__':
    #plot_y()
    
    feature = 'len_var'
    feature = 'start_time_var'
    feature = 'end_time_var'
    feature = 'conver_dur'
    feature = 'conver_freq'
    feature = 'late_var'
    feature = 'grade'

    single_vrb(feature)
    plot_feature(feature)
    
#     features = ['early', 'late', 'absent']
#     trait = 'extra'
#     multi_vrb(features, trait)
#     plot_multi_feature(features, trait)
    
#     features = ['days', 'views', 'contributions', 'questions', 'notes', 'answers']
#     trait = 'openn'
#     multi_vrb(features, trait)
#     plot_multi_feature(features, trait)

#     features = ['breakfast', 'lunch', 'supper', 'snack']
#     trait = 'extra'
#     multi_vrb(features, trait)
#     plot_multi_feature(features, trait)

#     features = ['breakfast_var', 'lunch_var', 'supper_var', 'snack_var']
#     trait = 'consc'
#     multi_vrb(features, trait)
#     plot_multi_feature(features, trait)
    

    
    
    