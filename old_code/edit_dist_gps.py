import os
import time
import copy
from datetime import datetime
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np

from utilities import edit_dist, get_y, get_all_y
from utilities import write_feature_to_csv
from bag_of_words import get_change_date, get_complete_days

cur_dir = os.path.dirname(os.path.realpath(__file__))

    
def get_seq(fp, by_complete_dates):
    if by_complete_dates:
        by_dates = by_complete_dates
    else:
        by_dates = {}
        
        fr = open(fp, 'rU') 
        lines = fr.readlines()
        for line in lines:
            #print line
            atts = line.strip('\n').split(",")
            dt = atts[1][:9]
            
            if dt not in by_dates:
                by_dates[dt] = []
                by_dates[dt].append(atts[5])
            else:
                by_dates[dt].append(atts[5])
            
        by_dates = sorted(by_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))  
                
    in_loc_count = []
    for idx, pair in enumerate(by_dates):
        in_loc_count.append((pair[0], []))
        entries = pair[1]
        for i, entry in enumerate(entries):
            if i==0:                
                m_entry = [copy.deepcopy(entry)]
                m_entry.append(i)
                in_loc_count[idx][1].append(m_entry)
            else:
                if entry != entries[i-1]:
                    m_entry = [copy.deepcopy(entry)]
                    m_entry.append(i)
                    in_loc_count[idx][1].append(m_entry)                                
    #pprint(in_loc_count) 
     
    for idx, pair in enumerate(in_loc_count):
        entries = pair[1]
        for i, entry in enumerate(entries):
            if i==len(entries)-1:
                end_index = len(by_dates[idx][1])-1
            else:
                end_index = entries[i+1][1]-1
            entry.append(end_index)
    #pprint(in_loc_count)
     
    
    for idx, pair in enumerate(in_loc_count):
        #print pair[0]
        in_loc_count[idx] = (pair[0], [])
        entries = pair[1]
        for i, entry in enumerate(entries):
            #print entry
            count = entry[2] - entry[1] + 1
            if count > 1:
                items = entry[0].split(';')
                in_loc_count[idx][1].append(items[0])   
    #pprint(in_loc_count)
    
    return in_loc_count
    
#     dt_locs = []
#     for idx, pair in enumerate(in_loc_count):
#  
#         locs = pair[1]
#         locs_merge = []
#         for i, loc in enumerate(locs):
#             if i == 0:
#                 locs_merge.append(loc)
#             else:
#                 if loc != locs[i-1]:
#                     locs_merge.append(loc)
#         dt_locs.append((pair[0], locs_merge))   
#          
#     #pprint(dt_locs) 
#     return dt_locs

def per_subject(fp, sample_days, by_complete_dates):

    locs = get_seq(fp, by_complete_dates)
    #pprint(locs)

    seqs = []

    for dt, entries in locs:
        if not dt in sample_days:
            continue
        dt_obj = datetime.strptime(dt, "%d%b%Y")
        weekday = dt_obj.strftime("%A")
        if weekday == 'Saturday' or weekday == 'Sunday':
            continue
        seqs.append(entries)
    #result.append((day, seqs))
        
    #pprint(seqs)
            
    return seqs



def get_avg_edit_dist(seqs):

    n = len(seqs)
         
    avg = 0
    dists = np.zeros((n, n))
    for i in range(n):
        for j in range(i,n):
            print '========'
            dists[i][j] = edit_dist(seqs[i], seqs[j])
            print seqs[i]
            print seqs[j]
            avg += dists[i][j]
      
    avg /= float(n*(n-1)/2)
  
    return avg


def get_feature():

    id_feature = {}
    addr_dir = os.path.join(cur_dir, 'data', 'gps_osm')
    for file in os.listdir(addr_dir):
        if not file.endswith('.csv'):
            continue
        fp = os.path.join(addr_dir, file)
        id = file.split('.')[0][-2:]
        
        change_dt = get_change_date(fp)
        complete, by_complete_dates = get_complete_days(fp, change_dt)
        
        #pprint(by_complete_dates)
        if len(complete) < 30:
            continue
        
        print 
        print 'subject id: ' + id
        

        sample_days = complete[:30]
        
#         seqs = per_subject_by_weekdays(fp, sample_days)
#         result = get_weekday_sum_avg_edit_dist(seqs)
        
        seqs = per_subject(fp, sample_days, by_complete_dates)
        #pprint(seqs)
        result = get_avg_edit_dist(seqs)

        id_feature[id] = result
    return id_feature


    
    
if __name__ == '__main__':
#     fp = os.path.join(cur_dir, 'data', 'gps_osm', 'wifigps_addr_04.csv')
#     per_subject_by_weekdays(fp)
    
    #all_subjects_plot()
    id_edit_dist = get_feature()
    write_feature_to_csv('gps_edit_dist', id_edit_dist)

    