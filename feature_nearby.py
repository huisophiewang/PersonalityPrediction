import os
from pprint import pprint
from util import CUR_DIR, write_feature_to_csv, get_entropy, OFF_CAMPUS
dir = os.path.join(CUR_DIR, "dataset", "sensing", "bluetooth")
from datetime import datetime
from feature_class import get_class_schedule

def get_nearby(fp, id):
    
    fr = open(fp, 'rU') 
    count_by_date = {}
    count_by_timestamp = {}
    by_date = {}
    by_mac = {}
    by_mac_day, by_mac_evening, by_mac_night = {}, {}, {}
    total = 0
    lines = fr.readlines()
    for line in lines:
        items = line.rstrip(',\n').split(",")
        total += 1
        mac = items[1]

        
        timestamp = items[0]
        if not timestamp in count_by_timestamp:
            count_by_timestamp[timestamp] = 0
        count_by_timestamp[timestamp] += 1
        date = timestamp[:10]
        time = timestamp[11:]
        
        if not date in count_by_date:
            count_by_date[date] = 0
            by_date[date] = []
        count_by_date[date] += 1
        by_date[date].append([time, mac])
        

        
    by_date = sorted(by_date.items(), key=lambda item: datetime.strptime(item[0], "%Y-%m-%d"))
    #pprint(by_date)
    
    
    # remove class time
#     by_date_no_class = []
#     week_schedule = get_class_schedule(id)
#     for idx, pair in enumerate(by_date):
#         by_date_no_class.append((pair[0], []))
#         date_obj = datetime.strptime(pair[0], "%Y-%m-%d")
#         weekday = date_obj.strftime("%A")   
#         if weekday in week_schedule:
#             day_schedule = week_schedule[weekday]
#             for entry in pair[1]:
#                 time = entry[0][:5]
#                 is_in_class = False
#                 for time_schedule in day_schedule:
#                     start_time = time_schedule[1]
#                     end_time = time_schedule[2]
#                     if datetime.strptime(time, "%H:%M") > datetime.strptime(start_time, "%H:%M") and \
#                         datetime.strptime(time, "%H:%M") < datetime.strptime(end_time, "%H:%M"):
#                         is_in_class = True
#                         break                
#                 if not is_in_class:
#                     by_date_no_class[idx][1].append(entry)    
#         else:
#             by_date_no_class[idx][1].extend(pair[1])
                
    #pprint(by_date_no_class)               
                
                    
            
    total2 = float(0)
    for pair in by_date[:30]:
             
        for entry in pair[1]:
            total2 += 1
            mac = entry[1]
            if not mac in by_mac:
                by_mac[mac] = 0
            by_mac[mac] += 1
    
    
    #return total
    #entropy = get_entropy(by_mac)
    #return entropy
    #pprint(by_mac)

        
#         hour = int(time[:2])
#         if hour >= 9 and hour < 18:
#             if not mac in by_mac_day:
#                 by_mac_day[mac] = 0
#             by_mac_day[mac] += 1
#         elif hour >= 18 and hour <= 23:
#             if not mac in by_mac_evening:
#                 by_mac_evening[mac] = 0
#             by_mac_evening[mac] += 1
#         else:
#             if not mac in by_mac_night:
#                 by_mac_night[mac] = 0
#             by_mac_night[mac] += 1           
            
    
        
    #print len(count_by_timestamp)   
    #pprint(count_by_date)
    #print len(count_by_date)
    #return float(total)/len(count_by_date)
    #return float(total)/len(count_by_timestamp)
    #print total
    #return total
    #pprint(by_date)

    
    by_mac = {k: by_mac[k]/total2 for k in by_mac}
    mac_sorted = sorted(by_mac.items(), key=lambda x: x[1], reverse=True)
    pprint(mac_sorted[:10])


#     acc_prob = 0.0
#     threshold = 0.2
#     friends = 0
#     for pair in mac_sorted:
#         acc_prob += pair[1]
#         friends += 1
#         if acc_prob >= threshold:
#             break
#     print friends
    #return friends
    #entropy = get_entropy(by_mac)
    #return entropy
    
    threshold = 0.05
    num_friends = 0
    for pair in mac_sorted:
        if pair[1] > threshold:
            num_friends += 1
    print num_friends
    return num_friends
            

    
    



    
def get_feature():
    id_feature = {}
    for file in os.listdir(dir):
        if not file.endswith('datetime.csv'):
            continue       
        id = file[4:6]
        
        if id in OFF_CAMPUS + ['49']:
            continue

        
        print '------'
        print "id: " + id
        

        
        fp = os.path.join(dir, file)
        result = get_nearby(fp, id)
        id_feature[id] = result

    #pprint(id_feature)
    return id_feature
        

if __name__ == '__main__':  
    id_feature = get_feature()
    #write_feature_to_csv(id_feature, 'nearby_daily')  
    #write_feature_to_csv(id_feature, 'nearby_timestamp')
    #write_feature_to_csv(id_feature, 'nearby_total')
    #write_feature_to_csv(id_feature, 'num_days_bluetooth')
    #write_feature_to_csv(id_feature, 'nearby_entropy_evening')
    #write_feature_to_csv(id_feature, 'nearby_friends_evening')
    #write_feature_to_csv(id_feature, 'nearby_entropy')
    #write_feature_to_csv(id_feature, 'nearby_total_30days_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_entropy_30days_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_total_30days_oncampus_noclass')
    #write_feature_to_csv(id_feature, 'nearby_entropy_30days_oncampus_noclass')
    #write_feature_to_csv(id_feature, 'nearby_num_unique_30days_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_timestamp_30days_oncampus')
    write_feature_to_csv(id_feature, 'nearby_num_friends_30days_oncampus')

    



    