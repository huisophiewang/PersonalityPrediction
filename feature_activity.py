import os
from pprint import pprint
from util import CUR_DIR, write_feature_to_csv, write_multi_features_to_csv, fill_miss_values,\
    OFF_CAMPUS
dir = os.path.join(CUR_DIR, "dataset", "sensing", "activity")



def get_feature():
    id_feature = {}
    for file in os.listdir(dir):
        if not file.endswith('datetime.csv'):
            continue       
        id = file[10:12]
        print '------'
        print "id: " + id
        
#         if id in ['59']:
#             continue
        #if id in OFF_CAMPUS + ['52']:
        if id in OFF_CAMPUS:
            continue

        fp = os.path.join(dir, file)
        fr = open(fp, 'rU') 
        lines = fr.readlines()
        count_date = set()
        total_stat, total_walk, total_run, total_unknown = 0, 0, 0, 0

        for line in lines:

            items = line.rstrip(',\n').split(",")
            date = items[0][:10]
            count_date.add(date)
            if items[1] == '0':
                total_stat += 1
            elif items[1] == '1':
                total_walk += 1
            elif items[1] == '2':
                total_run += 1
            elif items[1] == '3':
                total_unknown += 1
        
        

        #print days
        
        total = total_stat + total_walk + total_run + total_unknown
        #print total/float(days)

            
#         rate_stat, rate_walk, rate_run = total_stat/float(total), total_walk/float(total), total_run/float(total)
#         id_feature[id] = (rate_stat, rate_walk, rate_run)
#         
#         rate_stat, rate_act = total_stat/float(total), (total_walk+total_run)/float(total)
#         id_feature[id] = (rate_stat, rate_act)
        
        #id_feature[id] = (total_stat, total_walk+total_run)
       
        
#         daily_stat, daily_walk, daily_run = total_stat/float(days), total_walk/float(days), total_run/float(days)
#         id_feature[id] = (daily_stat, daily_walk, daily_run)

        days = len(count_date)
        id_feature[id] = days
        
        
        
        
    return id_feature

if __name__ == '__main__':  
    id_features = get_feature()
    #pprint(id_features)
    
    #fill_miss_values(id_features, 3, ['52'])
    #write_multi_features_to_csv(id_features, ['stat_rate', 'walk_rate', 'run_rate'])
    #write_multi_features_to_csv(id_features, ['stat_rate_oncampus', 'walk_rate_oncampus', 'run_rate_oncampus'])
    #write_multi_features_to_csv(id_features, ['stat_rate', 'act_rate'])
    
    #fill_miss_values(id_features, 2, ['59'])
    #write_multi_features_to_csv(id_features, ['stat_total', 'walk_total', 'run_total'])
    #write_multi_features_to_csv(id_features, ['stat_total', 'act_total'])
    
    #write_feature_to_csv(id_features, 'num_days_activity')
    write_feature_to_csv(id_features, 'num_days_activity_oncampus', normalize=True)
    
    #fill_miss_values(id_features, 3, ['59'])
    #write_multi_features_to_csv(id_features, ['stat_daily', 'walk_daily', 'run_daily'])
    

    
