import os
from util import WIFI_ALL_LOCS

def get_loc_gps(loc):
    dir = os.path.join('old_code', 'data', "by_subjects")
    for fn in os.listdir(dir):
        #print fn
        fp = os.path.join(dir, fn)
        fr = open(fp, 'rU')
        for line in fr.readlines():
            items = line.strip().split(',')
            #print items
            if items[4] == ('in[%s]' % loc) and items[2] and items[3]:
                print line.strip()

        
    
if __name__ == '__main__':
#     for loc in WIFI_ALL_LOCS:
#         print '-------'
    loc = 'occum'
    get_loc_gps(loc)