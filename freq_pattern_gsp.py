import os
import operator
from pprint import pprint
from edit_dist import get_seqs
from utilities import CUR_DIR, WIFI_OFF_CAMPUS, WIFI_ID_HOME, WIFI_ALL_LOCS

MIN_SUPPORT = 3
CUT_TO_LEVEL = 4

def replace_home(seqs, id):
    for i, seq in enumerate(seqs):
        for j, loc in enumerate(seq):
            if loc in WIFI_ID_HOME[id]:
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
            print seq
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
                #print flist[i], flist[j]
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



if __name__ == '__main__':
    all_locs = set()
    input_dir = os.path.join(CUR_DIR, 'data', 'by_subjects')
    for file in os.listdir(input_dir):
        if not file.endswith('.csv'):
            continue
        
        id = file.split('.')[0][-2:]
        if int(id) >= 45:
            continue     
        if id in WIFI_OFF_CAMPUS:
            continue
        fp = os.path.join(input_dir, file)
        
        if id != '02':
            continue
        
        seqs = get_seqs(fp)
        replace_home(seqs, id)
        
        freq_pat = []
        gsp(seqs, 1, [], freq_pat)
        pprint(freq_pat)
        
