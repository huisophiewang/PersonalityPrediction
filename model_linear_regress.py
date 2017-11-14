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
        y, X = dmatrices('%s ~ Q("%s")' % (TRAITS[i], feature), data=df)
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
    

    feature = 'len_mean_oncampus'
    feature = 'len_var_oncampus'
    feature = 'start_time_avg_oncampus'
    feature = 'start_time_var_oncampus'
    feature = 'end_time_avg_oncampus'
#     feature = 'end_time_var_oncampus'
#     feature = 'edit_dist'
#     
#     feature = 'gps_entropy'
#     feature = 'gps_avg_radius'
#     feature = 'gps_avg_area'
#     
#     feature = 'nearby_daily_oncampus'
#     feature = 'nearby_timestamp_oncampus'
#     feature = 'nearby_timestamp_30days_oncampus'
#     feature = 'nearby_total_30days_oncampus'
#     feature = 'nearby_total_30days_oncampus_noclass'
#      
#     feature = 'num_days_activity_oncampus'
#     
#     feature = 'conver_freq_oncampus'
#     feature = 'conver_dur_avg_oncampus'
#     feature = 'conver_dur_total_oncampus'
#     
#     feature = 'late_time_var_oncampus'
#     feature = 'late_time_avg_oncampus'
# 
# 
#     feature = 'fp_53_commons;baker-berry'
#     feature = 'fp_baker-berry;lsb'
#     feature = 'fp_kemeny;baker-berry'
    #feature = 'fp_sport-venues'
    #feature = 'fp_baker-berry;kemeny'
    #feature = 'fp_lsb;baker-berry;kemeny'
    #feature = 'fp_occum'
    #feature = 'fp_53_commons;sudikoff'
    

    
    single_vrb(feature)
#     plot_feature(feature)

###################################################################################################

#     features = ['len_var_mon', 'len_var_tue', 'len_var_wed', 'len_var_thr', 'len_var_fri']
#     features = ['start_time_var_mon','start_time_var_tue','start_time_var_wed','start_time_var_thr','start_time_var_fri']
#     features = ['end_time_var_mon','end_time_var_tue','end_time_var_wed','end_time_var_thr','end_time_var_fri']
# # # #   
    #features = ['daily_day_oncampus', 'daily_evening_oncampus', 'daily_night_oncampus']
#     features = ['daily_day_oncampus_noclass', 'daily_evening_oncampus_noclass', 'daily_night_oncampus_noclass']
#     features = ['daily_day_unique_oncampus', 'daily_evening_unique_oncampus', 'daily_night_unique_oncampus']
#     features = ['day_entropy_oncampus', 'evening_entropy_oncampus', 'night_entropy_oncampus']
#     features = ['day_entropy_oncampus_30days', 'evening_entropy_oncampus_30days', 'night_entropy_oncampus_30days']
# # # # #     
#     features = ['stat_rate_oncampus', 'walk_rate_oncampus', 'run_rate_oncampus']
    #features = ['stat_total_oncampus', 'walk_total_oncampus', 'run_total_oncampus']
#     features = ['stat_daily_oncampus', 'walk_daily_oncampus', 'run_daily_oncampus']
# # # # # 
#     features = ['conver_freq_daytime_oncampus', 'conver_freq_evening_oncampus', 'conver_freq_night_oncampus']
# # # # #     
#     features = ['early_oncampus', 'late_oncampus', 'absent_oncampus'] 
#     features = ['ontime_rate_oncampus', 'absent_rate_oncampus']
# # # # #     
#     features = ['days_oncampus', 'views_oncampus', 'contributions_oncampus', 'questions_oncampus', 'notes_oncampus', 'answers_oncampus']

 
#     trait = 'consc'
#     multi_feature_single_trait(features, trait)
#     plot_multi_feature(features, trait)

    
    

    
    
    