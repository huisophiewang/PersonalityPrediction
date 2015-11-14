import os
import time
import copy
from datetime import datetime
from pprint import pprint
import random
import math
import matplotlib.pyplot as plt

from bag_of_words_all_locs import id_home
from bag_of_words_all_locs import all_locs_1, all_locs_2
from utilities import get_y, get_all_y
from utilities import write_feature_to_csv

cur_dir = os.path.dirname(os.path.realpath(__file__))
MIN_SAMPLES = 65
NUM_DAYS = 30
MIN_FREQ = 2



def get_change_date(fp):
    by_dates = {}
    
    fr = open(fp, 'rU') 
    lines = fr.readlines()
    for line in lines:
        #print line
        atts = line.strip('\n').split(",")
        dt = atts[1][:9]
        
        if dt not in by_dates:
            by_dates[dt] = []
            by_dates[dt].append(atts[1])
        else:
            by_dates[dt].append(atts[1])
    
    #pprint(by_dates)
    by_dates = sorted(by_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    #pprint(by_dates)
    
    change_dt = None
    
    for pair in by_dates:
        seq = pair[1]
        avg = 0.0
        if len(seq) < 2:
            continue
        for idx in range(len(seq)):
            if idx == 0:
                continue
#             tm = time.strptime(seq[idx], "%H:%M:%S")
#             prev_tm = time.strptime(seq[idx-1], "%H:%M:%S")
#             diff = tm - prev_tm
#             print diff
            tm = datetime.strptime(seq[idx], "%d%b%Y:%H:%M:%S")
            prev_tm = datetime.strptime(seq[idx-1], "%d%b%Y:%H:%M:%S")
            diff = tm - prev_tm
            items = str(diff).split(':')
            sec = int(items[0])*3600 + int(items[1])*60 + int(items[2])
            avg += sec
            
        avg /= len(seq)-1
        if avg/60 < 15.0:
            change_dt = pair[0]
            break
    
    #print change_dt
    return change_dt
    

def get_complete_days(fp, change_dt):
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
    #pprint(by_dates)
    
    #complete = []
    complete = []
    by_complete_dates = {}
    for pair in by_dates:
        dt = pair[0]
        seq = pair[1]
        #pprint(seq)
 
    #     weekday = dt_obj.strftime("%A")
    #     if weekday != 'Saturday' and weekday != 'Sunday':
    #         continue
        
        if change_dt == None:
            if len(seq) >= MIN_SAMPLES and len(seq) <= 72:
                complete.append(dt)
                by_complete_dates[dt] = seq
                
        else:
            dt_obj = datetime.strptime(dt, "%d%b%Y")
            if dt_obj < datetime.strptime(change_dt, "%d%b%Y"):
                if len(seq) >= MIN_SAMPLES and len(seq) <= 72:
                    complete.append(dt)
                    by_complete_dates[dt] = seq
            else:
                if len(seq) >= MIN_SAMPLES * 2:
                    complete.append(dt)
                    # down sampling
                    by_complete_dates[dt] = seq[0::2]
                                      
    #pprint(complete)
    #print len(complete)

    by_complete_dates = sorted(by_complete_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    
    return complete, by_complete_dates

def get_loc_freq(sample_days, by_dates):
    loc_freq = {}
    
    for pair in by_dates:
        dt = pair[0]
        if not dt in sample_days:
            continue
        seq = pair[1]
        for loc in seq:
            if not loc in loc_freq:
                loc_freq[loc] = 0
                loc_freq[loc] += 1
            else:
                loc_freq[loc] += 1
                
#     loc_freq = sorted(loc_freq.items(), key=lambda item: item[1], reverse=True)
#     for pair in loc_freq:
#         print pair
#     print len(loc_freq)
    
    return loc_freq

def merge_homes(loc_freq, id):
    homes = id_home[id]
    loc_freq['home'] = 0
    home_of_31 = []
    for loc in loc_freq:
        if id == '31':
            if loc[4:] == homes[0]:
                home_of_31.append(loc)
                loc_freq['home'] += loc_freq[loc]
            if loc in homes[1:]:
                loc_freq['home'] += loc_freq[loc]
        else:
            if loc in homes:
                loc_freq['home'] += loc_freq[loc]
    
    if id == '31':
        for loc in homes[1:]:
            loc_freq.pop(loc)
        for loc in home_of_31:
            loc_freq.pop(loc)
    else:
        for loc in homes:
            if loc in loc_freq:
                loc_freq.pop(loc)
    
#     loc_freq = sorted(loc_freq.items(), key=lambda item: item[1], reverse=True)      
#     for pair in loc_freq:
#         print pair
#     print len(loc_freq)
    
    return loc_freq

def get_all_loc_freq(loc_freq):
    all_loc_freq = {}
    total_freq = 0
    for loc in all_locs_2:
        if loc in loc_freq and loc_freq[loc] >= MIN_FREQ:
            all_loc_freq[loc] = loc_freq[loc]
            total_freq += loc_freq[loc]
        else:
            all_loc_freq[loc] = 0
    
    for loc in all_loc_freq:
        all_loc_freq[loc] /= float(total_freq)
        
    #pprint(all_loc_freq)
    return all_loc_freq

def get_entropy(all_loc_freq):
    entropy = 0.0
    for loc in all_loc_freq:
        p = all_loc_freq[loc]
        if p != 0:
            entropy += (-p) * math.log(p, 2)       
    print entropy
    return entropy



def get_feature():
    all_locs = set()
    id_feature = {}
    addr_dir = os.path.join(cur_dir, 'data', 'gps_osm')
    for file in os.listdir(addr_dir):
        if not file.endswith('.csv'):
            continue
        fp = os.path.join(addr_dir, file)
        id = file.split('.')[0][-2:]
        
        change_dt = get_change_date(fp)
        complete, by_complete_dates = get_complete_days(fp, change_dt)
        if len(complete) < 30:
            continue
        
        print 
        print 'subject id: ' + id
        
        #sample_days = random.sample(complete, NUM_DAYS)
        sample_days = complete[:NUM_DAYS]

        loc_freq = get_loc_freq(sample_days, by_complete_dates)
        
        loc_freq = merge_homes(loc_freq, id)
         
        all_loc_freq = get_all_loc_freq(loc_freq)
           
        entropy = get_entropy(all_loc_freq)
        id_feature[id] = entropy
        
    
    return id_feature

def all_subjects_plot():

    id_x = get_feature()
    #pprint(id_x)

    cols = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]
    cols = [5, 7]
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
        
        #plt.subplot(6, 2, index+1)
        plt.subplot(2, 1, index+1)
        plt.scatter(x_values,y_values)
        plt.ylabel(y_label)
        
    
    plt.show()
 
    
def write_histogram_to_csv():
    output_fp = os.path.join(cur_dir, 'data', 'matrix_data', 'gps_features.csv')
    fw = open(output_fp, 'a')
    
    addr_dir = os.path.join(cur_dir, 'data', 'gps_osm')
    for file in os.listdir(addr_dir):
        if not file.endswith('.csv'):
            continue
        fp = os.path.join(addr_dir, file)
        id = file.split('.')[0][-2:]
        
        change_dt = get_change_date(fp)
        complete, by_complete_dates = get_complete_days(fp, change_dt)
        if len(complete) < 30:
            continue
        
        print 
        print 'subject id: ' + id
        
        id_y, label = get_y(5)
        if not id in id_y:
            continue
        

        #sample_days = random.sample(complete, NUM_DAYS)
        sample_days = complete[:NUM_DAYS]

        loc_freq = get_loc_freq(sample_days, by_complete_dates)
        
        loc_freq = merge_homes(loc_freq, id)
        
        all_loc_freq = get_all_loc_freq(loc_freq)
        
        all_loc_freq = sorted(all_loc_freq.items(), key=lambda item: item[0])
        

        line = [str(item[1]) for item in all_loc_freq]
        line.append(str(id_y[id]))
        fw.write(','.join(line) + '\n')
        
    fw.close() 
    


              
if __name__ == '__main__':
#     fp = os.path.join(cur_dir, 'data', 'gps_osm', 'wifigps_addr_04.csv')
#     change_dt = get_change_date(fp)
#     complete, by_complete_dates = get_complete_days(fp, change_dt)
#     sample_days = random.sample(complete, NUM_DAYS)
#     print sample_days
#     get_loc_freq(sample_days, by_complete_dates)
    
    #all_subjects_plot()
    

    id_entropy = get_feature()
    write_feature_to_csv('entropy', id_entropy)

    