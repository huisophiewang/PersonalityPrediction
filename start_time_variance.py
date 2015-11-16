from datetime import datetime
import time
from pprint import pprint
import copy
import os
import matplotlib.pyplot as plt

from utilities import get_y, write_feature_to_csv

DURATION_CUT = 60*5
START_TIME_CUT = time.strptime('04:00:00', "%H:%M:%S")

#off_campus = ['00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '56']
off_campus = ['00', '12', '13', '31', '34', '36', '39', '42', '44']

# remove 13, 36 because off campus
# removed 25, 41 missing whole row in psychology questionnaire data
id_home = {'01': ['kemeny', 'cutter-north', 'north-main'],
 '02': ['occum'],
 '03': ['north-park'],
 '04': ['ripley'],
 '05': ['massrow'],
 '07': ['east-wheelock'],
 '08': ['fahey-mclane', 'fayerweather'],
 '09': ['north-main'],
 '10': ['woodward'],
 '14': ['wheeler', 'rollins-chapel', 'college-street'],
 '15': ['massrow'],
 '16': ['massrow'],
 '17': ['gile'],
 '18': ['north-main'],
 '19': ['mclaughlin'],
 '20': ['north-park'],
 '22': ['massrow'],
 '23': ['north-park'],
 '24': ['occum'],
 '25': ['fayerweather'],
 '27': ['ripley'],
 '30': ['newhamp'],
 '32': ['massrow', 'parkhurst'],
 '33': ['channing-cox'],
 '35': ['north-park'],
 '41': ['ripley'],
 '43': ['butterfield']}

def get_major_loc(fp):

    lines = []
    
    ### group by dates
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
     
    ### only keep in[], ignore near[]
    in_loc = []
    for idx, pair in enumerate(by_dates):
        in_loc.append((pair[0], []))
        for entry in pair[1]:
            if entry[4].startswith('in'):
                in_loc[idx][1].append(entry)
       
    ### get a sequence of locations, its start time (line number)
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
     
    ### get its end time (line number)
    for idx, pair in enumerate(in_loc_duration):
        entries = pair[1]
        for i, entry in enumerate(entries):
            if i==len(entries)-1:
                end_index = len(in_loc[idx][1])-1
            else:
                end_index = entries[i+1][5]-1
            entry.append(end_index)
    #pprint(in_loc_duration)
     
    ### get duration, and cut by duration length
    for idx, pair in enumerate(in_loc_duration):
           
        in_loc_duration[idx] = (pair[0], [])
        entries = pair[1]
        for i, entry in enumerate(entries):
            time_start = in_loc[idx][1][entry[5]][1]
            time_end = in_loc[idx][1][entry[6]][1]
            duration = datetime.strptime(time_end, "%d%b%Y:%H:%M:%S") - datetime.strptime(time_start, "%d%b%Y:%H:%M:%S")
            duration = duration.seconds
            if duration >= DURATION_CUT:
                m_entry = []
                m_entry.append(entry[4])
                m_entry.append(time_start[-8:])
                m_entry.append(time_end[-8:])
                m_entry.append(duration)
                in_loc_duration[idx][1].append(m_entry)   
                
      

#     for pair in in_loc_duration:
#         dt = pair[0]
#         dt_obj = datetime.strptime(dt, "%d%b%Y")
#         weekday = dt_obj.strftime("%A")
#         if weekday == 'Sunday' or weekday == 'Saturday':
#             continue
#         print dt
#         pprint(pair[1])
    
    return in_loc_duration

def get_leaving_time(in_loc_duration, id):
    start_times = []
    
    for pair in in_loc_duration:
        dt = pair[0]
        seq = pair[1]
        dt_obj = datetime.strptime(dt, "%d%b%Y")

        #print dt   
        
        if dt_obj.strftime("%A") == 'Sunday' or dt_obj.strftime("%A") == 'Saturday':
            continue
        
        
        if id in off_campus:
            if seq:
                start_times.append(seq[0][1])
        else:
            for line in seq:
                loc = line[0][3:-1]
                start_time = time.strptime(line[1], "%H:%M:%S")
                if start_time > START_TIME_CUT and not loc in id_home[id]:
                    start_times.append(line[1])
                    #print line
                    break
    
    return start_times  

def calc_start_var(start_times):  

    avg = 0.0
    secs = []
    for t in start_times:  
        items = t.split(':')
        sec = int(items[0])*3600 + int(items[1])*60 + int(items[2])
        secs.append(sec)
        avg += sec
    avg /= len(start_times)
    
    var = 0.0
    for sec in secs:
        var += (sec - avg) * (sec - avg)
    
    var /= len(start_times)
    
    #print avg/3600, var/1000000
    
    #return avg/3600
    return var
    


def plot(result):
    id_y, label = get_y(3)
    
    y_values = []
    for id in id_home:
        #print id
        y_values.append(id_y[str(int(id))])
        
    plt.scatter(result, y_values)
    plt.show()
    
def get_feature():

    result_dict = {}
    for file in os.listdir(r'data\by subjects'):
        if not file.endswith('.csv'):
            continue
        id = file.split('.')[0][-2:]
        
        if int(id) >= 45:
            continue
        
        if id in off_campus:
            continue
        
        print '======================='
        print 'subject id: ' + id
        
        fp = os.path.join(r'data\by subjects', file)
        
        in_loc_duration = get_major_loc(fp)
  
        start_times = get_leaving_time(in_loc_duration, id)
        print start_times
        var = calc_start_var(start_times)
        print var

        result_dict[id] = var
        
    pprint(result_dict)
    return result_dict



if __name__ == "__main__":
#     fp = r'data\by subjects\wifigps_subject05.csv'
#     id = '05'
#     in_loc_duration = get_major_loc(fp)
#     start_times = get_leaving_time(in_loc_duration, id)
#     calc_start_var(start_times)
    
    id_start_time_var = get_feature()
    #plot(result)
    write_feature_to_csv('start_time_var', id_start_time_var)
    
