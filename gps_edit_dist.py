import os
import time
import copy
from datetime import datetime
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np

from utilities import edit_dist, get_y, get_all_y
from utilities import write_feature_to_csv

cur_dir = os.path.dirname(os.path.realpath(__file__))

    
def get_seq(fp):
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
    
    #return in_loc_count
    
    dt_locs = []
    for idx, pair in enumerate(in_loc_count):
 
        locs = pair[1]
        locs_merge = []
        for i, loc in enumerate(locs):
            if i == 0:
                locs_merge.append(loc)
            else:
                if loc != locs[i-1]:
                    locs_merge.append(loc)
        dt_locs.append((pair[0], locs_merge))   
         
    #pprint(dt_locs) 
    return dt_locs

def per_subject(fp):

    locs = get_seq(fp)
    #pprint(locs)

    seqs = []

    for dt, entries in locs:
        dt_obj = datetime.strptime(dt, "%d%b%Y")
        weekday = dt_obj.strftime("%A")
        if weekday == 'Saturday' or weekday == 'Sunday':
            continue
        seqs.append(entries)
    #result.append((day, seqs))
        
    pprint(seqs)
            
    return seqs

def per_subject_by_weekdays(fp):
    result = []
    locs = get_seq(fp)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for day in days:
        seqs = []
        seq_freq = {}
        avg_seq_len = 0
    
        for dt, entries in locs:
            dt_obj = datetime.strptime(dt, "%d%b%Y")
            weekday = dt_obj.strftime("%A")
            if weekday == day:

                seqs.append(entries)
        result.append((day, seqs))
        
    for pair in result:
        print pair[0]
        for entry in pair[1]:
            print entry
            
    return result
    
    
def get_weekday_sum_avg_edit_dist(fp):
    #fp = r"C:\Users\Sophie\Smart Phone Project Local\by subjects\wifigps_subject04.csv"
    sum = 0
    weekday_seqs = per_subject_by_weekdays(fp)
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
    #print sum
    return sum

def get_avg_edit_dist(fp):
    per_subject(fp)

def get_feature():
    id_feature = {}
    addr_dir = os.path.join(cur_dir, 'data', 'gps_osm')
    for file in os.listdir(addr_dir):
        if not file.endswith('.csv'):
            continue
        subj = file.split('.')[0][-2:]
        
        print subj
        #subj = str(int(subj))
        fp = os.path.join(addr_dir, file)
        
        #result = get_avg_edit_dist(fp)       
        result = get_weekday_sum_avg_edit_dist(fp)
        
        id_feature[subj] = result
    return id_feature

def all_subjects_plot():

    id_x = get_feature()
    #pprint(id_x)

    cols = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]
    #cols = [5, 7]
    for index, i in enumerate(cols):

        id_y, y_label = get_y(i)    
    
        id_values = {}
        for id in id_x:
            #print id
            if id in id_y:
                id_values[id] = (id_x[id], id_y[id])
            else:
                id_values[id] = None
         
        x_values = []
        y_values = []
        id_values = sorted(id_values.items(), key=lambda x: int(x[0]))   
         
    
        for item in id_values:
            if item[1]:
                x_values.append(item[1][0])
                y_values.append(item[1][1])
#                 print '---------------------'
#                 print 'subject id: '+ item[0]
#                 print 'x: ' + str(item[1][0]) 
#                 print 'y: ' + str(item[1][1])
        
        plt.subplot(6, 2, index+1)
        #plt.subplot(2, 1, index+1)
        plt.scatter(x_values,y_values)
        plt.ylabel(y_label)
        
    
    plt.show()
    
# def write_edit_dist_to_csv():
# 
#     output_fp = os.path.join(cur_dir, 'data', 'matrix_data', 'gps_edit_dist.csv')
#     fw = open(output_fp, 'a')
#     labels = ['subject_id', 'edit_dist', 'extra', 'agrbl', 'consc', 'neuro', 'open']
#     labels.extend(['assertive', 'activity', 'altruism', 'compliance', 'order', 'discipline', 'anxiety', 'depression'])
#     fw.write(','.join(labels) + '\n')
#     
#     id_edit_dist = get_x()
#     id_all_y = get_all_y()
#                 
#     for id in sorted(id_edit_dist):
# 
#         if not id in id_all_y:
#             continue
#         
#         line = [id]     
#         line.append(str(id_edit_dist[id]))
#           
#         for value in id_all_y[id]:
#             line.append(value)
#           
#         fw.write(','.join(line) + '\n')
#         
#     fw.close()
    
if __name__ == '__main__':
#     fp = os.path.join(cur_dir, 'data', 'gps_osm', 'wifigps_addr_04.csv')
#     per_subject_by_weekdays(fp)
    
    #all_subjects_plot()
    id_edit_dist = get_feature()
    write_feature_to_csv('gps_edit_dist', id_edit_dist)

    