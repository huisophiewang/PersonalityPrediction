from pprint import pprint
import math
import os

import numpy as np
import matplotlib.pyplot as plt

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

LABELS = ['extra', 'agrbl', 'consc', 'neuro', 'open', 
          'assertive', 'activity', 'altruism', 'compliance', 'order', 'discipline', 'anxiety', 'depression', 'aesthetics', 'ideas']

WIFI_OFF_CAMPUS = ['00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '56']

WIFI_COMMON_DAYS = ['22APR2013', '12APR2013', '13APR2013', '19APR2013', '07APR2013', 
                    '06APR2013', '09APR2013', '08APR2013', '03APR2013', '15APR2013', 
                    '01APR2013', '02APR2013', '14APR2013', '04APR2013', '21APR2013', 
                    '05APR2013', '27MAR2013', '10APR2013', '11APR2013', '23APR2013']

# remove 13, 36 because off campus
# removed 25, 41 missing whole row in psychology questionnaire data
WIFI_ID_HOME = {'01': ['kemeny', 'cutter-north', 'north-main'],
 '02': ['occum'],
 '03': ['north-park'],
 '04': ['ripley'],
 '05': ['massrow'],
 '07': ['east-wheelock'],
 '08': ['fahey-mclane', 'fayerweather'],
 '09': ['north-main'],
 '10': ['woodward'],
 '14': ['wheeler', 'rollins-chapel', 'college-street'],
 '15': ['massrow'],
 '16': ['massrow'],
 '17': ['gile'],
 '18': ['north-main'],
 '19': ['mclaughlin'],
 '20': ['north-park'],
 '22': ['massrow'],
 '23': ['north-park'],
 '24': ['occum'],
 '25': ['fayerweather'],
 '27': ['ripley'],
 '30': ['newhamp'],
 '32': ['massrow', 'parkhurst'],
 '33': ['channing-cox'],
 '35': ['north-park'],
 '41': ['ripley'],
 '43': ['butterfield']}

WIFI_ALL_LOCS = ['53_commons',
    '7-lebanon',
    'HanoverInn',
    'Mckenzie',
    'baker-berry',
    'batrlett',
    'blunt_alumni_center',
    'butterfield',
    'byrnehall',
    'carpenterhall',
    'carson-tech_services',
    'channing-cox',
    'college-street',
    'cummings',
    'cutter-north',
    'dana-library',
    'dartmouth_hall',
    'dewey',
    'east-wheelock',
    'fahey-mclane',
    'fairbanks',
    'fairchild',
    'fayerweather',
    'gile',
    'hanoverpsych',
    'hitchcock',
    'home',
    'hopkins',
    'isr_wireless',
    'kemeny',
    'library-default-services',
    'little_hall',
    'lodge',
    'lord',
    'lsb',
    'maclean',
    'massrow',
    'maxwell',
    'mclaughlin',
    'moore',
    'murdough',
    'north-main',
    'north-park',
    'occum',
    'reed',
    'remote_offices_HREAP',
    'ripley',
    'robinson',
    'ropeferry',
    'sanborn',
    'silsby-rocky',
    'softballfield',
    'sport-venues',
    'sport-venues-press',
    'steele',
    'streeter',
    'sudikoff',
    'thayer_secure',
    'tllc-raether',
    'topliff',
    'vac',
    'wentworth',
    'woodward']

def edit_dist(s,t):
    if not s:
        return len(t)
    
    if not t:
        return len(s)
    
    d = {}
    S = len(s)
    T = len(t)
    for i in range(S):
        d[i, 0] = i
    for j in range (T):
        d[0, j] = j
    for j in range(1,T):
        for i in range(1,S):
            if s[i] == t[j]:
                d[i, j] = d[i-1, j-1]
            else:
                d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + 1)
    #pprint(d)
    return d[S-1, T-1]

# Euclidean distance of x1 and x2, k dimenstion 
def distance(x1, x2, k):
    dist = 0.0
    for i in range(k):
        dist += math.pow((x1[i]-x2[i]), 2)
    dist = math.sqrt(dist)
    return dist

