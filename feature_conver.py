import os
from pprint import pprint
from datetime import datetime
from util import write_feature_to_csv, OFF_CAMPUS, write_multi_features_to_csv
dir = r'C:\Users\Sophie\workspace\Personality\dataset\sensing\conversation'

def freq(id):
    dt_freq = {}
    fp = os.path.join(dir, r'conversation_u%s_datetime.csv' % id)
    fr = open(fp, 'rU') 
    lines = fr.readlines()
    by_day_day, by_day_evening, by_day_night = {}, {}, {}
    for line in lines:
        items = line.rstrip(',\n').split(",")
        date = items[0][:10]
#         weekday = datetime.strptime(dt, "%Y-%m-%d").strftime("%A")
#         if weekday in ['Saturday', 'Sunday']:
#             continue
        hour = int(items[0][11:13])
        #print items[0]
#         if not dt in dt_freq:
#             dt_freq[dt] = 0
#         dt_freq[dt] += 1
#     pp.pprint(dt_freq)
#     
#     total = 0
#     for dt in dt_freq:
#         total += dt_freq[dt]
#     avg = float(total) / len(dt_freq)
    #print avg
    #return avg
    
        if hour >= 9 and hour < 18:
            if not date in by_day_day:
                by_day_day[date] = 0
            by_day_day[date] += 1
        elif hour >= 18 and hour <= 23:
            if not date in by_day_evening:
                by_day_evening[date] = 0
            by_day_evening[date] += 1
        else:
            if not date in by_day_night:
                by_day_night[date] = 0
            by_day_night[date] += 1   
            
    #pprint(by_day_day)
    
    daily_day = 0.0
    for dt in by_day_day:
        daily_day += by_day_day[dt]
    if len(by_day_day):
        daily_day /= len(by_day_day)
      
      
    daily_evening = 0.0
    for dt in by_day_evening:
        daily_evening += by_day_evening[dt]
    if len(by_day_evening):
        daily_evening /= len(by_day_evening)
  
       
    daily_night = 0.0
    for dt in by_day_night:
        daily_night += by_day_night[dt]
    if len(by_day_night):
        daily_night /= len(by_day_night)
  
    print (daily_day, daily_evening, daily_night)
    return (daily_day, daily_evening, daily_night)


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
    pprint(dt_dur)
    
    total = 0
    for dt in dt_dur:
        total += dt_dur[dt]
    
    avg = float(total) / len(dt_dur)
#     print avg
    return avg
    #return total
        
    
    
    
def get_feature(func):
    id_feature = {}
    for file in os.listdir(dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue        
        id = file.split('.')[0][-2:]

        if id in OFF_CAMPUS:
            continue

#         if id != '01':
#             continue
        
        print '----------'
        print 'id: ' + id
        
        result = func(id)   
        id_feature[id] = result
        
    return id_feature     

if __name__ == '__main__':  
    id_feature = get_feature(freq)
    #write_feature_to_csv(id_feature, 'conver_freq')
    #write_feature_to_csv(id_feature, 'conver_freq_oncampus')
    #write_multi_features_to_csv(id_feature, ['conver_freq_daytime_oncampus', 'conver_freq_evening_oncampus', 'conver_freq_night_oncampus'])

    id_feature = get_feature(duration)
    #write_feature_to_csv(id_feature, 'conver_dur_avg') 
    #write_feature_to_csv(id_feature, 'conver_dur_avg_oncampus') 
    #write_feature_to_csv(id_feature, 'conver_dur_total')  
    #write_feature_to_csv(id_feature, 'conver_dur_total_oncampus')  