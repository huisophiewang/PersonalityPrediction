import json
import pprint
pp = pprint.PrettyPrinter(width=100)

from prep_class_schedule import get_late_time
from util import write_feature_to_csv, write_multi_features_to_csv

to_weekday = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday'}
class_info_file = open(r'dataset\education\class_info.json')
class_info = json.load(class_info_file)

def get_ratio(result):
    num_pos, num_neg, num_na = 0, 0, 0
    for item in result:
        if item == 'NA':
            num_na += 1
        elif item <= 0.0:
            num_neg += 1
        else:
            num_pos += 1
    
    absent_rate = float(num_na) / len(result)
    late_rate = float(num_pos) / len(result)
    early_rate = float(num_neg) / len(result)
    #print (early_rate, late_rate, absent_rate)
    return (early_rate, late_rate, absent_rate)

def get_late_var(result):
    avg = 0
    count = 0
    for item in result:
        if item != 'NA':
            avg += item
            count += 1
    avg /= count
    
    var = 0.0
    for item in result:
        if item != 'NA':
            var += (item - avg) * (item - avg)
    var /= count
    
    return var

def get_class_schedule(id):
    fr = open(r'dataset\education\class.csv', 'rU')
    lines = fr.readlines()
    for line in lines:
        items = line.rstrip().split(',') 
        if len(items) <= 1:
            continue    
        # found id line
        if id == items[0][1:]:
            schedule = {}
            for item in items[1:]:
                if item in class_info:
                    info = class_info[item]
                    loc = info['location']
                    periods = info['periods']
                    # organize by weekday
                    for period in periods:
                        wkd = to_weekday[period['day']]
                        if not wkd in schedule:
                            schedule[wkd] = []
                        start = period['start']
                        end = period['end']
                        schedule[wkd].append((loc, start, end))
            # sort by start time
            for wkd in schedule:
                schedule[wkd].sort(key=lambda tup:tup[1])
            #pp.pprint(schedule)
            return schedule  
        
def get_feature():
    id_feature = {}
    fr = open(r'dataset\education\class.csv', 'rU')
    lines = fr.readlines()
    for line in lines:
        items = line.rstrip().split(',') 
        if len(items) <= 1:
            continue    
        id = items[0][1:]
     
        if id in ['13', '51', '34', '35']:
            continue
        
        print '=============='
        print id
        schedule = {}
        for item in items[1:]:
            if item in class_info:
                info = class_info[item]
                loc = info['location']
                periods = info['periods']
                # organize by weekday
                for period in periods:
                    wkd = to_weekday[period['day']]
                    if not wkd in schedule:
                        schedule[wkd] = []
                    start = period['start']
                    end = period['end']
                    schedule[wkd].append((loc, start, end))
        # sort by start time
        for wkd in schedule:
            schedule[wkd].sort(key=lambda tup:tup[1])
        pp.pprint(schedule)  
        
        result = get_late_time(id, schedule)
        #feature = get_ratio(result)
        feature = get_late_var(result)
        
        id_feature[id] = feature
    return id_feature
        
if __name__ == '__main__':
    #id_features = get_feature()
    #write_multi_features_to_csv(id_features, ['early', 'late', 'absent'], False)
    
    id_feature = get_feature()
    write_feature_to_csv(id_feature, 'late_var')