def KL_divergence(p, q, k):
    dist = 0.0
    for i in range(k):
        if q[i] != 0 and p[i] != 0:
            dist += p[i] * math.log(p[i]/q[i], 2)
    return dist

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
        dict[key] = str((dict[key] - mean) / variance)
        
    return dict

def get_y(col):
    id_y = {}
    with open(r'data\FiveFactors.csv', 'rU') as fr:
        labels = fr.readline().split(',')
        lines = fr.readlines()
        for line in lines:
            if line == '\n':
                continue
            #print line
            atts = line.strip('\n').split(",")
            if atts[col]:
                id = atts[0]
                id = '%02d' % int(id)
                id_y[id] = float(atts[col])
    return id_y, labels[col]

def get_y_category(col):
    id_y = {}
    count_low = 0
    count_high = 0
    with open(r'data\FiveFactors.csv', 'rU') as fr:
        labels = fr.readline().split(',')
        lines = fr.readlines()
        for line in lines:
            if line == '\n':
                continue
            #print line
            atts = line.strip('\n').split(",")
            if atts[col]:
                id = atts[0]
                id = '%02d' % int(id)
                y = float(atts[col])
                if y <= 3:
                    id_y[id] = 'L'
                    count_low += 1
                else:
                    id_y[id] = 'H'
                    count_high += 1
    
    print labels[col]
    #pprint(id_y)
    print count_low, count_high
    return id_y, labels[col]

def get_all_y():
    personality = {}
    fr = open(r'data\FiveFactors.csv', 'rU')
    fr.readline()
    lines = fr.readlines()
    for line in lines:
        if line == '\n':
            continue
        #print line
        atts = line.strip('\n').split(",")

        id = atts[0]
        id = '%02d' % int(id)
        value = atts[1:16]
        #print value
        personality[id] = value
            
    return personality

def write_feature_to_csv(feature_name, id_feature):

    output_fp = os.path.join(CUR_DIR, 'data', 'matrix_data', 'feature_' + feature_name+'.csv')
    fw = open(output_fp, 'a')
    labels = ['subject_id', feature_name, 'extra', 'agrbl', 'consc', 'neuro', 'open']
    labels.extend(['assertive', 'activity', 'altruism', 'compliance', 'order', 'discipline', 'anxiety', 'depression', 'aesthetics', 'ideas'])
    fw.write(','.join(labels) + '\n')
    
    
    id_all_y = get_all_y()
    id_feature = z_score_normalize(id_feature)
                
    for id in sorted(id_feature):

        if not id in id_all_y:
            continue
        
        line = [id]     
        line.append(str(id_feature[id]))
          
        for value in id_all_y[id]:
            line.append(value)
          
        fw.write(','.join(line) + '\n')
        
    fw.close()
    
def plot_all(id_feature):


    cols = range(1, 16)

    for index, i in enumerate(cols):

        id_y, y_label = get_y(i)    
    
        id_values = {}
        for id in id_feature:
            #print id
            if id in id_y:
                id_values[id] = (id_feature[id], id_y[id])
            else:
                id_values[id] = None
         
        x_values = []
        y_values = []
        id_values = sorted(id_values.items(), key=lambda x: int(x[0]))   
         
    
        for item in id_values:
            if item[1]:
                x_values.append(item[1][0])
                y_values.append(item[1][1])

        
        plt.subplot(8, 2, index+1)
        #plt.subplot(2, 1, index+1)
        plt.scatter(x_values,y_values)
        plt.ylabel(y_label)
        
    
    plt.show()
    
def replace_nan(data, y_col):
    y_avg = 0.0
    count = 0
    y = data[:, y_col]
    for i in range(data.shape[0]):
        if not np.isnan(y[i]):
            y_avg += y[i]
            count += 1

    y_avg /= count
    y[np.isnan(y)] = y_avg
    
if __name__ == '__main__':
    k=5
    for i in range(k):
        get_y_category(i+1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    