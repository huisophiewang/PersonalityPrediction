import os
from pprint import pprint
from util import CUR_DIR, write_feature_to_csv, write_multi_features_to_csv, fill_miss_values
from cookielib import DAYS
dir = os.path.join(CUR_DIR, "dataset", "sensing", "audio")



def get_feature():
    id_feature = {}
    for file in os.listdir(dir):
        if not file.endswith('datetime.csv'):
            continue       
        id = file[7:9]
        print '------'
        print "id: " + id
        
        fp = os.path.join(dir, file)
        fr = open(fp, 'rU') 
        lines = fr.readlines()
        count_date = set()
        
        for line in lines:
            items = line.rstrip(',\n').split(",")
            date = items[0][:10]
            count_date.add(date)
            
        days = len(count_date)
        print days
        id_feature[id] = days
        
    return id_feature
        
        
if __name__ == '__main__':  
    id_features = get_feature()
    write_feature_to_csv(id_features, 'num_days_audio')