import os
import pprint
pp = pprint.PrettyPrinter(width=200)

def from_gps(fp, id):
    
    cut = -4
    
    gps_freq = {}
    dates = {}
    loc_gps = {}
    fr = open(fp, 'rU')
    lines = fr.readlines()
    for i, line in enumerate(lines):
        items = line.strip('\n').split(",")

        gps = items[4][:cut] + ',' + items[5][:cut]
        if gps not in gps_freq:
            gps_freq[gps] = 0
        gps_freq[gps] += 1

    
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
    
#     most_freq = gps_freq_sorted[0]
#     gps = most_freq[0]
#     freq = most_freq[1]
#     print gps_loc[gps]
#     if gps_loc[gps] != ' ':
#         subj_home[id] = [gps_loc[gps]]
#         print 'on campus'

def from_gps_all():
    dir = r'C:\Users\Sophie\workspace\Personality\dataset\sensing\gps'
    for file in os.listdir(dir):
        if not file.endswith('.csv') or file.endswith('datetime.csv'):
            continue
        id = file.split('.')[0][-2:]
        print '----------'
        print 'id: ' + id
        
        fp = os.path.join(dir, file)
        from_gps(fp, id)
        
def from_wifi(fp, id):
    loc_dates = {}
    fr = open(fp, 'rU')
    for line in fr.readlines():
        line = line.rstrip(',\n')
        items = line.split(",")
        # 4 am?
        if items[0][-8:-6] == '04':
#             if id == '23':
#                 print line
            if items[1].startswith("near"):
                continue
            loc = items[1][3:-1]
            if not loc in loc_dates:
                loc_dates[loc] = set()
            loc_dates[loc].add(items[0][:10])
    
    #loc_freq_sorted = sorted(loc_freq.items(), key=lambda item: item[1], reverse=True)
    for loc in loc_dates:
        print "%s: %d" % (loc, len(loc_dates[loc]))

            
    
def from_wifi_all():
    dir = r'C:\Users\Sophie\workspace\Personality\dataset\sensing\wifi_location'
    for file in os.listdir(dir):
        if not file.endswith('datetime.csv'):
            continue
        id = file.split('.')[0][-11:-9]
        print '----------'
        print 'u%s' % id
        
        fp = os.path.join(dir, file)
        from_wifi(fp, id)
    
if __name__ == "__main__":
    #from_gps_all()
    from_wifi_all()
