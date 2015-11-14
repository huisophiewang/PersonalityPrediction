from datetime import datetime, date, time, timedelta
from pprint import pprint
import os
import matplotlib.pyplot as plt

def gps(fp):
    lats = []
    lons = []
    
    locs = {}
    dates = {}
    with open(fp, 'rU') as fr:
        lines = fr.readlines()
        for line in lines:
            atts = line.strip('\n').split(",")

            if not atts[2] or not atts[3]:
                continue
            
            dt = datetime.strptime(atts[1][:9], "%d%b%Y")
            weekday = dt.strftime("%A")
            if weekday!= 'Monday':
                continue
            
#             dt = atts[1]
#             if dt[:9] not in dates:
#                 dates[dt[:9]] = []
#                 dates[dt[:9]].append(dt[-8:])
#             else:
#                 dates[dt[:9]].append(dt[-8:])
#                 
#             gps = atts[2][:-5] + ',' + atts[3][:-5]
#             if gps not in locs:
#                 locs[gps] = 0
#                 locs[gps] += 1
#             else:
#                 locs[gps] += 1
                
            lat = float(atts[2])
            lats.append(lat)
            
            lon = float(atts[3])
            lons.append(lon)
    
    #pprint(lats)
    print(len(lats))
    
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(lats)

    axarr[1].plot(lons)
    #plt.plot(lats)
    plt.show()
        
if __name__ == "__main__":
    fp = r'C:\Users\Sophie\Smart Phone Project Local\by subjects\wifigps_subject02.csv'
    gps(fp)