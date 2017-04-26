import time
import os
import random
import copy
from datetime import datetime
from prep_wifi_loc import get_in_loc_duration, get_seqs
from util import CUR_DIR, ID_HOME, REMOVE_SUBJECTS, OFF_CAMPUS
from util import write_feature_to_csv, write_multi_features_to_csv
from util import get_time_var, get_time_mean
import pprint
pp = pprint.PrettyPrinter(width=100)
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')

def get_start_var_oncampus(in_loc_duration, id, wkd=None):

    start_times = []
    for pair in in_loc_duration:
        dt = pair[0]    
        weekday = datetime.strptime(dt, "%Y-%m-%d").strftime("%A")       
        if not wkd:  
            if weekday in ['Saturday', 'Sunday']:
                continue 
        else:
            if wkd != weekday:
                continue
        seq = pair[1]
        #pp.pprint(seq)
        for line in seq:
            loc = line[0][3:-1]
            loc_start_time = time.strptime(line[1], "%H:%M:%S")
            # the first loc after 4:00 am that is not home
            if loc_start_time > time.strptime('04:00:00', "%H:%M:%S") and not loc in ID_HOME[id]:
                start_times.append(line[1])
                #print line[1]
                break
    #print len(start_times)
    #samples = random.sample(start_times, 20)
    samples = start_times
    #print len(samples)
    return get_time_mean(samples)
    #return get_time_var(samples)

def get_start_var_offcampus(in_loc_duration, id):
    start_times = []
    for pair in in_loc_duration:
        dt = pair[0]    
        weekday = datetime.strptime(dt, "%Y-%m-%d").strftime("%A")         
        if weekday in ['Saturday', 'Sunday']:
            continue 
        seq = pair[1]
        #pp.pprint(seq)
        first_loc = seq[0]
        start_time = first_loc[1]
        #print start_time
        start_times.append(start_time)
    #print len(start_times)
    #samples = random.sample(start_times, 20)
    samples = start_times
    return get_time_var(samples)

    
def get_end_var_oncampus(in_loc_duration, id, wkd=None):
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
        if not wkd:  
            if weekday in ['Saturday', 'Sunday']:
                continue 
        else:
            if wkd != weekday:
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
            if i > 0 and not loc in ID_HOME[id]:
                end_time = seq_extend_reverse[i-1][1]
                
#                 items = end_time.split(':')
#                 hour = int(items[0])
#                 if hour < 4:
#                     end_time = "%02d:%s:%s" % (hour+24, items[1], items[2])
           
                end_times.append(end_time)
                break
   
    samples = end_times
    #print len(samples)
    #return get_time_var(samples)
    return get_time_mean(samples)
    
     
def get_end_var_offcampus(in_loc_duration, id):
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
        
        last_loc = seq_extend[-1]
        #print last_loc
        end_time = last_loc[2]
        end_times.append(end_time)
    #print len(start_times)
    #samples = random.sample(start_times, 20)
    samples = end_times
    return get_time_var(samples)

def get_feature(func):
    id_feature = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]
#         if id in REMOVE_SUBJECTS:
#             continue
        
        if not id in OFF_CAMPUS:
            continue
        
        print '===================='
        print 'id: ' + id
    
        in_loc_duration = get_in_loc_duration(id, duration_cut=60*5)
        #pp.pprint(in_loc_duration)
 
        result = func(in_loc_duration, id)
        id_feature[id] = result
        
    return id_feature



def get_feature_start_var():
    id_feature = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]

        print '===================='
        print 'id: ' + id
    
        in_loc_duration = get_in_loc_duration(id, duration_cut=60*5)
        #seqs = get_seqs(id)
        
        if id in OFF_CAMPUS:
            #result = get_start_var_offcampus(in_loc_duration, id)
            continue
        else:
            result = get_start_var_oncampus(in_loc_duration, id)
            
        id_feature[id] = result
        
    return id_feature


def get_feature_start_var_weekday():
    id_features = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]

        print '===================='
        print 'id: ' + id
    
        in_loc_duration = get_in_loc_duration(id, duration_cut=60*5)
        #seqs = get_seqs(id)
        
        if id in OFF_CAMPUS:
            #result = get_start_var_offcampus(in_loc_duration, id)
            continue
        
        result = []
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            result.append(get_start_var_oncampus(in_loc_duration, id, day))
        print result
        id_features[id] = result
        
    return id_features

def get_feature_end_var():
    id_feature = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]

        print '===================='
        print 'id: ' + id
    
        in_loc_duration = get_in_loc_duration(id, duration_cut=60*5)
        
        if id in OFF_CAMPUS:
            #result = get_end_var_offcampus(in_loc_duration, id)
            continue
        else:
            result = get_end_var_oncampus(in_loc_duration, id)
            
        id_feature[id] = result
        
    return id_feature

def get_feature_end_var_weekday():
    id_features = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]

        print '===================='
        print 'id: ' + id
    
        in_loc_duration = get_in_loc_duration(id, duration_cut=60*5)
        #seqs = get_seqs(id)
        
        if id in OFF_CAMPUS:
            #result = get_start_var_offcampus(in_loc_duration, id)
            continue
        
        result = []
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            result.append(get_end_var_oncampus(in_loc_duration, id, day))
        print result
        id_features[id] = result
        
    return id_features

if __name__ == '__main__':
#     id_feature = get_feature(get_start_var)
#     write_feature_to_csv(id_feature, 'start_time_var')
    
#     id_feature = get_feature(get_start_var_offcampus)
#     write_feature_to_csv(id_feature, 'start_time_var_offcampus')
    
#     id_feature = get_feature(get_end_var)
#     write_feature_to_csv(id_feature, 'end_time_var')
    
#     id_feature = get_feature(get_end_var_offcampus)
#     write_feature_to_csv(id_feature, 'end_time_var_offcampus')
    
    
#     id = '01'
#     in_loc_duration = get_in_loc_duration(id)
#     get_end_time_test(in_loc_duration, id)

    #id_feature = get_feature_start_var()
    #write_feature_to_csv(id_feature, 'start_time_var_oncampus')
    #write_feature_to_csv(id_feature, 'start_time_avg_oncampus')
    
    id_feature = get_feature_end_var()
    #write_feature_to_csv(id_feature, 'end_time_var_oncampus')
    write_feature_to_csv(id_feature, 'end_time_avg_oncampus')

    #id_features = get_feature_start_var_weekday()
    #write_multi_features_to_csv(id_features, ['start_time_var_mon','start_time_var_tue','start_time_var_wed','start_time_var_thr','start_time_var_fri'])   
    
#     id_features = get_feature_end_var_weekday()
#     write_multi_features_to_csv(id_features, ['end_time_var_mon','end_time_var_tue','end_time_var_wed','end_time_var_thr','end_time_var_fri'])   
#     