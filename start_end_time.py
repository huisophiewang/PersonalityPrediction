import time
import os
import random
import copy
from datetime import datetime
from wifi_prep import get_in_loc_duration
from util import CUR_DIR, id_home, remove_subjects, write_feature_to_csv
import pprint
pp = pprint.PrettyPrinter(width=100)
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')

def get_start_var(in_loc_duration, id):
    # randomly choose 20 days
    
    start_times = []
    for pair in in_loc_duration:
        dt = pair[0]    
        weekday = datetime.strptime(dt, "%Y-%m-%d").strftime("%A")         
        if weekday in ['Saturday', 'Sunday']:
            continue 
        seq = pair[1]
        #pp.pprint(seq)
        for line in seq:
            loc = line[0][3:-1]
            loc_start_time = time.strptime(line[1], "%H:%M:%S")
            # the first loc after 4:00 am that is not home
            if loc_start_time > time.strptime('04:00:00', "%H:%M:%S") and not loc in id_home[id]:
                start_times.append(line[1])
                #print line[1]
                break
    #print len(start_times)
    #samples = random.sample(start_times, 20)
    samples = start_times
    return get_var(samples)

def get_end_var_old(in_loc_duration, id):
    end_times = []

    for pair in in_loc_duration:
        dt = pair[0]    
        weekday = datetime.strptime(dt, "%Y-%m-%d").strftime("%A")         
        if weekday in ['Saturday', 'Sunday']:
            continue       
        seq = pair[1]        
        if not seq:
            continue
        last_loc = seq[-1][0][3:-1]
        if not last_loc in id_home[id]:
            continue
        for line in reversed(seq):
            loc = line[0][3:-1]
            end_time = time.strptime(line[2], "%H:%M:%S")
            # the last loc after 3:00 pm that is not home
            if end_time > time.strptime('15:00:00', "%H:%M:%S") and not loc in id_home[id]:
                end_times.append(line[2])
                #print line[2]
                break
            
    samples = end_times
    return get_var(samples)
    
def get_end_var(in_loc_duration, id):
    end_times = []
    for idx, pair in enumerate(in_loc_duration): 
        # don't consider last day
        if idx == len(in_loc_duration) - 1:
            continue
        td, td_seq = in_loc_duration[idx]
        tmr, tmr_seq = in_loc_duration[idx+1]
        td_obj = datetime.strptime(td, "%Y-%m-%d")
        tmr_obj = datetime.strptime(tmr, "%Y-%m-%d")
        weekday = td_obj.strftime("%A")         
        if weekday in ['Saturday', 'Sunday']:
            continue 
        duration = tmr_obj - td_obj
        # extend seq to before 4:00 am the next day
        seq_extend = copy.deepcopy(td_seq)
        if duration.days == 1:
            for line in tmr_seq:
                loc_start_time = time.strptime(line[1], "%H:%M:%S")
                if loc_start_time < time.strptime('04:00:00', "%H:%M:%S"):
                    seq_extend.append(line)
        # check locs in reverse order, find the first non-home loc, and use the following home loc start time
        seq_extend_reverse = list(reversed(seq_extend))
        for i, line in enumerate(seq_extend_reverse):
            loc = line[0][3:-1]
            if i > 0 and not loc in id_home[id]:
                end_time = seq_extend_reverse[i-1][1]
                
#                 items = end_time.split(':')
#                 hour = int(items[0])
#                 if hour < 4:
#                     end_time = "%02d:%s:%s" % (hour+24, items[1], items[2])
           
                end_times.append(end_time)
                break
   
    samples = end_times
    print len(samples)
    return get_var(samples)
    
     

def get_var(times):  

    avg = 0.0
    secs = []
    for t in times:  
        items = t.split(':')
        sec = int(items[0])*3600 + int(items[1])*60 + int(items[2])
        #sec = sec/60
        secs.append(sec)
        avg += sec
    avg /= len(times)
    
    var = 0.0
    for sec in secs:
        var += (sec - avg) * (sec - avg)
    
    var /= len(times)

    return var

def get_feature(func):
    id_feature = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]
        if id in remove_subjects:
            continue
        
        print '===================='
        print 'id: ' + id
    
        in_loc_duration = get_in_loc_duration(id, duration_cut=60*5)
        #pp.pprint(in_loc_duration)
 
        result = func(in_loc_duration, id)
        id_feature[id] = result
        
    return id_feature

if __name__ == '__main__':
#     id_feature = get_feature(get_start_var)
#     write_feature_to_csv(id_feature, 'start_time_var')
    
    id_feature = get_feature(get_end_var)
    write_feature_to_csv(id_feature, 'end_time_var')
    
#     id = '01'
#     in_loc_duration = get_in_loc_duration(id)
#     get_end_time_test(in_loc_duration, id)


    
    