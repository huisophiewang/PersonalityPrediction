import os
from pprint import pprint
from util import CUR_DIR, write_feature_to_csv
dir = os.path.join(CUR_DIR, "dataset", "sensing", "bluetooth")

def nearby_count(fp):
    fr = open(fp, 'rU') 
    count_by_date = {}
    count_by_time = {}
    total = 0
    lines = fr.readlines()
    for line in lines:
        items = line.rstrip(',\n').split(",")
        total += 1
        
        timestamp = items[0]
        if not timestamp in count_by_time:
            count_by_time[timestamp] = 0
        count_by_time[timestamp] += 1
        
        date = timestamp[:10]
        if not date in count_by_date:
            count_by_date[date] = 0
        count_by_date[date] += 1
        
        
    #print len(count_by_date)   
    #pprint(count_by_date)
    #print len(count_by_date)
    #return float(total)/len(count_by_date)
    #return float(total)/len(count_by_time)
    return total



    
def get_feature(func):
    id_feature = {}
    for file in os.listdir(dir):
        if not file.endswith('datetime.csv'):
            continue       
        id = file[4:6]
        print '------'
        print "id: " + id
        fp = os.path.join(dir, file)
        result = func(fp)
        id_feature[id] = result

    pprint(id_feature)
    return id_feature
        

if __name__ == '__main__':  
    id_feature = get_feature(nearby_count)
    #write_feature_to_csv(id_feature, 'nearby_daily')  
    #write_feature_to_csv(id_feature, 'nearby_timestamp')
    #write_feature_to_csv(id_feature, 'nearby_total')



    