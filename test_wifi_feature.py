import csv
import copy
from pprint import pprint
from collections import OrderedDict
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from utilities import edit_dist, get_y, write_feature_to_csv, plot_all
from utilities import CUR_DIR, WIFI_COMMON_DAYS, WIFI_OFF_CAMPUS
from utilities import get_wifi_seqs

  


def avg_seq_len(seqs):
    avg_len = 0.0
    for seq in seqs:
        avg_len += len(seq)
    avg_len /= len(seqs)
    return avg_len

def num_pattern(seqs):
    pat = set()
    for seq in seqs:
        pat.add(','.join(seq))
        
    return len(pat)

def get_feature():
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
        
        seqs = get_wifi_seqs(fp, 60*10, 30)
        #result = avg_seq_len(seqs)
        result = num_pattern(seqs)
        print result
        
        id_feature[id] = result
        
    return id_feature
        
    


if __name__ == '__main__':  


#     fp = r'data\by subjects\wifigps_subject08.csv'
#     get_avg_edit_dist(fp)
    

    feature = get_feature()
    write_feature_to_csv('num_pattern', feature)


    
    
    
    
    
    
    
    
    
    
    
    
    