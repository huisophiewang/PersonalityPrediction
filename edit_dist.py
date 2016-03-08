import csv
import copy
from pprint import pprint
from collections import OrderedDict
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from utilities import edit_dist, get_y, write_feature_to_csv, write_raw_feature_to_csv
from utilities import CUR_DIR, WIFI_COMMON_DAYS, WIFI_OFF_CAMPUS
from utilities import get_wifi_seqs

  


def get_seqs_by_weekdays(fp):
    result = []
    dt_locs = get_wifi_seqs(fp, 60*10, 20)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for day in days:
        #print day
        #pprint(locs)
        seqs = []
        seq_freq = {}
        avg_seq_len = 0
    
        for dt, entries in dt_locs:
            dt_obj = datetime.strptime(dt, "%d%b%Y")
            weekday = dt_obj.strftime("%A")
            #if weekday != 'Sunday' and weekday != 'Saturday':
            if weekday == day:
         
                seqs.append(entries)

        #pprint(seqs)
        result.append((day, seqs))
        
    
    for pair in result:
        print pair[0]
        for entry in pair[1]:
            print entry
 
    return result
    
def get_weekday_sum_avg_edit_dist(weekday_seqs):
    #fp = r"C:\Users\Sophie\Smart Phone Project Local\by subjects\wifigps_subject04.csv"
    sum = 0
    
    for pair in weekday_seqs:
        seqs = pair[1]
        n = len(seqs)
         
        avg = 0
        dists = np.zeros((n, n))
        for i in range(n):
            for j in range(i,n):
                dists[i][j] = edit_dist(seqs[i], seqs[j])
                avg += dists[i][j]
          
        avg /= float(n*(n-1)/2)
      
        sum += avg
    print sum
    return sum

def get_avg_edit_dist(seqs):
    n = len(seqs)
     
    avg = 0
    dists = np.zeros((n, n))
    for i in range(n):
        for j in range(i,n):
            dists[i][j] = edit_dist(seqs[i], seqs[j])
            avg += dists[i][j]
      
    avg /= float(n*(n-1)/2)
    return avg

def get_feature():
    id_feature = {}
    addr_dir = os.path.join(CUR_DIR, 'data', 'by_subjects')
    for file in os.listdir(addr_dir):
        if not file.endswith('.csv'):
            continue
        
        id = file.split('.')[0][-2:]
        if int(id) >= 45:
            continue     
        if id in WIFI_OFF_CAMPUS:
            continue
        fp = os.path.join(addr_dir, file)
        print '----------'
        print 'id: ' + id
        
        seqs = get_wifi_seqs(fp, 60*10, 20)
        #print seqs
        #print len(seqs)
        result = get_avg_edit_dist(seqs)
        
        id_feature[id] = result
        
    return id_feature
        
    


if __name__ == '__main__':  


#     fp = r'data\by subjects\wifigps_subject08.csv'
#     get_avg_edit_dist(fp)
    

    id_edit_dist = get_feature()
    #write_feature_to_csv('edit_dist', id_edit_dist)
    #plot_all(id_edit_dist)
    write_raw_feature_to_csv('edit_dist', id_edit_dist)

    
    
    
    
    
    
    
    
    
    
    
    
    