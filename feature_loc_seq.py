import os
import numpy as np

import pprint 
pp = pprint.PrettyPrinter(width=200)

from util import CUR_DIR, REMOVE_SUBJECTS, OFF_CAMPUS
from util import write_feature_to_csv, edit_dist, write_multi_features_to_csv
from prep_wifi_loc import get_seqs, get_seqs_by_weekday
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')

#############################
# outlier (off-campus): '00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '51', '56'
# outlier: 46

def get_len_var(seqs):
    n = len(seqs)
    
    mean = 0.0
    for i in range(n):
        mean += len(seqs[i])
    mean /= n
    
    var = 0.0
    for i in range(n):
        var += (len(seqs[i]) - mean)*(len(seqs[i]) - mean)
    var /= n
    
    #return mean
    return var
    

def get_avg_edit_dist(seqs):
    n = len(seqs)
     
    avg = 0
    dists = np.zeros((n, n))
    for i in range(n):
        for j in range(i,n):
            dists[i][j] = edit_dist(seqs[i], seqs[j])
            avg += dists[i][j]
      
    avg /= float(n*(n-1)/2)
    return avg

def get_feature():
    id_feature = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]
        
        if id in OFF_CAMPUS:
            continue
    
        print '----------'
        print 'id: ' + id

        seqs = get_seqs(id)
        #print seqs
        #print len(seqs)
        result = get_len_var(seqs)
        #result = get_avg_edit_dist(seqs)
        print result
        
        id_feature[id] = result
        
    return id_feature

def get_feature_weekday():
    id_features = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]
        
        if id in OFF_CAMPUS:
            continue
    
        print '----------'
        print 'id: ' + id
        
        result = []
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            day_seqs = get_seqs_by_weekday(id, day)

            result.append(get_len_var(day_seqs))
            #result = get_avg_edit_dist(seqs)

        print result
        id_features[id] = result
        
    return id_features

if __name__ == '__main__':  
    #id_feature = get_feature()
    #pp.pprint(id_feature)
    #write_feature_to_csv(id_feature, 'len_var', False)

    #pp.pprint(get_seqs('46'))
    
    #write_feature_to_csv(id_feature, 'len_mean')
    #write_feature_to_csv(id_feature, 'len_var_oncampus')
    #write_feature_to_csv(id_feature, 'len_mean_oncampus')
    #write_feature_to_csv(id_feature, 'avg_edit_dist')
    
    id_features = get_feature_weekday()
    #write_multi_features_to_csv(id_features, ['len_mean_Mon', 'len_mean_Tue', 'len_mean_Wed', 'len_mean_Thr', 'len_mean_Fri'])
    write_multi_features_to_csv(id_features, ['len_var_mon', 'len_var_tue', 'len_var_wed', 'len_var_thr', 'len_var_fri'])
    
    