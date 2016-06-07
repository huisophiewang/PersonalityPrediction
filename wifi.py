import os
import random
from datetime import datetime
import pprint 
import copy

from util import CUR_DIR, remove_subjects
pp = pprint.PrettyPrinter(width=200)
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')
dir = r'C:\Users\Sophie\workspace\Personality\dataset\sensing'

def get_in_loc_duration(fp, duration_cut, sample_days, weekday_only):
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
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        weekday = date_obj.strftime("%A")         
        if weekday_only and weekday in ['Saturday', 'Sunday']:
            continue 
         
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
        
def get_seqs(fp, duration_cut=60*5, sample_days=20, weekday_only=True):

    in_loc_duration = get_in_loc_duration(fp, duration_cut, sample_days, weekday_only)

    ### sample same number of days for each subject    
    seqs = []
    samples = random.sample(in_loc_duration, sample_days)
    for pair in samples:
        locs = [entry[0][3:-1] for entry in pair[1]]
        seqs.append(locs)  
        print pair[0] + ' ' +  ', '.join(locs)
    #pp.pprint(seqs)
    
    return seqs

def get_all_subjects_seqs():
    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue        
        id = file.split('.')[0][-2:]
        if id in remove_subjects:
            continue
        print '----------'
        print 'id: ' + id
     
        fp = os.path.join(wifi_dir, file)
        get_seqs(fp, 60*5)

def to_datetime(folder, id):
    input_fp = os.path.join(dir, folder, '%s_u%2d.csv' % (folder, id))  
    output_fp = os.path.join(dir, folder, '%s_u%2d_datetime.csv' % (folder, id))
    
    fr = open(input_fp, 'rU') 
    fw = open(output_fp, 'a')
    fr.readline()
    lines = fr.readlines()
    for line in lines:
        if line == '\n':
            continue
        items = line.rstrip(',\n').split(",")
        dt = datetime.fromtimestamp(int(items[0])).strftime('%Y-%m-%d-%H:%M:%S')
        outline = [dt]
        
        outline.extend(items[1:])
        #print outline
        fw.write(','.join(outline) + '\n')
    fw.close()
    
    

    
if __name__ == '__main__':  
    get_all_subjects_seqs()
    
#     for id in [46, 47, 49, 50, 51, 52, 53, 54, 56, 57, 58, 59]:
#         to_datetime('gps', id)
    
    #print random.sample([1,4,5,6,7],2)


        
        