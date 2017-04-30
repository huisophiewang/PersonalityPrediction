import os
from datetime import datetime
from pprint import pprint

from util_gps import id_home
from util_gps import all_locs_1, all_locs_2
from util import get_entropy, OFF_CAMPUS

MIN_SAMPLES = 65
NUM_DAYS = 30
MIN_FREQ = 2



# gps frequency changes from every 20 min to every 10 min
def get_complete_days(fp):
    time_by_dates = {}
    loc_by_dates = {}
    
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
        else:
            time_by_dates[dt].append(atts[1])
            loc_by_dates[dt].append(atts[5])
            
    time_by_dates = sorted(time_by_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    
    #complete = []
    complete_dates = []
    by_complete_dates = {}
    for pair in time_by_dates:
        dt = pair[0]
        seq = pair[1]
        #print dt, len(seq)  
    #     weekday = dt_obj.strftime("%A")
    #     if weekday != 'Saturday' and weekday != 'Sunday':
    #         continue
              
        avg = 0.0
        if len(seq) < 10:
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
        
        # sample rate is 10 min:
        if avg/60 < 15.0:
            if len(seq) >= MIN_SAMPLES * 2:
                complete_dates.append(dt)
                # down sampling
                loc_seq = loc_by_dates[dt]
                by_complete_dates[dt] = loc_seq[0::2]
        # sample rate is 20 min:
        else:
            if len(seq) >= MIN_SAMPLES and len(seq) <= 72:
                complete_dates.append(dt)
                by_complete_dates[dt] = loc_by_dates[dt]                                     
    #pprint(complete)
    #print len(complete)

    by_complete_dates = sorted(by_complete_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    #pprint(by_complete_dates)
    
    print len(complete_dates)
    return complete_dates, by_complete_dates

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

    for loc in loc_freq:
        if loc in homes:
            loc_freq['home'] += loc_freq[loc]
    
    for loc in homes:
        if loc in loc_freq:
            loc_freq.pop(loc)
    
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

#         if id != '59':
#             continue
               
        print 
        print 'subject id: ' + id
        
        #get_change_date(fp)

        complete_dates, by_complete_dates = get_complete_days(fp)

#         if len(complete_dates) < NUM_DAYS:
#             continue
        

        
#         #sample_days = random.sample(complete, NUM_DAYS)
#         sample_days = complete[:NUM_DAYS]
        sample_days = complete_dates

        loc_freq = get_loc_freq(sample_days, by_complete_dates)    
        #pprint(loc_freq) 
        #loc_freq = merge_homes(loc_freq, id)
        #pprint(loc_freq)
#           
#         all_loc_freq = get_all_loc_freq(loc_freq)
#         entropy = get_entropy(all_loc_freq)

        entropy = get_entropy(loc_freq)
        id_feature[id] = entropy
        
    
    return id_feature

if __name__ == '__main__':
    get_feature()
    