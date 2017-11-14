import os
import random
from datetime import datetime
import pprint 
import copy

from util import CUR_DIR, REMOVE_SUBJECTS
pp = pprint.PrettyPrinter(width=200)
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')


def get_in_loc_duration(id, duration_cut=60*5):
    fp = os.path.join(wifi_dir, r'wifi_location_u%s.csv' % id)
    fr = open(fp, 'rU') 
    fr.readline()
    lines = fr.readlines()
    
    by_dates = {}
    ### group 'in' entries by date
    for line in lines:
        items = line.rstrip(',\n').split(",")
        if not items[1].startswith('in'):
            continue
        dt = datetime.fromtimestamp(int(items[0])).strftime('%Y-%m-%d %H:%M:%S')
        date = dt[:10]    
         
        if date not in by_dates:
            by_dates[date] = []
        by_dates[date].append([dt,items[1]])

    by_dates = sorted(by_dates.items(), key=lambda item: datetime.strptime(item[0], "%Y-%m-%d"))
    #pp.pprint(by_dates)
  

    in_loc = []
    ### to compute duration, when loc changes, append start line number
    for idx, pair in enumerate(by_dates):
        in_loc.append((pair[0], []))
        entries = pair[1]
        for i, entry in enumerate(entries):
            ### first loc or loc != prev_loc
            if i==0 or entries[i][1][3:-1] != entries[i-1][1][3:-1]:
                m_entry = copy.deepcopy(entry)
                m_entry.append(i)
                in_loc[idx][1].append(m_entry)                                                  
    #pp.pprint(in_loc) 
    

    ### to compute duration, append end line number
    for idx, pair in enumerate(in_loc):
        entries = pair[1]
        for i, entry in enumerate(entries):
            # if last loc 
            if i==len(entries)-1:
                end_index = len(by_dates[idx][1])-1
            else:
                end_index = entries[i+1][2]-1
            entry.append(end_index)
    #pp.pprint(in_loc)
    
      
    ### compute duration  
    in_loc_duration = []
    for idx, pair in enumerate(in_loc): 
        m_entries = []
        entries = pair[1]
        for i, entry in enumerate(entries):
            time_start = by_dates[idx][1][entry[2]][0]
            time_end = by_dates[idx][1][entry[3]][0]          
            duration =  datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S") - datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")
            duration = duration.seconds
            if duration > duration_cut:
                m_entry = []
                m_entry.append(entry[1])
                m_entry.append(time_start[-8:])
                m_entry.append(time_end[-8:])
                m_entry.append(duration)
                m_entries.append(m_entry)
        # remove empty days
        if len(m_entries) > 0:          
            in_loc_duration.append((pair[0], m_entries))                                
    #pp.pprint(in_loc_duration) 
    #print len(in_loc_duration)
    return in_loc_duration

def merge(in_loc_duration, threshold = 7):
    in_loc_duration_merge = []
    for pair in in_loc_duration:  
        seq = pair[1]
        
        ## for each loc in seq, count contains the number of previous locs that are the same as the current one
        count = [0] * len(seq)
        for i, loc in enumerate(seq):
            if i == 0:
                continue
            if seq[i][0] == seq[i-1][0]:
                count[i] = count[i-1] + 1
        #print count
        
        merged_seq = []
        for i, m in enumerate(count):
            ## keep these locations if count is under threshold
            if m < threshold-1:
                merged_seq.append(seq[i])
            ## 
            elif m == threshold-1:
                for j in range(threshold-1):
                    merged_seq.pop()
                merged_start_time = seq[i-threshold+1][:2]
                merged_seq.append(merged_start_time)
            ## the 
            elif i==len(count)-1 or count[i+1]==0:
                merge_end_time = seq[i][2]
                duration =  datetime.strptime(merge_end_time, "%H:%M:%S") - datetime.strptime(merged_seq[-1][1], "%H:%M:%S")
                duration = duration.seconds
                merged_seq[-1].append(merge_end_time)
                merged_seq[-1].append(duration)
                
        #pp.pprint(merged_seq)  
        in_loc_duration_merge.append((pair[0], merged_seq))   
    return in_loc_duration_merge   
                
        
def get_seqs(id, duration_cut=60*5, sample_days=20, weekday_only=True):

    in_loc_duration = get_in_loc_duration(id, duration_cut)
    #pp.pprint(in_loc_duration)
    in_loc_duration_merge = merge(in_loc_duration)
    #pp.pprint(in_loc_duration_merge)
    
    ### remove weekends
    in_loc_duration_weekdays = []
    for pair in in_loc_duration_merge:   
        date_obj = datetime.strptime(pair[0], "%Y-%m-%d")
        weekday = date_obj.strftime("%A")         
        if weekday_only and weekday in ['Saturday', 'Sunday']:
            continue 
        in_loc_duration_weekdays.append((pair[0], pair[1]))
    
      
    seqs = []
    ### randomly choose the same number of days for each subject  
    #samples = random.sample(in_loc_duration_weekdays, sample_days)
    ### choose the first 20 days
    samples = in_loc_duration_weekdays[:20]
    #print len(samples)
    for pair in samples:
        locs = [entry[0][3:-1] for entry in pair[1]]
        seqs.append(locs)  
        #print pair[0] + ' ' +  ', '.join(locs)
    
    return seqs

def get_seqs_by_weekday(id, weekday):
    in_loc_duration = get_in_loc_duration(id, 60*5)
    #pp.pprint(in_loc_duration)
    in_loc_duration_merge = merge(in_loc_duration)
    #pp.pprint(in_loc_duration_merge)
    
    ### remove weekends
    in_loc_duration_weekdays = []
    for pair in in_loc_duration_merge:   
        date_obj = datetime.strptime(pair[0], "%Y-%m-%d")
        wkday = date_obj.strftime("%A")         
        if wkday == weekday:
            in_loc_duration_weekdays.append((pair[0], pair[1]))
    
      
    seqs = []
    ### randomly choose the same number of days for each subject  
    #samples = random.sample(in_loc_duration_weekdays, sample_days)
    ### choose the first 20 days
    samples = in_loc_duration_weekdays
    #print len(samples)
    for pair in samples:
        locs = [entry[0][3:-1] for entry in pair[1]]
        seqs.append(locs)  
        #print pair[0] + ' ' +  ', '.join(locs)
    
    return seqs


def get_all_subjects_seqs():
    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue        
        id = file.split('.')[0][-2:]
        if id in REMOVE_SUBJECTS:
            continue
        print '----------'
        print 'id: ' + id
            
        get_seqs(id, 60*5)
        
def get_weekday_seqs(id):
    in_loc_duration = get_in_loc_duration(id)
    for pair in in_loc_duration:   
        date_obj = datetime.strptime(pair[0], "%Y-%m-%d")
        weekday = date_obj.strftime("%A")   
        if weekday in ['Monday', 'Wednesday', 'Friday']:
            print weekday  
            pp.pprint(pair[1])

def get_all_wifi_locs():
    all_locs = set()
    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        id = file.split('.')[0][-2:]
        seqs = get_seqs(id)
        for seq in seqs:
            for loc in seq:
                all_locs.add(loc)
    
    for loc in sorted(all_locs):
        print "'" + loc + "'" + ','
    
if __name__ == '__main__':          
#     result = get_in_loc_duration('01')
#     pp.pprint(result)

    #get_weekday_seqs('01')
    #get_seqs('01')
    get_all_wifi_locs()
    #get_seq_by_weekday('05','Monday')



        
