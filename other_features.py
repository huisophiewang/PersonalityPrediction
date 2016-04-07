import os
from pprint import pprint
import numpy as np

from utilities import edit_dist, write_feature_to_csv, write_raw_feature_to_csv
from utilities import CUR_DIR, WIFI_OFF_CAMPUS
from utilities import get_wifi_seqs

def get_avg_len(seqs):
    avg_len = 0
    num_days = len(seqs)
    for seq in seqs:
        avg_len += len(seq)
    avg_len /= float(num_days)
    return avg_len

def get_num_patterns(seqs):
    patterns = set()
    for seq in seqs:
        seq_str = ','.join(seq)
        if not seq_str in patterns:
            patterns.add(seq_str)            
    return len(patterns)

def get_len_var(seqs):
    num_days = len(seqs)
    avg_len = get_avg_len(seqs)
    var = 0
    for seq in seqs:
        var += (len(seq) - avg_len)*(len(seq) - avg_len)
    var /= float(num_days)
    return var

        
    
def get_feature(func):
    id_feature = {}
    addr_dir = os.path.join(CUR_DIR, 'data', 'by_subjects')
    for file in os.listdir(addr_dir):
        if not file.endswith('.csv'):
            continue
        
        id = file.split('.')[0][-2:]
        if int(id) >= 45:
            continue     
        if id in WIFI_OFF_CAMPUS:
            continue
        fp = os.path.join(addr_dir, file)
        print '----------'
        print 'id: ' + id
        
        seqs = get_wifi_seqs(fp, 60*10, 20)
        #pprint(seqs)
        #print len(seqs)
        for seq in seqs:
            print seq
        
        result = func(seqs)
        print result
        
        id_feature[id] = result
        
    return id_feature
        
    


if __name__ == '__main__':  
    #id_avg_len = get_feature()
    #write_feature_to_csv('avg_len', id_avg_len)
    

    #id_num_patterns = get_feature(get_num_patterns)
    #write_feature_to_csv('num_patterns', id_num_patterns)
    
    id_len_var = get_feature(get_len_var)
    write_feature_to_csv('len_var', id_len_var)

    
    
    
    