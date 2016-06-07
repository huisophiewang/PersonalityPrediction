import os

import pprint 
pp = pprint.PrettyPrinter(width=200)

from util import CUR_DIR, remove_subjects, write_feature_to_csv
from wifi import get_seqs, get_in_loc_duration
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')

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

    return var



def get_feature():
    id_feature = {}

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        
        id = file.split('.')[0][-2:]
        if id in remove_subjects:
            continue
        
        print '----------'
        print 'id: ' + id
    
        fp = os.path.join(wifi_dir, file)
        seqs = get_seqs(fp)
        #print seqs
        #print len(seqs)
        result = get_len_var(seqs)
        print result
        
        id_feature[id] = result
        
    return id_feature


if __name__ == '__main__':  
    id_feature = get_feature()
    #write_feature_to_csv(id_feature, 'len_var')
    
    