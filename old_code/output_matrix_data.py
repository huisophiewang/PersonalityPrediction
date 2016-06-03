import os
import math
from pprint import pprint

from utilities import get_all_y, get_y, LABELS
cur_dir = os.path.dirname(os.path.realpath(__file__))

ids = ['01', '02', '03', '04', '05', 
       '07', '08', '09', '10', '14', 
       '15', '16', '17', '18', '19', 
       '20', '22', '23', '24', '27', 
       '30', '32', '33', '35', '43']
        

# assume all feature files contain those 25 subjects in ids
def read_feature(feature):
    id_feature = {}
    input_fp = os.path.join(cur_dir, 'data', 'matrix_data', 'feature_' + feature + '.csv')
    fr = open(input_fp, 'rU')
    fr.readline()
    lines = fr.readlines()
    for line in lines:
        atts = line.strip('\n').split(",")
        id_feature[atts[0]] = atts[1]
        #feature_value.append(atts[1])
    return id_feature

def write_all_wifi_features(features, raw=False):
    if raw:
        output_fp = os.path.join(cur_dir, 'data', 'matrix_data', 'all_wifi_features_raw.csv')
    else:
        output_fp = os.path.join(cur_dir, 'data', 'matrix_data', 'all_wifi_features.csv')
    fw = open(output_fp, 'a')
    
    all_features = {}
    for feature in features:
        id_feature = read_feature(feature)
        all_features[feature] = id_feature
        
    all_y = get_all_y()
    
    labels = ['subject_id']
    labels.extend(features)
    labels.extend(LABELS)
    fw.write(','.join(labels) + '\n')
    
    for id in ids:
        line = [id]
        for feature in features:
            line.append(all_features[feature][id])
        line.extend(all_y[id])
        fw.write(','.join(line) + '\n')
        
    fw.close()   
    
def write_wifi_features_for_knn():
    for i in range(1, 16):
        id_y, label = get_y(i)
        label = LABELS[i-1]
        output_fp = os.path.join(cur_dir, 'data', 'matrix_data', 'for_knn', 'wifi_features',  label + '.csv')
        fw = open(output_fp, 'a')
          
        all_features = {}
        features = ['edit_dist', 'start_time_var', 'end_time_var']
        for feature in features:
            id_feature = read_feature(feature)
            all_features[feature] = id_feature
            
        labels = ['subject_id']
        labels.extend(features)
        labels.append(label)
        fw.write(','.join(labels) + '\n')
        
        for id in ids:
            line = [id]
            for feature in features:
                line.append(all_features[feature][id])
            if id in id_y:
                line.append(str(id_y[id]))
            else:
                line.append('')
            fw.write(','.join(line) + '\n')
            
        fw.close()
    
if __name__ == '__main__':

    features = ['edit_dist', 'len_diff', 'len_var', 'avg_len', 'num_patterns', 'start_time_var', 'end_time_var',
                'fp_home', 'fp_lsb', 'fp_hopkins', 'fp_sudikoff', 'fp_53_commons', 'fp_baker-berry', 'fp_sport-venues']
    #features = ['raw_edit_dist', 'raw_len_diff', 'raw_start_time_var', 'raw_end_time_var']
    write_all_wifi_features(features, False)
    #write_wifi_features_for_knn()
    
    