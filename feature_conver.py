import os
import pprint 
from datetime import datetime
from util import write_feature_to_csv
pp = pprint.PrettyPrinter(width=200)
dir = r'C:\Users\Sophie\workspace\Personality\dataset\sensing\conversation'

def freq(id):
    dt_freq = {}
    fp = os.path.join(dir, r'conversation_u%s_datetime.csv' % id)
    fr = open(fp, 'rU') 
    lines = fr.readlines()
    for line in lines:
        items = line.rstrip(',\n').split(",")
        dt = items[0][:10]
#         weekday = datetime.strptime(dt, "%Y-%m-%d").strftime("%A")
#         if weekday in ['Saturday', 'Sunday']:
#             continue
        if not dt in dt_freq:
            dt_freq[dt] = 0
        dt_freq[dt] += 1
    pp.pprint(dt_freq)
    
    total = 0
    for dt in dt_freq:
        total += dt_freq[dt]
    avg = float(total) / len(dt_freq)
    print avg
    return avg


def duration(id):
    dt_dur = {}
    fp = os.path.join(dir, r'conversation_u%s_datetime.csv' % id)
    fr = open(fp, 'rU') 
    lines = fr.readlines()
    for line in lines:
        items = line.rstrip(',\n').split(",")
        dt = items[0][:10]
        start_time = items[0][-8:]
        end_time = items[1][-8:]
        duration =  datetime.strptime(end_time, "%H:%M:%S") - datetime.strptime(start_time, "%H:%M:%S")
        duration = duration.seconds
        if not dt in dt_dur:
            dt_dur[dt] = 0
        dt_dur[dt] += duration
    pp.pprint(dt_dur)
    
    total = 0
    for dt in dt_dur:
        total += dt_dur[dt]
    
#     avg = float(total) / len(dt_dur)
#     print avg
#     return avg
    return total
        
    
    
    
def get_feature(func):
    id_feature = {}
    for file in os.listdir(dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue        
        id = file.split('.')[0][-2:]

        print '----------'
        print 'id: ' + id
            
        result = func(id)   
        #result = duration(id)
        id_feature[id] = result
        
    return id_feature     

if __name__ == '__main__':  
#     id_feature = get_feature(freq)
#     write_feature_to_csv(id_feature, 'conver_freq')

    id_feature = get_feature(duration)
    #write_feature_to_csv(id_feature, 'conver_dur_avg') 
    write_feature_to_csv(id_feature, 'conver_dur_total')  