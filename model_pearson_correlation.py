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
    #print np.mean(x)
    #print x
    
    fp_trait = os.path.join('dataset','survey','BigFivePre_oncampus.csv')
    agr = np.genfromtxt(fp_trait, delimiter=",", dtype=float, skip_header=1)[:,2]
    #print agr
    #print pearsonr(x, agr)
 
    for i in range(2, 7):
        y = data[:, i]
        print pearsonr(x, y)
        
def pearson_multi_features(feature_names):
    
    fp_trait = os.path.join('dataset','survey','BigFivePre_oncampus.csv')
    agr = np.genfromtxt(fp_trait, delimiter=",", dtype=float, skip_header=1)[:,2]
    
    fp = os.path.join('result', 'feature', '%s.csv' % '-'.join(feature_names))
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    data = data[:,1:]
    num = len(feature_names)
    for i in range(num):
        print '--------------------'
        print feature_names[i]
        x = data[:, i]
        #print np.mean(x)
        print pearsonr(x, agr)
#         for j in range(num, num+5):
#             y = data[:, j]
#             print pearsonr(x, y)
    
    

def trait_corr_matrix():
    #fp = os.path.join('dataset', 'survey', 'BigFivePre.csv')
    fp = os.path.join('dataset', 'survey', 'BigFivePre_oncampus.csv')
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
    
    feature = 'len_var_oncampus'
    feature = 'len_mean_oncampus'
    feature = 'start_time_var_oncampus'
    feature = 'start_time_avg_oncampus'
    feature = 'end_time_var_oncampus'
    feature = 'end_time_avg_oncampus'
    #feature = 'edit_dist'
    
#     feature = 'num_days_bluetooth_oncampus'
#     feature = 'nearby_entropy_30days_oncampus'
#     feature = 'nearby_timestamp_oncampus'
    #feature = 'nearby_timestamp_30days_oncampus'
    #feature = 'nearby_daily_oncampus'
    #feature = 'nearby_total_30days_oncampus'
    
    #feature = 'late_time_var_oncampus'
    #feature = 'num_days_activity_oncampus'
        #feature = 'conver_freq'
    #feature = 'num_days_activity'
    #feature = 'num_days_audio'
    
    #feature = 'fp_53_commons;sudikoff'
#     feature = 'fp_occum'
    #feature = 'fp_53_commons;baker-berry'
    #feature = 'fp_kemeny;baker-berry'
#     feature = 'fp_baker-berry;kemeny'
#     feature = 'fp_lsb;baker-berry;kemeny'
#     feature = 'fp_sport-venues'

    #feature = 'gps_avg_area'

    pearson_single_feature(feature)
    
    
    #features = ['len_var_mon', 'len_var_tue', 'len_var_wed', 'len_var_thr', 'len_var_fri']
    #features = ['start_time_var_mon','start_time_var_tue','start_time_var_wed','start_time_var_thr','start_time_var_fri']
    #features = ['end_time_var_mon','end_time_var_tue','end_time_var_wed','end_time_var_thr','end_time_var_fri']
    
    #features = ['daily_day_oncampus', 'daily_evening_oncampus', 'daily_night_oncampus']
#     features = ['day_entropy_oncampus_30days', 'evening_entropy_oncampus_30days', 'night_entropy_oncampus_30days']
#     features = ['daily_day_unique_oncampus', 'daily_evening_unique_oncampus', 'daily_night_unique_oncampus']
#     features = ['days_oncampus', 'views_oncampus', 'contributions_oncampus', 'questions_oncampus', 'notes_oncampus', 'answers_oncampus']
#     features = ['early_oncampus', 'late_oncampus', 'absent_oncampus'] 
#     features = ['stat_rate_oncampus', 'walk_rate_oncampus', 'run_rate_oncampus']
#     features = ['conver_freq_daytime_oncampus', 'conver_freq_evening_oncampus', 'conver_freq_night_oncampus']

    
    #pearson_multi_features(features)



    