import os
from util import TRAITS, get_trait_scores

def read_feature(fp):
    fr = open(fp, 'rU')
    fr.readline()
    id_feature = {}
    for line in fr.readlines():
        items = line.split(',')
        id = items[0]
        features = items[1:-5]
        id_feature[id] = features
    return id_feature


        
def combine(feature_names):
    output_fp = r'result\feature\all_features.csv'
    fw = open(output_fp, 'a')
    labels = ['uid']
    for feature_name in feature_names:
        if '-' in feature_name:
            labels.extend(feature_name.split('-'))
        else:
            labels.append(feature_name)
    labels.extend(TRAITS)
    #labels.extend(['depress', 'pcs', 'mcs'])
    fw.write(','.join(labels) + '\n')  
    
    id_y = get_trait_scores()  
    #id_depress = get_other_scores(r'dataset\survey\PHQ-9Pre.csv')  
    #id_health = get_other_scores(r'dataset\survey\vr_12Pre.csv')
    
    ids = sorted(id_y.keys())
    all_features = {id:[] for id in ids}
    for feature_name in feature_names:
        fp = r'result\feature\%s.csv' % feature_name
        id_feature = read_feature(fp)
        for id in all_features:
            if id in id_feature:
                all_features[id].extend(id_feature[id])
            else:
                if '-' in feature_name:
                    num = feature_name.count('-') + 1
                    all_features[id].extend(['NA'] * num)
                else:
                    all_features[id].append('NA')
    
    for id in ids:
        line = [id]
        line.extend(all_features[id])
        
        if id in id_y:
            line.extend(id_y[id])
        else:
            line.extend(['NA'] * 5)
            
#         if id in id_depress:
#             line.extend(id_depress[id])
#         else:
#             line.extend(['NA'])
#             
#         if id in id_health:
#             line.extend(id_health[id])
#         else:
#             line.extend(['NA'] * 2)
        
        fw.write(','.join(line) + '\n') 
    fw.close()
        
def combine_freq_patterns(support, trait='extra'):
    output_fp = os.path.join('result', 'feature', 'all_freq_pat_%d.csv' % support)
    #input_dir = r'result\feature\freq_pat_select\support%s\%s' % (support, trait)
    input_dir = os.path.join('result', 'feature', 'freq_pat', 'support%d' % support)
    labels = ['uid']
    id_y = get_trait_scores() 
    ids = sorted(id_y.keys())
    id_all_features = {id:[] for id in ids}
    for filename in os.listdir(input_dir):
        feature = filename[:-4]
        print feature
        labels.append(feature)
        #fp = r'result\feature\freq_pat\support%d\%s.csv' % (support, feature)
        fp = os.path.join(input_dir, filename)
        id_feature = read_feature(fp)
        for id in id_all_features:
            if id in id_feature:
                id_all_features[id].extend(id_feature[id])
        #print id_all_features
    fw = open(output_fp, 'a')
    labels.append(trait)
    fw.write(','.join(labels) + '\n')  
    trait_idx = TRAITS.index(trait)
    for id in ids:
        line = [id]
        line.extend(id_all_features[id])
        line.append(id_y[id][trait_idx])
        fw.write(','.join(line) + '\n') 
    fw.close()
    
        
        

        
        
if __name__ == '__main__':
    fnames = ['len_var', 'start_time_var', 'end_time_var']
    fnames.extend(['early-late-absent', 'late_time_var'])
    fnames.append('days-views-contributions-questions-notes-answers')
    #fnames.append('breakfast-lunch-supper-snack')
    #combine(fnames)
    
    combine_freq_patterns(30)
 
    






