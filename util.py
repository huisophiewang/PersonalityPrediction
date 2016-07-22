import os
import math
import time
import pprint
from datetime import datetime

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
traits = ['extra', 'agrbl', 'consc', 'neuro', 'openn']


off_campus = ['00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '51', '56']

remove_subjects = off_campus
# need to remove outlier for feature_len_var to work
remove_subjects = set(off_campus).union(set(['46']))


id_home = {'01': ['kemeny', 'cutter-north'], # Phi Tau frat
 '02': ['occum'],  # Epsilon Kappa Theta soro
 '03': ['north-park'], # graduate
 '04': ['ripley'],  # north park
 '05': ['massrow'],  # school house
 '07': ['east-wheelock'], 
 '08': ['fahey-mclane', 'fayerweather'], # west
 '09': ['north-main'],  # Alpha Theta frat
 '10': ['woodward'],  # north park
 '14': ['wheeler', 'rollins-chapel'],  # first year house communities
 '15': ['massrow'],
 '16': ['massrow'],
 '17': ['gile'],  # Allen
 '18': ['north-main'],  # Alpha Theta frat
 '19': ['mclaughlin'],  # living learning communities
 '20': ['north-park'],
 '22': ['massrow', 'lord'],
 '23': ['north-park'],
 '24': ['occum'],
 '25': ['fayerweather', 'lodge'],
 '27': ['ripley'],
 '30': ['newhamp'],  # South
 '32': ['massrow', 'parkhurst'],
 '33': ['channing-cox'],  # senior apartments
 '35': ['north-park'],
 '41': ['ripley'],
 '43': ['butterfield'],
 '46':['french'],
 '49':['little_hall'],
 '50':['north-park'],
 '52':['north-main', 'mclaughlin'],
 '53':['north-park'],
 '54':['maxwell'],
 '57':['north-main'],
 '58':['north-park'],
 '59':['butterfield']
 } 




def get_y():
    id_y = {}
    fp = os.path.join(CUR_DIR, 'dataset', 'survey', 'BigFivePre.csv')
    fr = open(fp, 'rU')
    fr.readline()
    lines = fr.readlines()
    for line in lines:
        items = line.strip('\n').split(",")
        id = items[0][1:]
        value = items[1:]
        id_y[id] = value            
    return id_y

def z_score_normalize(dic):

    values = dic.values()
    n = len(values)
    mean = sum(values)/float(n)
    #print mean
    
    variance = 0.0 
    for value in values:
        variance += value*value
    variance /= float(n)
    variance = math.sqrt(variance - mean*mean)
    
    for key in dic:
        dic[key] = (dic[key] - mean) / variance 
    return dic

## write normalized feature
def write_feature_to_csv(id_feature, feature_name, normalize=True):

    output_fp = os.path.join(CUR_DIR, 'result', 'feature', feature_name+'.csv')
    fw = open(output_fp, 'a')
    labels = ['uid', feature_name]
    labels.extend(traits) 
    fw.write(','.join(labels) + '\n')
    
    if normalize:
        id_feature = z_score_normalize(id_feature)
    id_y = get_y()             
    for id in sorted(id_feature):
        if not id in id_y:
            continue       
        line = [id]   
        line.append("{0:.3f}".format(id_feature[id]))    
        line.extend(id_y[id])         
        fw.write(','.join(line) + '\n')     
    fw.close()
    
def write_multi_features_to_csv(id_features, feature_names, normalize=True):
    
    output_fp = os.path.join(CUR_DIR, 'result', 'feature', '-'.join(feature_names)+'.csv')
    fw = open(output_fp, 'a')
    labels = ['uid']
    labels.extend(feature_names)       
    labels.extend(traits) 
    fw.write(','.join(labels) + '\n')
    
    features = []
    for i in range(len(feature_names)):
        id_feature = {k:v[i] for k, v in id_features.iteritems()}
        if normalize:
            id_feature = z_score_normalize(id_feature)
        features.append(id_feature)
        
    id_y = get_y()  
    for id in sorted(id_features.keys()):
        if not id in id_y:
            continue
        line = [id]   
        for i in range(len(feature_names)):
            line.append("{0:.3f}".format(features[i][id]))        
        line.extend(id_y[id])      
        fw.write(','.join(line) + '\n')     
    fw.close()
    
def to_datetime(folder, filename, id):
    dir = r'C:\Users\Sophie\workspace\Personality\dataset\sensing'
    input_fp = os.path.join(dir, folder, '%s_u%02d.csv' % (filename, id))  
    output_fp = os.path.join(dir, folder, '%s_u%02d_datetime.csv' % (filename, id))
    
    if not os.path.exists(input_fp) or os.path.exists(output_fp):
        return
    
    print output_fp
    
    fr = open(input_fp, 'rU') 
    fw = open(output_fp, 'a')
    fr.readline()
    lines = fr.readlines()
    for line in lines:
        if line == '\n':
            continue
        items = line.rstrip(',\n').split(",")
        #print items
        dt = datetime.fromtimestamp(int(items[0])).strftime('%Y-%m-%d-%H:%M:%S')
        #dt_end = datetime.fromtimestamp(int(items[1])).strftime('%Y-%m-%d-%H:%M:%S')
        outline = [dt]
         
        outline.extend(items[1:])
        #print outline
        fw.write(','.join(outline) + '\n')
    fw.close()
    
def get_entropy(item_freq):
    entropy = 0.0
    total = sum(item_freq.values())
    for item in item_freq:
        if item_freq[item]:
            p = item_freq[item]/float(total)
            entropy += (-p) * math.log(p, 2)       
    return entropy

def get_time_var(times):  
    avg = 0.0
    secs = []
    for t in times:  
        items = t.split(':')
        sec = int(items[0])*3600 + int(items[1])*60 + int(items[2])
        secs.append(sec)
        avg += sec
    avg /= len(times)
    
    var = 0.0
    for sec in secs:
        var += (sec - avg) * (sec - avg)
    var /= len(times)
    return var
        
if __name__ == '__main__':
#     id_features = {'01':(1,2,3), '02':(4,5,6)}
#     write_multi_features_to_csv(id_features, ['a', 'b', 'c'], False)

    for id in range(60):
        to_datetime('bluetooth', 'bt', id)
    

            
    
        
    