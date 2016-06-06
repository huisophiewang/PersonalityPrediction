import os
from datetime import datetime
import pprint 
import copy

from util import CUR_DIR
pp = pprint.PrettyPrinter(width=200)
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')

def get_seqs(fp, duration_cut):

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
  

    in_loc_duration = []
    ### to compute duration, when loc changes, append start line number
    for idx, pair in enumerate(by_dates):
        in_loc_duration.append((pair[0], []))
        entries = pair[1]
        for i, entry in enumerate(entries):
            ### first loc or loc != prev_loc
            if i==0 or entries[i][1][3:-1] != entries[i-1][1][3:-1]:
                m_entry = copy.deepcopy(entry)
                m_entry.append(i)
                in_loc_duration[idx][1].append(m_entry)                                                  
    #pp.pprint(in_loc_duration) 
    

    ### to compute duration, append end line number
    for idx, pair in enumerate(in_loc_duration):
        entries = pair[1]
        for i, entry in enumerate(entries):
            # if last loc 
            if i==len(entries)-1:
                end_index = len(by_dates[idx][1])-1
            else:
                end_index = entries[i+1][2]-1
            entry.append(end_index)
    #pp.pprint(in_loc_duration)
    
      
    ### compute duration  
    for idx, pair in enumerate(in_loc_duration): 
        ## clear out in_loc_duration
        in_loc_duration[idx] = (pair[0], [])
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
                in_loc_duration[idx][1].append(m_entry)                                  
    #pp.pprint(in_loc_duration) 

    ### output seqs of all dates
    seqs = []
    for idx, pair in enumerate(in_loc_duration):
        entries = pair[1]
        locs = [entry[0][3:-1] for entry in entries]
        seqs.append(locs)
        print ', '.join(locs)
    #pp.pprint(seqs)
    
    return seqs

if __name__ == '__main__':  

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv'):
            continue
         
        id = file.split('.')[0][-2:]
     
        fp = os.path.join(wifi_dir, file)
        print '----------'
        print 'id: ' + id

        get_seqs(fp, 60*5)
        
        