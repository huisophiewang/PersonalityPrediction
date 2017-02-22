import os
import math
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas
import patsy
from patsy.builtins import Q
from patsy.highlevel import dmatrices, dmatrix

from util import CUR_DIR, TRAITS

def single_vrb(feature):
    input_fp = os.path.join(CUR_DIR, 'result', 'feature', feature + '.csv')
    df = pandas.read_csv(input_fp)
    print df
    for i in range(len(TRAITS)):
        print "#####################################################################################"
        print TRAITS[i]
        y, X = dmatrices('%s ~ %s' % (TRAITS[i], feature), data=df)
        mod = sm.OLS(y, X)
        res = mod.fit()
        print res.summary()
        
def multi_feature_single_trait(feature_names, trait):
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
    
def plot_y_histogram():
    #fr = open(r'dataset\survey\BigFivePre.csv', 'rU')
    fr = open(r'dataset\survey\BigFivePre_oncampus.csv', 'rU')
    fr.readline()
    
    all_y = [[],[],[],[],[]]
    for line in fr.readlines():
        items = line.strip('\n').split(",")
        for idx, item in enumerate(items[1:]):
            #print idx, item
            all_y[idx].append(float(item))
    

    f, axarr = plt.subplots(5, sharex=True)
    axarr[0].set_title('Histograms of traits')
    for i in range(5):
        y = all_y[i]
        axarr[i].set_ylabel(TRAITS[i])
        axarr[i].hist(np.log10(y))
    
    plt.show()
    
def plot_y_boxplot():
    #data = np.genfromtxt(r'dataset\survey\BigFivePre.csv', delimiter=",", dtype=float, skip_header=1)
    data = np.genfromtxt(r'dataset\survey\BigFivePre_oncampus.csv', delimiter=",", dtype=float, skip_header=1)
    #plt.boxplot([data[:,1], data[:,2], data[:,3], data[:,4], data[:,5]])
    #plt.boxplot(data[:,2])
    plt.boxplot(np.log10(data[:,2]))
    #plt.xticks([1,2,3,4,5], ['E', 'A', 'C', 'N', 'O'])
    plt.show()
    
def plot_x_histogram():
    data = np.genfromtxt(os.path.join('result', 'feature', 'num_days_activity_oncampus.csv'), delimiter=",", dtype=float, skip_header=1)
    plt.hist(data[:,1])
    plt.show()
    
    
    
def plot_other(file_path):
    fr = open(file_path, 'rU')
    cols = fr.readline()
    m = len(cols.split(',')) - 1
    
    all = []
    for i in range(m):
        all.append([])

    for line in fr.readlines():
        items = line.strip('\n').split(",")
        for idx, item in enumerate(items[1:]):
            all[idx].append(float(item))

    f, axarr = plt.subplots(m, sharex=True)
    for i in range(m):
        y = all[i]
        axarr[i].hist(y)
    plt.show()       
           
if __name__ == '__main__':
    #plot_y_histogram()
    #plot_y_boxplot()
    #plot_x_histogram()
    
    feature = 'len_var'
    feature = 'len_var_oncampus'
    #feature = 'len_mean_oncampus'
#     feature = 'avg_edit_dist'
    feature = 'start_time_var_oncampus'
    feature = 'end_time_var_oncampus'
    

#     feature = 'late_var'
#     feature = 'grade'
#     feature = 'reply_count'
#     feature = 'q1'
#     feature = 'q2'
#     feature = 'q3'

#     feature = 'len_var_offcampus'
#     feature = 'start_time_var_offcampus'
#     feature = 'end_time_var_offcampus'
#     feature = 'start_time_var_all'
#     feature = 'end_time_var_all'
#     feature = 'len_var_all'

    #feature = 'late_time_var'
    #feature = 'late_time_var_oncampus'
    
    #feature = 'conver_freq'
    #feature = 'conver_freq_oncampus'
    #feature = 'conver_dur_avg_oncampus'
    #feature = 'conver_dur_total_oncampus'
    
#     feature = 'num_days_activity'
    feature = 'num_days_activity_oncampus'
    #feature = 'num_days_audio'
    #feature = 'num_days_bluetooth_oncampus'
    
    #feature = 'nearby_daily'
#     feature = 'nearby_timestamp'
#     feature = 'nearby_total'
    #feature = 'nearby_entropy_day'
    #feature = 'nearby_entropy_night'
    #feature = 'nearby_entropy_evening'
    #feature = 'nearby_entropy'
    #feature = 'nearby_friends_evening'
    #feature = 'nearby_friends'
    feature = 'nearby_total_30days_oncampus'
    feature = 'nearby_entropy_30days_oncampus'
    #feature = 'nearby_total_30days_oncampus_noclass'
    #feature = 'nearby_entropy_30days_oncampus_noclass'
    #feature = 'nearby_num_unique_30days_oncampus'
    #feature = 'nearby_timestamp_30days_oncampus'
    #feature = 'nearby_num_friends_30days_oncampus'
    #feature = 'nearby_daily_oncampus'
    #feature = 'nearby_timestamp_oncampus'
    #feature = 'nearby_total_oncampus'
    #feature = 'late_time_var_oncampus'
    
    #feature = 'fp_bakerberryhopkins' # discard
    #feature = 'fp_bakerberrykemeny' # discard
    #feature = 'fp_bakerberrylsb'
    #feature = 'fp_sudikoffhopkins'
    #feature = 'fp_occum'
    #feature = 'fp_sportvenues'

    
    single_vrb(feature)
    plot_feature(feature)
    
    #features = ['early', 'late', 'absent']   
    #features = ['early_oncampus', 'late_oncampus', 'absent_oncampus'] 
    #features = ['days', 'views', 'contributions', 'questions', 'notes', 'answers']
    features = ['days_oncampus', 'views_oncampus', 'contributions_oncampus', 'questions_oncampus', 'notes_oncampus', 'answers_oncampus']
#     features = ['breakfast', 'lunch', 'supper', 'snack']
#     features = ['breakfast_var', 'lunch_var', 'supper_var', 'snack_var']

    #features = ['stat_total', 'walk_total', 'run_total']
    #features = ['stat_rate', 'walk_rate', 'run_rate']
    #features = ['stat_rate_oncampus', 'walk_rate_oncampus', 'run_rate_oncampus']
    #features = ['stat_rate', 'act_rate']
    #features = ['stat_total', 'act_total']
    #features = ['stat_daily', 'walk_daily', 'run_daily']
    
    #features = ['daily_day_oncampus', 'daily_evening_oncampus', 'daily_night_oncampus']
    #features = ['daily_day_oncampus_noclass', 'daily_evening_oncampus_noclass', 'daily_night_oncampus_noclass']
    #features = ['daily_day_unique_oncampus', 'daily_evening_unique_oncampus', 'daily_night_unique_oncampus']
    #features = ['ontime_rate_oncampus', 'absent_rate_oncampus']
    #features = ['day_entropy_oncampus', 'evening_entropy_oncampus', 'night_entropy_oncampus']
    #features = ['day_entropy_oncampus_30days', 'evening_entropy_oncampus_30days', 'night_entropy_oncampus_30days']
    #features = ['conver_freq_daytime_oncampus', 'conver_freq_evening_oncampus', 'conver_freq_night_oncampus']
    
#     trait = 'extra'
#     multi_feature_single_trait(features, trait)
#     plot_multi_feature(features, trait)

    
    

    
    
    