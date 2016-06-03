from datetime import datetime, date, time, timedelta
from pprint import pprint
import os

DATA_DIR = r'data\by subjects'

off_campus = ['00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '56']

subj_home = {}

def gps(fp, id):
    
    cut = -4
    
    gps_freq = {}
    dates = {}
    loc_gps = {}
    with open(fp, 'rU') as fr:
        lines = fr.readlines()
        for i, line in enumerate(lines):
            atts = line.strip('\n').split(",")
            
            if not atts[2] or not atts[3]:
                continue
            
            #dt = datetime.strptime(atts[1][:9], "%d%b%Y")
#             if atts[1][:9] != r'27MAR2013':
#                 continue
            
                
            if atts[4]:
                if not atts[4].startswith('in'):
                    continue
                loc = atts[4][3:-1]
                if loc not in loc_gps:
                    loc_gps[loc] = set()
                    loc_gps[loc].add(atts[2][:cut] + ',' + atts[3][:cut])
                else:
                    loc_gps[loc].add(atts[2][:cut] + ',' + atts[3][:cut])
            

            gps = atts[2][:cut] + ',' + atts[3][:cut]
            if gps not in gps_freq:
                gps_freq[gps] = 0
                gps_freq[gps] += 1
            else:
                gps_freq[gps] += 1
                


    #pprint(loc_gps)
    
    #pprint(gps_freq)
    
    gps_loc = {}
    gps_freq_sorted = sorted(gps_freq.items(), key=lambda item: item[1], reverse=True)
    for item in gps_freq_sorted:
        gps = item[0]
        freq = item[1]
        if freq < 2:
            continue
        gps_loc[gps] = ' '
        for loc in loc_gps:
            if gps in loc_gps[loc]:
                gps_loc[gps] = loc
                break
    

    for item in gps_freq_sorted[:10]:
        gps = item[0]
        freq = item[1]
        print gps + ' ' +  gps_loc[gps] + ' ' + str(freq)
    
    most_freq = gps_freq_sorted[0]
    gps = most_freq[0]
    freq = most_freq[1]
    print gps_loc[gps]
    if gps_loc[gps] != ' ':
        subj_home[id] = [gps_loc[gps]]
        print 'on campus'
    
def gps_all():
    for file in os.listdir(DATA_DIR):
        if not file.endswith('.csv'):
            continue
        id = file.split('.')[0][-2:]
        print
        print 'subject id: ' + id
        
        fp = os.path.join(DATA_DIR, file)
        gps(fp, id)

if __name__ == "__main__":
#     fp = r'data\by subjects\wifigps_subject02.csv'
#     gps(fp)


    

    gps_all()
    
    pprint(subj_home)
    print len(subj_home)


       
            