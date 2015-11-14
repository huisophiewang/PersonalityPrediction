from datetime import datetime, date, time, timedelta
from pprint import pprint
import os
import time
import random
import geopy
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3

locator = Nominatim()
#locator = GoogleV3()

cur_dir = os.path.dirname(os.path.realpath(__file__))



def gps(fp, id):
    gps_addr = {}
    
    output_fp = os.path.join(cur_dir, 'data', 'gps_osm', "temp",  'wifigps_addr_' + id + '.csv')
    
    old_dt = r'27MAR2013'
    
    count = 0
    
    fr = open(fp, 'rU') 
    lines = fr.readlines()
    fr.close()

    for line in lines:
        line_success = False
        atts = line.strip('\n').split(",")
        
        #print atts
        
        if not atts[2] or not atts[3]:
            continue
        
        dt = atts[1][:9]
        
                
        dt_obj = datetime.strptime(atts[1][:9], "%d%b%Y")       
        if dt_obj > datetime.strptime('12APR2013', "%d%b%Y"):
            continue
        
        if dt != old_dt:
            time.sleep(random.randint(10, 30))
            
        if count == 1000:
            print 'count=1000, sleeping...'
            time.sleep(300)
            count = 0
            
        while not line_success:
            try:                
                gps = atts[2]+ ',' + atts[3]
                
                
                if gps in gps_addr:
                    addr = gps_addr[gps]                
                else:
                    #time.sleep(5)
                    location = locator.reverse(gps, timeout=20, exactly_one=True)
                    addr = location.address.encode("ascii", "replace")
                    addr = addr.replace(',', ';')
                    gps_addr[gps] = addr
        
                atts.append(addr)
                new_line = ','.join(atts)
                print new_line
                
                fw = open(output_fp, 'a')
                fw.write(new_line + '\n')
                fw.close()
                
                line_success = True
            
                old_dt = dt
                count += 1
                
            except geopy.exc.GeocoderServiceError, e:
                print e
                fw = open(output_fp, 'a')
                fw.write('==========' + '\n')
                fw.close()
                print "server error, sleeping..."
                time.sleep(600)
            
    #gps_addr = sorted(gps_addr.items(), key = lambda item:item[0])
    #pprint(gps_addr)

    print "subject " + id + ' is finished.'
    fw = open(output_fp, 'a')
    fw.write("subject " + id + ' is finished.' + '\n')
    fw.close()
    

    
def gps_all():
    raw_dir = os.path.join(cur_dir, 'data', 'by subjects')
    for file in os.listdir(raw_dir):
        if not file.endswith('.csv'):
            continue
        id = file.split('.')[0][-2:]
        print 'subject id: ' + id
        
        if id in ['10', '12', '13', '14', '15', '16', '17', '18']:
            fp = os.path.join(raw_dir, file)
            gps(fp, id)


if __name__ == "__main__":
    
#     fp = os.path.join(cur_dir, 'data', 'by subjects', 'wifigps_subject05.csv')
#     print fp
#     id = '05'
#     gps(fp, id)

    gps_all()


       
            