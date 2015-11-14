import csv
import copy
from datetime import datetime, date, time, timedelta
from pprint import pprint
from collections import OrderedDict
import os

import matplotlib.pyplot as plt
import numpy as np

from utilities import edit_dist, get_y

DATA_DIR = r'data\by subjects'

off_campus = ['00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '56']

common_days = ['22APR2013', '12APR2013', '13APR2013', '19APR2013', '07APR2013', '06APR2013', '09APR2013', '08APR2013', '03APR2013', '15APR2013', '01APR2013', '02APR2013', '14APR2013', '04APR2013', '21APR2013', '05APR2013', '27MAR2013', '10APR2013', '11APR2013', '23APR2013']


def get_major_loc(fp):

    lines = []
     
    by_dates = {}
    with open(fp, 'rU') as fr:
        lines = fr.readlines()
        for line in lines:
            atts = line.strip('\n').split(",")
            #print atts
            dt = atts[1][:9]
            
#             if dt not in common_days:
#                 continue
            
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
    
# merge 
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
   
    result = []
    locs = get_major_loc(fp)
    #print day
    #pprint(locs)
    seqs = []
    seq_freq = {}
    avg_seq_len = 0

    for dt, entries in locs:
        dt_obj = datetime.strptime(dt, "%d%b%Y")
        weekday = dt_obj.strftime("%A")
        if weekday != 'Sunday' and weekday != 'Saturday':
        #if weekday == day:
#             print dt_obj
#             pprint(entries)
            dt_locs = [entry[0][3:-1] for entry in entries]
            
            seqs.append(dt_locs)
        
            avg_seq_len += len(dt_locs)
            dt_locs_str = ','.join(dt_locs)
            if dt_locs_str not in seq_freq:
                seq_freq[dt_locs_str] = 0
                seq_freq[dt_locs_str] += 1
            else:
                seq_freq[dt_locs_str] += 1
                
    seq_freq = sorted(seq_freq.items(), key=lambda x: x[1])    
    #pprint(seq_freq) 
 
     
    num_patterns =  len(seq_freq)
    avg_seq_len /= float(len(locs))
    
    return num_patterns
    #return avg_seq_len

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
    
def get_avg_edit_dist(fp):
    #fp = r"C:\Users\Sophie\Smart Phone Project Local\by subjects\wifigps_subject04.csv"
    sum = 0
    weekday_seqs = per_subject_by_weekdays(fp)
#     for pair in weekday_seqs:
#         seqs = pair[1]
#         n = len(seqs)
#         
#         avg = 0
#         dists = np.zeros((n, n))
#         for i in range(n):
#             for j in range(i,n):
#                 dists[i][j] = edit_dist(seqs[i], seqs[j])
#                 avg += dists[i][j]
#          
#         avg /= float(n*(n-1)/2)
#      
#         sum += avg
    #print sum
    return sum


                
def all_subjects_plot():
    
    id_y, label = get_y(5)

    id_values = {}
    for file in os.listdir(DATA_DIR):
        if not file.endswith('.csv'):
            continue
        subj = file.split('.')[0][-2:]
        

        if int(subj) >= 45:
            continue
        
        if subj in off_campus:
            continue
        
        print subj
        subj = str(int(subj))
        fp = os.path.join(DATA_DIR, file)
        
        result = get_avg_edit_dist(fp)       
        #result = per_subject(fp)
        
        id_values[subj] = result
 
    for id in id_values:
        #print id
        if id in id_y:
            feature = id_values[id]
            id_values[id] = (feature, id_y[id])
        else:
            id_values[id] = None
     
    x_values = []
    y_values = []
    id_values = sorted(id_values.items(), key=lambda x: int(x[0]))   
     
    #pprint(id_values)    
     
    for item in id_values:
        if item[1]:
            x_values.append(item[1][0])
            y_values.append(item[1][1])
            print '---------------------'
            print 'subject id: '+ item[0]
            print 'x: ' + str(item[1][0]) 
            print 'y: ' + str(item[1][1])
#         if id_values[id]:
#             x_values.append(id_values[id][0])
#             y_values.append(id_values[id][1])
#             print 'subject id: '+ id
#             print 'x: ' + str(id_values[id][0]) 
#             print 'y: ' + str(id_values[id][1])            
 
 
     
    plt.scatter(x_values,y_values)
    #plt.xlabel('average sequence length')
    #plt.ylabel('openness')
    plt.show()
    


if __name__ == '__main__':  
    #all_subjects_edit_dist()
    #all_subjects_plot()
    

    fp = r'data\by subjects\wifigps_subject08.csv'
    get_avg_edit_dist(fp)
    

    #all_subjects_plot()

    
    
    
    
    
    
    
    
    
    
    
    
    