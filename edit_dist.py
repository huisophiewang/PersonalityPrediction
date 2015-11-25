import csv
import copy
from datetime import datetime, date, time, timedelta
from pprint import pprint
from collections import OrderedDict
import os

import matplotlib.pyplot as plt
import numpy as np

from utilities import edit_dist, get_y, write_feature_to_csv, plot_all


cur_dir = os.path.dirname(os.path.realpath(__file__))

off_campus = ['00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '56']

common_days = ['22APR2013', '12APR2013', '13APR2013', '19APR2013', '07APR2013', 
               '06APR2013', '09APR2013', '08APR2013', '03APR2013', '15APR2013', 
               '01APR2013', '02APR2013', '14APR2013', '04APR2013', '21APR2013', 
               '05APR2013', '27MAR2013', '10APR2013', '11APR2013', '23APR2013']


def get_major_loc(fp):

    lines = []
     
    by_dates = {}
    with open(fp, 'rU') as fr:
        lines = fr.readlines()
        for line in lines:
            atts = line.strip('\n').split(",")
            #print atts
            dt = atts[1][:9]
            
            if dt not in common_days:
                continue
            
            if dt not in by_dates:
                by_dates[dt] = []
                by_dates[dt].append(atts)
            else:
                by_dates[dt].append(atts)
    
    #pprint(by_dates)
    by_dates = sorted(by_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    #print len(by_dates)
     
    in_loc = []
    for idx, pair in enumerate(by_dates):
        in_loc.append((pair[0], []))
        for entry in pair[1]:
            if entry[4].startswith('in'):
                in_loc[idx][1].append(entry)
    #pprint(in_loc)        
     
    in_loc_duration = []
    for idx, pair in enumerate(in_loc):
        #by_dates[idx] = (pair[0], [])
        in_loc_duration.append((pair[0], []))
        entries = pair[1]
        for i, entry in enumerate(entries):
            if i==0:
                m_entry = copy.deepcopy(entry)
                m_entry.append(i)
                in_loc_duration[idx][1].append(m_entry)
            else:
                loc = entry[4][3:-1]
                loc_prev = entries[i-1][4][3:-1]
                if loc != loc_prev:
                    m_entry = copy.deepcopy(entry)
                    m_entry.append(i)
                    in_loc_duration[idx][1].append(m_entry)            
    #pprint(in_loc_duration) 
     
    for idx, pair in enumerate(in_loc_duration):
        entries = pair[1]
        for i, entry in enumerate(entries):
            if i==len(entries)-1:
                end_index = len(in_loc[idx][1])-1
            else:
                end_index = entries[i+1][5]-1
            entry.append(end_index)
    #pprint(in_loc_duration)
     
      
    for idx, pair in enumerate(in_loc_duration):
           
        in_loc_duration[idx] = (pair[0], [])
        entries = pair[1]
        for i, entry in enumerate(entries):
            time_start = in_loc[idx][1][entry[5]][1]
            time_end = in_loc[idx][1][entry[6]][1]
            duration = datetime.strptime(time_end, "%d%b%Y:%H:%M:%S") - datetime.strptime(time_start, "%d%b%Y:%H:%M:%S")
            duration = duration.seconds
            if duration > 60*10:
                m_entry = []
                m_entry.append(entry[4])
                m_entry.append(time_start[-8:])
                m_entry.append(time_end[-8:])
                m_entry.append(duration)
                in_loc_duration[idx][1].append(m_entry)     
    #pprint(in_loc_duration)
    
#     # merge
#     dt_locs = []
#     for idx, pair in enumerate(in_loc_duration):
#         #print pair[0]
#         entries = pair[1]
#         locs = [entry[0][3:-1] for entry in entries]
#         #print locs
#         locs_merge = []
#         for i, loc in enumerate(locs):
#             if i == 0:
#                 locs_merge.append(loc)
#             else:
#                 if loc != locs[i-1]:
#                     locs_merge.append(loc)
#         dt_locs.append((pair[0], locs_merge))    
#         #print locs_merge
#     return dt_locs

    dt_locs = []
    for idx, pair in enumerate(in_loc_duration):
        #print pair[0]
        entries = pair[1]
        locs = [entry[0][3:-1] for entry in entries]
        #print locs
 
        dt_locs.append((pair[0], locs))    
        #print locs_merge
    pprint(dt_locs)
    return dt_locs




def per_subject(fp):
   

    locs = get_major_loc(fp)

    seqs = []
    seq_freq = {}
    avg_seq_len = 0

    for dt, entries in locs:
        dt_locs = [entry[0][3:-1] for entry in entries]
        seqs.append(dt_locs)
        
        
#         dt_obj = datetime.strptime(dt, "%d%b%Y")
#         weekday = dt_obj.strftime("%A")
#         if weekday != 'Sunday' and weekday != 'Saturday':
#         #if weekday == day:
# #             print dt_obj
# #             pprint(entries)
#             dt_locs = [entry[0][3:-1] for entry in entries]
#             
#             seqs.append(dt_locs)
#         
#             avg_seq_len += len(dt_locs)
# 
# 
#     num_patterns =  len(seq_freq)
#     avg_seq_len /= float(len(locs))
#     
#     return num_patterns
#     #return avg_seq_len
    
    return seqs

def per_subject_by_weekdays(fp):
    result = []
    dt_locs = get_major_loc(fp)
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
    addr_dir = os.path.join(cur_dir, 'data', 'by_subjects')
    for file in os.listdir(addr_dir):
        if not file.endswith('.csv'):
            continue
        
        id = file.split('.')[0][-2:]
        if int(id) >= 45:
            continue     
        if id in off_campus:
            continue
        fp = os.path.join(addr_dir, file)

#         weekday_seqs = per_subject_by_weekdays(fp)
#         result = get_weekday_sum_avg_edit_dist(weekday_seqs)
        
        seqs = per_subject(fp)
        result = get_avg_edit_dist(seqs)
        
        id_feature[id] = result
        
    return id_feature
        
    


if __name__ == '__main__':  


#     fp = r'data\by subjects\wifigps_subject08.csv'
#     get_avg_edit_dist(fp)
    

    id_edit_dist = get_feature()
    write_feature_to_csv('edit_dist', id_edit_dist)
    plot_all(id_edit_dist)

    
    
    
    
    
    
    
    
    
    
    
    
    