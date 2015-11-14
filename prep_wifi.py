import csv
import copy

from datetime import datetime, date, time, timedelta
from pprint import pprint
from collections import OrderedDict
import os

import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = r'data\by subjects'
DURATION_CUT = 60*10

def get_major_loc(fp):

    lines = []
     
    by_dates = {}
    with open(fp, 'rU') as fr:
        lines = fr.readlines()
        for line in lines:
            atts = line.strip('\n').split(",")
            #print atts
            dt = atts[1][:9]
            if dt not in by_dates:
                by_dates[dt] = []
                by_dates[dt].append(atts)
            else:
                by_dates[dt].append(atts)
    
    #pprint(by_dates)
    by_dates = sorted(by_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    #pprint(by_dates)
     
    in_loc = []
    for idx, pair in enumerate(by_dates):
        in_loc.append((pair[0], []))
        for entry in pair[1]:
            if entry[4].startswith('in'):
                in_loc[idx][1].append(entry)
       
     
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
    pprint(in_loc_duration)
     
      
    for idx, pair in enumerate(in_loc_duration):
           
        in_loc_duration[idx] = (pair[0], [])
        entries = pair[1]
        for i, entry in enumerate(entries):
            time_start = in_loc[idx][1][entry[5]][1]
            time_end = in_loc[idx][1][entry[6]][1]
            duration = datetime.strptime(time_end, "%d%b%Y:%H:%M:%S") - datetime.strptime(time_start, "%d%b%Y:%H:%M:%S")
            duration = duration.seconds
            if duration > DURATION_CUT:
                m_entry = []
                m_entry.append(entry[4])
                m_entry.append(time_start[-8:])
                m_entry.append(time_end[-8:])
                m_entry.append(duration)
                in_loc_duration[idx][1].append(m_entry)   
                
      
    #pprint(in_loc_duration)
    
    for item in in_loc_duration:
#         if item[0] != '27MAR2013':
#             continue
        print item[0]
        pprint(item[1])
    
    return in_loc_duration

def all_subjects():
    for file in os.listdir(DATA_DIR):
        if not file.endswith('.csv'):
            continue
        subj = file.split('.')[0][-2:]
        print
        print 'subject id: ' + subj
        
        fp = os.path.join(DATA_DIR, file)
        get_major_loc(fp)
    
  
if __name__ == '__main__':  
    
    fp = r'data\by subjects\wifigps_subject01.csv'
    get_major_loc(fp)
    #all_subjects()
    

        

    
    
    
    
    
    
    
    
    
    
    
    
    