import os
from pprint import pprint
from edit_dist import get_seqs
from utilities import CUR_DIR, WIFI_OFF_CAMPUS, WIFI_ID_HOME, WIFI_ALL_LOCS

MIN_SUPPORT = 3

def replace_home(seqs, id):
    for i, seq in enumerate(seqs):
        for j, loc in enumerate(seq):
            if loc in WIFI_ID_HOME[id]:
                seqs[i][j] = 'home'

def get_all_locs(seqs):
    for seq in seqs:
        for loc in seq:
            all_locs.add(loc)
            
def test(seqs):
    fdict = {}
    for seq in seqs:
        print seq
        for loc in WIFI_ALL_LOCS:
            if loc in seq:
                if loc in fdict:
                    fdict[loc] += 1
                else:
                    fdict[loc] = 1 
    pprint(fdict)
    
    flist = []         
    for loc in fdict:
        if fdict[loc] >= MIN_SUPPORT:
            flist.append([loc])
    flist.sort()
    print flist
    
    clist = []
    n = len(flist)
    for i in range(n):
        for j in range(n):
            print flist[i], flist[j]
            if flist[i][1:] == flist[j][:-1]:
                cad = []
                cad.extend(flist[i])
                cad.append(flist[j][-1])
                clist.append(cad)
    pprint(clist)  
    
    # todo: prune
    
    f2dict = {}
    for seq in seqs:
        for cad in clist:
            if ','.join(cad) in ','.join(seq):
                cad_str = ','.join(cad)
                if cad_str in f2dict:
                    f2dict[cad_str] += 1
                else:
                    f2dict[cad_str] = 1
    
    f2list = []               
    for cad_str in f2dict:
        if f2dict[cad_str] >= MIN_SUPPORT:
            f2list.append(cad_str.split(','))
    f2list.sort()
    pprint(f2list)
    

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
        test(seqs)
        
