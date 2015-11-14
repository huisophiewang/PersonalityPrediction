import os
import math

cur_dir = os.path.dirname(os.path.realpath(__file__))

ids = ['01', '02', '03', '04', '05', 
       '07', '08', '09', '10', '14', 
       '15', '16', '17', '18', '19', 
       '20', '22', '23', '24', '27', 
       '30', '32', '33', '35', '43']

# sum of weekday average edit distance, on campus subjects, 20 complete days
avg_edit_dist = {'01': 31.476190476190474,
 '02': 18.523809523809526,
 '03': 10.0,
 '04': 39.571428571428569,
 '05': 33.285714285714285,
 '07': 31.285714285714285,
 '08': 30.0,
 '09': 24.714285714285715,
 '10': 18.38095238095238,
 '14': 38.428571428571431,
 '15': 26.238095238095237,
 '16': 20.333333333333332,
 '17': 20.38095238095238,
 '18': 23.857142857142858,
 '19': 23.047619047619044,
 '20': 18.19047619047619,
 '22': 25.80952380952381,
 '23': 11.761904761904763,
 '24': 25.666666666666668,
 '25': 30.19047619047619,
 '27': 16.952380952380953,
 '30': 36.0,
 '32': 40.523809523809518,
 '33': 18.80952380952381,
 '35': 20.0,
 '41': 26.047619047619047,
 '43': 26.476190476190474}

# number of different sequences, on campus subjects, 20 complete days
num_patterns = {'01': 15,
 '02': 15,
 '03': 7,
 '04': 15,
 '05': 15,
 '07': 15,
 '08': 15,
 '09': 15,
 '10': 15,
 '14': 15,
 '15': 15,
 '16': 15,
 '17': 14,
 '18': 15,
 '19': 15,
 '20': 12,
 '22': 15,
 '23': 11,
 '24': 14,
 '25': 15,
 '27': 13,
 '30': 15,
 '32': 15,
 '33': 15,
 '35': 14,
 '41': 15,
 '43': 15}

start_time_var = {'00': 132352429.2986111,
 '01': 57978436.35154136,
 '02': 21982547.923177082,
 '03': 40335689.85487529,
 '04': 5855449.5823914325,
 '05': 31109399.77840909,
 '07': 51830849.26118627,
 '08': 59164627.106172845,
 '09': 51911461.8291358,
 '10': 1708770.7183159722,
 '12': 69658346.02646503,
 '13': 435462306.6693751,
 '14': 106206325.75661628,
 '15': 208057154.1914672,
 '16': 51418181.965432115,
 '17': 33035098.503401358,
 '18': 122764375.562449,
 '19': 57630217.4323223,
 '20': 136458364.16493055,
 '22': 96996435.94437502,
 '23': 124895672.60586742,
 '24': 95290423.80999999,
 '25': 214971985.74316293,
 '27': 171994440.03854865,
 '30': 20713341.56521739,
 '31': 615280261.9075963,
 '32': 84140690.47873263,
 '33': 156626244.35428572,
 '34': 470969490.2806122,
 '35': 52616814.08984375,
 '36': 426361217.0024692,
 '39': 463714033.77514803,
 '41': 121239930.98339844,
 '42': 148766929.609375,
 '43': 147236044.99773246,
 '44': 205692844.7654321}

def read_personality():
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
        value = atts[1:6]
        #print value
        personality[id] = value
            
    return personality

def z_score_normalize(dict):

    values = dict.values()
    n = len(values)
    mean = sum(values)/float(n)
    print mean
    
    variance = 0.0 
    for value in values:
        variance += value*value
    variance /= float(n)
    variance = math.sqrt(variance - mean*mean)
    
    for key in dict:
        dict[key] = str((dict[key] - mean) / variance)
        
    print dict
    return dict
        
        

def write_csv(personality):
    output_fp = os.path.join(cur_dir, 'data', 'matrix_data', 'features.csv')
    labels = ['subject_id', 'start_time_var', 'extra', 'agrbl', 'consc', 'neuro','open' ]
    fw = open(output_fp, 'a')
    fw.write(','.join(labels) + '\n')
                
    for id in ids:
        line = [id] 
        line.extend([avg_edit_dist[id], num_patterns[id], start_time_var[id]])
        print line
        id = str(int(id))
        if not id in personality:
            print 'no id in personality data'
 
        for value in personality[id]:
            line.append(value)
         
        fw.write(','.join(line) + '\n')
        
    fw.close()
    
if __name__ == '__main__':
    avg_edit_dist = z_score_normalize(avg_edit_dist)
    num_patterns = z_score_normalize(num_patterns)
    start_time_var = z_score_normalize(start_time_var)
    personality = read_personality()
    write_csv(personality)
    
    