import os
import operator
from pprint import pprint
import numpy as np

from util import CUR_DIR, OFF_CAMPUS, ID_HOME
from util import write_feature_to_csv
from prep_wifi_loc import get_seqs
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')
MIN_SUPPORT = 10
DURATION_CUT = 60*10
NUM_DAYS = 20
CUT_TO_LEVEL = 10

def replace_home(seqs, id):
    for i, seq in enumerate(seqs):
        for j, loc in enumerate(seq):
            if loc in ID_HOME[id]:
                seqs[i][j] = 'home'

def get_all_locs(seqs):
    for seq in seqs:
        for loc in seq:
            all_locs.add(loc)
            
def gsp(seqs, level, flist, freq_pat):
    
#     print '========'
#     print "level: %d" % level

    if level > CUT_TO_LEVEL:
        return freq_pat
    
    if level == 1:
        fdict = {}
        for seq in seqs:
            #print seq
            for loc in WIFI_ALL_LOCS:
                if loc in seq:
                    if loc in fdict:
                        fdict[loc] += 1
                    else:
                        fdict[loc] = 1 

    else:
        
        clist = []
        n = len(flist)
        for i in range(n):
            for j in range(n):
                if flist[i][1:] == flist[j][:-1]:
                    cad = []
                    cad.extend(flist[i])
                    cad.append(flist[j][-1])
                    clist.append(cad)
        
        # todo: prune before scan all seqs
        fdict = {}
        for seq in seqs:
            for cad in clist:
                if ','.join(cad) in ','.join(seq):
                    cad_str = ','.join(cad)
                    if cad_str in fdict:
                        fdict[cad_str] += 1
                    else:
                        fdict[cad_str] = 1
    fdict = sorted(fdict.items(), key=operator.itemgetter(1), reverse=True)
    #pprint(fdict) 
    
    flist = []              
    for cad_str, freq in fdict:
        if freq >= MIN_SUPPORT:
            freq_pat.append((cad_str, freq))
            if level == 1:
                flist.append([cad_str])
            else:
                flist.append(cad_str.split(','))                
    #pprint(freq_pat)
    
    gsp(seqs, level+1, flist, freq_pat)

def get_freq_pat():
    all_locs = set()
    all_seqs = []
    seqs_by_subject = []
    ids = []

    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue        
        id = file.split('.')[0][-2:]
   
        if id in OFF_CAMPUS:
            continue
        fp = os.path.join(input_dir, file)
        
        ids.append(id)
        print id
        
        seqs = get_wifi_seqs(fp, DURATION_CUT, NUM_DAYS)
#         for seq in seqs:
#             print seq
            
        replace_home(seqs, id)
        seqs_by_subject.append(seqs)
        all_seqs.extend(seqs)
    

    ### run GSP algorithm to get freq pattern
    freq_pat = []
    gsp(all_seqs, 1, [], freq_pat)
    #pprint(freq_pat)
    print len(freq_pat)
    
    
    ### 
    for i, p in enumerate(freq_pat):
        print i, p
     
    ## n x m matrix, n subjects, m frequent patterns
    n = len(ids)
    m = len(freq_pat)
    count = np.zeros((n, m))
     
 
    for i in range(n):
        for seq in seqs_by_subject[i]:
            # print subject i daily sequences
            if i == 1:
                print ','.join(seq)
                
            for j, (pat,f) in enumerate(freq_pat):
                if pat in ','.join(seq):
                    count[i, j] += 1
          
    print count  
    
    print n, m
    print count[1]  
    print count[:, 0:7]

    ## write the first 7 frequent patterns to csv
    for j, (pat,f) in enumerate(freq_pat[:2]):
        id_feature = {}
        feature = count[:, j]
        #print feature
        for i, id in enumerate(ids):
            id_feature[id] = feature[i]
        feature_name = "fp_test_" + pat.replace(',',';')
        write_feature_to_csv(feature_name, id_feature)

if __name__ == '__main__':

        