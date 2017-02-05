import json
from pprint import pprint
#pp = pprint.PrettyPrinter(width=100)

from prep_class_schedule import get_late_time
from util import write_feature_to_csv, write_multi_features_to_csv, fill_miss_values,\
    OFF_CAMPUS

to_weekday = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday'}
class_info_file = open(r'dataset\education\class_info.json')
class_info = json.load(class_info_file)

###########################
# missing: 00, 36, 39, 56 (probably dropped the course)
# ourlier for late_time_var (come to class too early): 13, 34, 35, 51, 

def get_ratio(result):
    num_pos, num_neg, num_na = 0, 0, 0
    for item in result:
        if item == 'NA':
            num_na += 1
        elif item > 0.0:
            num_pos += 1
        else:
            num_neg += 1
    
    absent_rate = float(num_na) / len(result)
    late_rate = float(num_pos) / len(result)
    early_rate = float(num_neg) / len(result)
    #print (early_rate, late_rate, absent_rate)
    ontime_rate = float(num_neg) / len(result)
    #return (early_rate, late_rate, absent_rate)
    return (ontime_rate, absent_rate)

def get_late_var(result):
    
    avg = 0.0
    count = 0
    for item in result:
        if item != 'NA':
            avg += item
            count += 1
    if count > 0:
        avg /= count
        
    #print avg
    #return avg
    var = 0.0
    for item in result:
        if item != 'NA':
            var += (item - avg) * (item - avg)
    if count > 0:
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
 
        id = items[0][1:]
        
#         if id in ['00', '36', '39', '56']:
#             continue
     
#         if id in ['13', '51', '34', '35']:
#             continue

        if id in OFF_CAMPUS + ['35']:
            continue
        
#         if id!='35':
#             continue
        
        print '=============='
        print "id: " + id
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
        
        result = get_late_time(id, schedule)
        #pprint(result)
        #print len(result)
        
        #feature = get_ratio(result)
        feature = get_late_var(result)
        
        id_feature[id] = feature
    return id_feature
        
if __name__ == '__main__':
    id_features = get_feature()
    #fill_miss_values(id_features, 3, ['00', '36', '39', '56'])
    #write_multi_features_to_csv(id_features, ['early', 'late', 'absent'])
    #write_multi_features_to_csv(id_features, ['early_oncampus', 'late_oncampus', 'absent_oncampus'])
    #write_multi_features_to_csv(id_features, ['ontime_rate_oncampus', 'absent_rate_oncampus'])
    
    #fill_miss_values(id_features, 1, ['00', '36', '39', '56'])
    #write_feature_to_csv(id_features, 'late_time_var')
    #write_feature_to_csv(id_features, 'late_time_var_oncampus')
    #write_feature_to_csv(id_features, 'late_time_avg_oncampus')
    write_feature_to_csv(id_features, 'late_time_var_oncampus')
    
    #get_class_schedule('01')