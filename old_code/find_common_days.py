from datetime import datetime, date, time, timedelta
from pprint import pprint
import os

off_campus = ['00', '12', '13', '31', '34', '36', '39', '42', '44', '45', '47', '56']

#common_days = ['22APR2013', '12APR2013', '13APR2013', '19APR2013', '07APR2013', '06APR2013', '09APR2013', '08APR2013', '03APR2013', '15APR2013', '01APR2013', '02APR2013', '14APR2013', '04APR2013', '21APR2013', '05APR2013', '27MAR2013', '10APR2013', '11APR2013', '23APR2013']
common_days = ['27MAR2013', '01APR2013', '02APR2013', '03APR2013', '04APR2013', '05APR2013', '06APR2013', '07APR2013', '08APR2013', '09APR2013', '10APR2013', '11APR2013', '12APR2013', '13APR2013', '14APR2013', '15APR2013', '19APR2013', '21APR2013', '22APR2013', '23APR2013']

def remove_missing(fp):
    
    lines = []
     
    by_dates = {}
    with open(fp, 'rU') as fr:
        lines = fr.readlines()
        for line in lines:
            atts = line.strip('\n').split(",")
            
#             wifi_loc = atts[4]
#             if not wifi_loc:
#                 continue
            
            
            dt = atts[1][:9]
            
#             dt_obj = datetime.strptime(dt, "%d%b%Y")
#             weekday = dt_obj.strftime("%A")
#             if weekday == 'Sunday' or weekday == 'Saturday':
#                 continue
            
            if dt not in by_dates:
                by_dates[dt] = []
                by_dates[dt].append(atts)
            else:
                by_dates[dt].append(atts)
    
    #pprint(by_dates)
    #by_dates = sorted(by_dates.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))
    #pprint(by_dates)
    
    dates_complete = set(by_dates.keys())
    print len(dates_complete)
    
    by_dates_complete = {}
    for dt in by_dates:
        if not dt in common_days:
            continue

        seqs = by_dates[dt]
        start_time = seqs[0][1][10:]
        end_time = seqs[-1][1][10:]
        if not start_time.startswith('00') or not end_time.startswith('23'):
            print dt
            print seqs[0]
            print seqs[-1]
            continue
        
        by_dates_complete[dt] = by_dates[dt]
        
    
#     dates_complete = set(by_dates_complete.keys())
#     print len(dates_complete)
    
    return dates_complete
    
    #by_dates_complete = sorted(by_dates_complete.items(), key=lambda item: datetime.strptime(item[0], "%d%b%Y"))    
    #pprint(by_dates_complete)   
    #print len(by_dates_complete)
    
def all_subjects():
    result = set()
    for file in os.listdir(r'data\by_subjects'):
        if not file.endswith('.csv'):
            continue
        id = file.split('.')[0][-2:]
        
        if id in off_campus:
            continue
        
        if int(id)>=45:
            continue
        
        print 'subject id: ' + id

        fp = os.path.join(r'data\by_subjects', file)
        dates_complete = remove_missing(fp)
        
        if id == '01':
            result.update(dates_complete)
        else:
            result.intersection_update(dates_complete)
        print len(result)
        print result
    
if __name__ == '__main__':  
#     fp = r'data\by subjects\wifigps_subject15.csv'
#     remove_missing(fp)
    all_subjects()
    
    #print sorted(common_days)