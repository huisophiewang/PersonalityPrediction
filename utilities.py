from pprint import pprint
import math
import os

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

id_entropy = {'00': 3.118727616978805,
 '01': 1.408777137368882,
 '02': 2.4568807161451063,
 '03': 0.6395246690055945,
 '04': 3.1119407396484644,
 '05': 2.315081319973245,
 '07': 1.6013338498459595,
 '08': 3.3148861609649036,
 '09': 2.307256679103043,
 '10': 2.173789832213921,
 '12': 2.0050181792797668,
 '13': 1.3942691269747995,
 '14': 2.8151986413288843,
 '16': 1.3788934505696804,
 '17': 1.1242050850627003,
 '18': 1.7084499687961445,
 '19': 2.7287022684323863,
 '20': 1.0210540068815712,
 '22': 1.8876842879939737,
 '27': 1.8095827369083115,
 '30': 2.8097768544248023,
 '31': 1.621032463168753,
 '32': 2.7292218598650586,
 '33': 1.4721500983949525,
 '35': 1.6923609773311215,
 '36': 1.7173211286959709,
 '41': 2.104094459509634,
 '42': 1.7868689378506994,
 '44': 1.3089701112746464,
 '46': 2.9501641363628264,
 '50': 1.2685025141704767,
 '51': 1.642932793433514,
 '52': 2.226831528083481,
 '53': 0.7933898052361501,
 '56': 1.9822730005686946,
 '57': 2.439825184451555,
 '58': 0.8120888511215856,
 '59': 3.0130183543037323}

id_edit_dist = {'00': 37.817460317460323,
 '01': 32.336507936507935,
 '02': 35.388888888888893,
 '03': 26.031746031746032,
 '04': 40.599206349206348,
 '05': 50.966666666666669,
 '07': 40.952380952380956,
 '08': 69.483333333333334,
 '09': 35.816666666666663,
 '10': 42.433333333333344,
 '12': 34.977777777777774,
 '13': 27.801587301587301,
 '14': 40.80238095238095,
 '15': 33.509523809523813,
 '16': 46.138888888888886,
 '17': 21.661111111111111,
 '18': 25.87222222222222,
 '19': 34.266666666666666,
 '20': 38.511904761904759,
 '22': 31.063492063492067,
 '23': 28.448412698412699,
 '24': 51.233333333333334,
 '25': 50.083333333333329,
 '27': 37.694444444444443,
 '30': 52.266666666666666,
 '31': 42.996825396825386,
 '32': 50.988095238095241,
 '33': 22.854761904761904,
 '34': 35.819047619047616,
 '35': 21.800000000000001,
 '36': 25.883333333333336,
 '39': 11.199999999999999,
 '41': 31.765873015873016,
 '42': 20.772222222222226,
 '43': 57.419047619047625,
 '44': 25.12539682539682,
 '45': 39.320634920634923,
 '46': 34.86904761904762,
 '47': 37.455555555555556,
 '49': 67.13095238095238,
 '50': 15.066666666666666,
 '51': 25.12222222222222,
 '52': 42.927777777777777,
 '53': 18.888888888888886,
 '54': 56.588095238095235,
 '56': 16.964285714285715,
 '57': 57.961111111111116,
 '58': 15.994444444444444,
 '59': 55.035714285714292}

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
        
   # print dict
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
    
if __name__ == '__main__':
    k=5
    for i in range(k):
        get_y_category(i+1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    