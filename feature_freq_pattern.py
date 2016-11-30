import os
import operator
from pprint import pprint
import numpy as np

from util import CUR_DIR, OFF_CAMPUS, ID_HOME
from util import write_feature_to_csv
from prep_wifi_loc import get_seqs
wifi_dir = os.path.join(CUR_DIR, 'dataset', 'sensing', 'wifi_location')




##########################################################################
# frequent itemset/pattern mining 
# algorithms: Apriori
#             FP-growth
# reference reading: Data Mining Concepts and Techniques 3rd ed, Chapter 6
# note: it's based on sets, item order doesn't matter
#       in Aproiori, items are sorted to avoid duplicates

##########################################################################
# frequent sequential pattern mining
# algorithms: GSP
#             PrefixSpan
# reference paper: GSP: http://rakesh.agrawal-family.com/papers/edbt96seq.pdf
#                  PrefixSpan https://static.aminer.org/pdf/PDF/000/300/860/prefixspan_mining_sequential_patterns_by_prefix_projected_growth.pdf
# note: definition of subsequence, e.g. a,c,d is a subsequence of a,b,c,d
#       GSP is based on Aproiori



def replace_home(seqs, id):
    for i, seq in enumerate(seqs):
        for j, loc in enumerate(seq):
            if loc in ID_HOME[id]:
                seqs[i][j] = 'home'

def get_all_locs(seqs):
    for seq in seqs:
        for loc in seq:
            all_locs.add(loc)
            


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
        
def gsp(seqs, level, flist, min_support):
    if level == 1:
        fdict = {}
        for seq in seqs:
            for loc in seq:
                if not loc in fdict:
                    fdict[loc] = 1
                else:
                    fdict[loc] += 1 
    else:
        # generate all candidates of length level from length (level-1)
        clist = []
        n = len(flist)
        for i in range(n):
            for j in range(n):
                if flist[i][1:] == flist[j][:-1]:
                    clist.append(flist[i] + flist[j][-1:])           
        # count the frequency of those candidates
        fdict = {}
        for seq in seqs:
            for cad in clist:
                # here we use contiguous subsequence
                # since it makes more sense for daily location sequence
                cad_str = ','.join(cad)
                if cad_str in ','.join(seq):
                    if not cad_str in fdict:
                        fdict[cad_str] = 1
                    else:
                        fdict[cad_str] += 1                
    # sort by frequency                   
    fdict = sorted(fdict.items(), key=lambda x: x[1], reverse=True)
    #pprint(fdict) 
    
    # select those candidates with frequency larger than min_support
    flist = []              
    for cad_str, freq in fdict:
        if freq >= min_support:
            flist.append(cad_str.split(','))     
    return flist
    
def gsp_test():
    s1 = ['a', 'b', 'd']
    s2 = ['a', 'b', 'c', 'd']
    s3 = ['b', 'c', 'a', 'f']
    s4 = ['a', 'c', 'e', 'c', 'b']
    s5 = ['a']
    seqs = [s1, s2, s3, s4, s5]
    
    level = 1
    last_freq = []
    all_freq_pat = []
    max_pattern_len = 3
    while level <= max_pattern_len:
        freq = gsp(seqs, level, last_freq, min_support=1)
        all_freq_pat.extend(freq)
        last_freq = freq
        level += 1
    pprint(all_freq_pat)

def get_freq_pattern():
    ### get seqs 
    ids = []
    all_seqs = []  # all seqs of all subjects
    seqs_by_subject = [] # n subjects, length n 
    for file in os.listdir(wifi_dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        id = file.split('.')[0][-2:]
        ids.append(id)
        seqs = get_seqs(id)
        all_seqs.extend(seqs)
        seqs_by_subject.append(seqs)
    
    ### get freq_patterns from all_seqs
    freq_patterns = []
    level = 1
    max_pattern_len = 5
    prev_level_freq = []
    while level <= max_pattern_len:
        freq = gsp(all_seqs, level, prev_level_freq, min_support=20)
        freq_patterns.extend(freq)
        prev_level_freq = freq
        level += 1
    pprint(freq_patterns)
    print len(freq_patterns)
    
    ### compute frequency of freq_patterns for each subject
    n = len(ids) # n subjects
    m = len(freq_patterns) # m frequent patterns
    count = np.zeros((n, m)) # n x m matrix
    for i in range(n):
        for seq in seqs_by_subject[i]:
            for j, pat in enumerate(freq_patterns):
                if ','.join(pat) in ','.join(seq):
                    count[i, j] += 1
    #print count[:,100]

    ### use frequency as feature, write to csv
    for j, pat in enumerate(freq_patterns):
        id_feature = {}
        feature = count[:, j]
        #print feature
        for i, id in enumerate(ids):
            id_feature[id] = feature[i]
        feature_name = "fp_" + ';'.join(pat)
        write_feature_to_csv(id_feature, feature_name, 'freq_pat', False)
    
if __name__ == '__main__':
    
    #seqs = get_seqs('01')
    #pprint(seqs)

    #gsp_test()
    get_freq_pattern()


    

    

        