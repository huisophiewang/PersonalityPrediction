import os
from datetime import datetime
from pprint import pprint
import random
import math
import numpy as np

from util_gps import ID_HOME_GPS
from util_gps import all_locs_1, all_locs_2
from util import get_entropy, OFF_CAMPUS, write_feature_to_csv, fill_miss_values

# MIN_SAMPLES = 65
# NUM_DAYS = 10

MIN_SAMPLES = 36
NUM_DAYS = 20

# gps frequency changes from every 20 min to every 10 min
def get_complete_days(fp):
    time_by_dates = {}
    loc_by_dates = {}
    coord_by_dates = {}
    
    fr = open(fp, 'rU') 
    lines = fr.readlines()
    for line in lines:
        #print line
        atts = line.strip('\n').split(",")
        dt = atts[1][:9]
        
        if dt not in time_by_dates:
            time_by_dates[dt] = []
            time_by_dates[dt].append(atts[1])
            loc_by_dates[dt] = []
            loc_by_dates[dt].append(atts[5])
            coord_by_dates[dt] = []
            coord_by_dates[dt].append((atts[2],atts[3]))
        else:
            time_by_dates[dt].append(atts[1])
            loc_by_dates[dt].append(atts[5])
            coord_by_dates[dt].append((atts[2],atts[3]))
            
    time_by_dates = sorted(time_by_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
#     print len(loc_by_dates)
#     return loc_by_dates
    
    complete_dates = []
    loc_by_complete_dates = {}
    coord_by_complete_dates = {}
    for pair in time_by_dates:
        dt = pair[0]
        seq = pair[1]
        #print dt, len(seq)  
#         dt_obj = datetime.strptime(dt, "%d%b%Y")
#         weekday = dt_obj.strftime("%A")
#         if weekday != 'Saturday' and weekday != 'Sunday':
#             continue
               
        avg = 0.0
        if len(seq) < 10:
            continue
        for idx in range(len(seq)):
            if idx == 0:
                continue
            tm = datetime.strptime(seq[idx], "%d%b%Y:%H:%M:%S")
            prev_tm = datetime.strptime(seq[idx-1], "%d%b%Y:%H:%M:%S")
            diff = tm - prev_tm
            items = str(diff).split(':')
            sec = int(items[0])*3600 + int(items[1])*60 + int(items[2])
            avg += sec
        avg /= len(seq)-1
         
        # sample rate is 10 min:
        if avg/60 < 15.0:
            if len(seq) >= MIN_SAMPLES * 2:
                complete_dates.append(dt)
                # down sampling
                loc_by_complete_dates[dt] = loc_by_dates[dt][0::2]
                coord_by_complete_dates[dt] = coord_by_dates[dt][0::2]
        # sample rate is 20 min:
        else:
            if len(seq) >= MIN_SAMPLES and len(seq) <= 72:
                complete_dates.append(dt)
                loc_by_complete_dates[dt] = loc_by_dates[dt] 
                coord_by_complete_dates[dt] = coord_by_dates[dt]                                    
    #pprint(complete)
    #print len(complete)
 
    loc_by_complete_dates = sorted(loc_by_complete_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    coord_by_complete_dates = sorted(coord_by_complete_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    #pprint(by_complete_dates)
     
    print len(complete_dates)
    return complete_dates, loc_by_complete_dates, coord_by_complete_dates



def get_loc_freq(sample_days, loc_by_dates):
    loc_freq = {}
    
    for pair in loc_by_dates:
        dt = pair[0]
        if not dt in sample_days:
            continue
        print pair
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
    #print len(loc_freq)
    
    return loc_freq

def merge_homes(loc_freq, id):
    homes = ID_HOME_GPS[id]
    loc_freq['home'] = 0

    for loc in loc_freq:
        if loc in homes:
            loc_freq['home'] += loc_freq[loc]
    
    for loc in homes:
        if loc in loc_freq:
            loc_freq.pop(loc)
    
    return loc_freq


            
def get_radius(sample_days, coord_by_dates):
    #print sample_days
    radius = []
    area = []
    
    for pair in coord_by_dates:
        dt = pair[0]
        if not dt in sample_days:
            continue
            
        coords = pair[1]
        lati = [float(coord[0]) for coord in coords]
        logi = [float(coord[1]) for coord in coords]
        a = max(lati) - min(lati)
        b = max(logi) - min(logi)
        r = math.sqrt(a*a+b*b)
        s = a*b
        radius.append(r)
        area.append(s)
        
    avg_radius = np.mean(radius)
    var_radius = np.var(radius)
    avg_area = np.mean(area)
    #print avg_radius
    #return avg_radius
    return avg_area

def get_feature():
    all_locs = set()
    id_feature = {}
    addr_dir = os.path.join('dataset', 'sensing','gps_osm')
    for file in os.listdir(addr_dir):
        if not file.endswith('.csv'):
            continue
        fp = os.path.join(addr_dir, file)
        id = file.split('.')[0][-2:]
        
        if id in OFF_CAMPUS:
            continue
        
#         if id != '01':
#             continue
               
        print 
        print 'subject id: ' + id


        complete_dates, loc_by_complete_dates, coord_by_complete_dates = get_complete_days(fp)
        sample_days = random.sample(complete_dates, NUM_DAYS)
        
        #sample_days = complete_dates[:NUM_DAYS]
        #sample_days = complete_dates
#         loc_freq = get_loc_freq(sample_days, loc_by_complete_dates)    
#         #pprint(loc_freq) 
#         loc_freq = merge_homes(loc_freq, id)
#         #pprint(loc_freq)
# 
# 
#         entropy = get_entropy(loc_freq)
#         id_feature[id] = entropy

        result = get_radius(sample_days, coord_by_complete_dates)
        id_feature[id] = result
        
    
    return id_feature

if __name__ == '__main__':
    id_feature = get_feature()
    pprint(id_feature)
    #write_feature_to_csv(id_feature, 'gps_entropy')
    #write_feature_to_csv(id_feature, 'gps_avg_radius')
    #fill_miss_values(id_feature, 1, ['59','54', '57'])
    #write_feature_to_csv(id_feature, 'gps_var_radius')
    fill_miss_values(id_feature, 1, ['59'])
    write_feature_to_csv(id_feature, 'gps_avg_area')
    
    
    