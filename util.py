import os
import math
import time

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
traits = ['extra', 'agrbl', 'consc', 'neuro', 'openn']

# is 51 off-campus?
off_campus = ['00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '56']
# has less than 20 days: 39
# has less than 30 days: 24, 34, 50
# outliers for feature wifi_features: 49, 52
remove_subjects = off_campus
# need to remove for len_var to work
remove_subjects = set(off_campus).union(set(['39', '49', '52', '46']))
# need to remove for end_time_var to work
#remove_subjects = set(off_campus).union(set(['39', '49', '52', '25', '50']))
#remove_subjects = set(off_campus).union(set(['46', '47', '49', '50', '51', '52', '53', '54', '56', '57', '58', '59']))


start_time_cut = time.strptime('04:00:00', "%H:%M:%S")

# TODO: try to start from 4:00 am the next day, check locs in reverse order, use the first time loc appears
end_time_cut = time.strptime('15:00:00', "%H:%M:%S")

# TODO: home should be more accurate, try to do it again
id_home = {'01': ['kemeny', 'cutter-north', 'north-main'], # Phi Tau frat
 '02': ['occum'],  # Epsilon Kappa Theta soro
 '03': ['north-park'], # graduate
 '04': ['ripley'],  # north park
 '05': ['massrow'],  # school house
 '07': ['east-wheelock'], 
 '08': ['fahey-mclane', 'fayerweather'], # west
 '09': ['north-main'],  # Alpha Theta frat
 '10': ['woodward'],  # north park
 '14': ['wheeler', 'rollins-chapel', 'college-street'],  # first year house communities
 '15': ['massrow'],
 '16': ['massrow'],
 '17': ['gile'],  # Allen
 '18': ['north-main'],  # Alpha Theta frat
 '19': ['mclaughlin'],  # living learning communities
 '20': ['north-park'],
 '22': ['massrow'],
 '23': ['north-park'],
 '24': ['occum'],
 '25': ['fayerweather'],
 '27': ['ripley'],
 '30': ['newhamp'],  # South
 '32': ['massrow', 'parkhurst'],
 '33': ['channing-cox'],  # senior apartments
 '35': ['north-park'],
 '41': ['ripley'],
 '43': ['butterfield'],
 '46':['french','college-street'],
 '49':['little_hall'],
 '50':['north-park'],
 '52':['north-main', 'mclaughlin'],
 '53':['north-park'],
 '54':['maxwell'],
 '57':['north-main'],
 '58':['north-park'],
 '59':['butterfield']
 
 
 
 
 } # West




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

def z_score_normalize(dict):

    values = dict.values()
    n = len(values)
    mean = sum(values)/float(n)
    #print mean
    
    variance = 0.0 
    for value in values:
        variance += value*value
    variance /= float(n)
    variance = math.sqrt(variance - mean*mean)
    
    for key in dict:
        dict[key] = (dict[key] - mean) / variance
        
    return dict

## write normalized feature
def write_feature_to_csv(id_feature, feature_name):

    output_fp = os.path.join(CUR_DIR, 'result', 'feature', feature_name+'.csv')
    fw = open(output_fp, 'a')
    labels = ['uid', feature_name]
    labels.extend(traits) 
    fw.write(','.join(labels) + '\n')
    
    id_y = get_y()
    id_feature = z_score_normalize(id_feature)
                
    for id in sorted(id_feature):

        if not id in id_y:
            continue
        
        line = [id]   
        line.append("{0:.3f}".format(id_feature[id]))
          
        for value in id_y[id]:
            line.append(value)
          
        fw.write(','.join(line) + '\n')
        
    fw.close()