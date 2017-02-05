import os
from pprint import pprint
from util import CUR_DIR, OFF_CAMPUS, write_feature_to_csv, get_entropy, write_multi_features_to_csv, fill_miss_values
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
    by_day_day, by_day_evening, by_day_night = {}, {}, {}
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
        
        hour = int(time[:2])
        if hour >= 9 and hour < 18:
            if not date in by_day_day:
                by_day_day[date] = 0
            by_day_day[date] += 1
        elif hour >= 18 and hour <= 23:
            if not date in by_day_evening:
                by_day_evening[date] = 0
            by_day_evening[date] += 1
        else:
            if not date in by_day_night:
                by_day_night[date] = 0
            by_day_night[date] += 1   
        

        
    by_date = sorted(by_date.items(), key=lambda item: datetime.strptime(item[0], "%Y-%m-%d"))
    #pprint(by_date)
    #pprint(count_by_timestamp)
#     print total
#     print len(count_by_timestamp)   
#     print float(total)/len(count_by_timestamp)
#     print len(count_by_date)
#     print float(total)/len(count_by_date)
    #pprint(count_by_timestamp)
    #pprint(count_by_date)
    #print len(count_by_date)
    #return float(total)/len(count_by_date)
    #return float(total)/len(count_by_timestamp)
    #print total
    #return total
    #pprint(by_date)    
    #pprint(by_day_day)
    
    #print len(count_by_date)
    #return len(by_date)
    
    daily_day = 0.0
    for dt in by_day_day:
        daily_day += by_day_day[dt]
    daily_day /= len(by_day_day)
      
      
    daily_evening = 0.0
    for dt in by_day_evening:
        daily_evening += by_day_evening[dt]
    daily_evening /= len(by_day_evening)
  
       
    daily_night = 0.0
    for dt in by_day_night:
        daily_night += by_day_night[dt]
    daily_night /= len(by_day_night)
  
    #return (daily_day, daily_evening, daily_night)

#     daily_day, daily_evening, daily_night = 0.0, 0.0, 0.0
#     daily_day_unique, daily_evening_unique, daily_night_unique = 0.0, 0.0, 0.0
#     day_unique, evening_unique, night_unique = set(), set(), set()
#     for pair in by_date:
#         for entry in pair[1]:
#             hour = int(entry[0][:2])
#             if hour >= 9 and hour < 18:
#                 daily_day += 1
#                 day_unique.add(entry[1])
#             elif hour >= 18 and hour <= 23:
#                 daily_evening += 1
#                 evening_unique.add(entry[1])
#             else:
#                 daily_night += 1
#                 night_unique.add(entry[1])
#                 
#     daily_day /= len(by_date)
#     daily_evening /= len(by_date)
#     daily_night /= len(by_date)
#     
#     #return (daily_day, daily_evening, daily_night)
#     
#     daily_day_unique = len(day_unique) / float(len(by_date))
#     daily_evening_unique = len(evening_unique) / float(len(by_date))
#     daily_night_unique = len(night_unique) / float(len(by_date))
#     
#     return (daily_day_unique, daily_evening_unique, daily_night_unique)
        
    

    
#     # remove class time
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
#     #pprint(by_date_no_class)               
#     
#     daily_day, daily_evening, daily_night = 0.0, 0.0, 0.0
#     for pair in by_date_no_class:
#         for entry in pair[1]:
#             hour = int(entry[0][:2])
#             if hour >= 9 and hour < 18:
#                 daily_day += 1
#             elif hour >= 18 and hour <= 23:
#                 daily_evening += 1
#             else:
#                 daily_night += 1
#                 
#     daily_day /= len(by_date_no_class)
#     daily_evening /= len(by_date_no_class)
#     daily_night /= len(by_date_no_class)
#     
#     return (daily_day, daily_evening, daily_night)



    total2 = float(0)
    for pair in by_date[:30]:
               
        for entry in pair[1]:
#             total2 += 1
#             mac = entry[1]
#             if not mac in by_mac:
#                 by_mac[mac] = 0
#             by_mac[mac] += 1
     
     
    #return total
    #entropy = get_entropy(by_mac)
    #return entropy
    #pprint(by_mac)
 
            #print entry
            hour = int(entry[0][:2])
            mac = entry[1]
 
            if hour >= 9 and hour < 18:
                if not mac in by_mac_day:
                    by_mac_day[mac] = 0
                by_mac_day[mac] += 1
            elif hour >= 18 and hour <= 23:
                if not mac in by_mac_evening:
                    by_mac_evening[mac] = 0
                by_mac_evening[mac] += 1
            else:
                if not mac in by_mac_night:
                    by_mac_night[mac] = 0
                by_mac_night[mac] += 1           
             
     
    nearby_day_entropy = get_entropy(by_mac_day)
    nearby_evening_entropy = get_entropy(by_mac_evening)
    nearby_night_entropy = get_entropy(by_mac_night)
    print (nearby_day_entropy, nearby_evening_entropy, nearby_night_entropy)
    return (nearby_day_entropy, nearby_evening_entropy, nearby_night_entropy)


    
#     by_mac = {k: by_mac[k]/total2 for k in by_mac}
#     mac_sorted = sorted(by_mac.items(), key=lambda x: x[1], reverse=True)
#     pprint(mac_sorted[:10])


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
    
#     threshold = 0.05
#     num_friends = 0
#     for pair in mac_sorted:
#         if pair[1] > threshold:
#             num_friends += 1
#     print num_friends
#     return num_friends
            

    
    



    
def get_feature():
    id_feature = {}
    for file in os.listdir(dir):
        if not file.endswith('datetime.csv'):
            continue       
        id = file[4:6]
        
        # '49' is an outlier
        if id in OFF_CAMPUS:
            continue
        
#         if id != '02':
#             continue
        
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
    #write_feature_to_csv(id_feature, 'nearby_daily_oncampus')  
    #write_feature_to_csv(id_feature, 'nearby_timestamp')
    #write_feature_to_csv(id_feature, 'nearby_timestamp_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_total')
    #write_feature_to_csv(id_feature, 'nearby_total_oncampus')
    #write_feature_to_csv(id_feature, 'num_days_bluetooth')
    #write_feature_to_csv(id_feature, 'num_days_bluetooth_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_entropy_evening')
    #write_feature_to_csv(id_feature, 'nearby_friends_evening')
    #write_feature_to_csv(id_feature, 'nearby_entropy')
    #write_feature_to_csv(id_feature, 'nearby_total_30days_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_entropy_30days_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_total_30days_oncampus_noclass')
    #write_feature_to_csv(id_feature, 'nearby_entropy_30days_oncampus_noclass')
    #write_feature_to_csv(id_feature, 'nearby_num_unique_30days_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_timestamp_30days_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_num_friends_30days_oncampus')
    #write_feature_to_csv(id_feature, 'nearby_oncampus_daily_day') 

    fill_miss_values(id_feature, 3, ['49'])
    #write_multi_features_to_csv(id_feature, ['daily_day_oncampus', 'daily_evening_oncampus', 'daily_night_oncampus'])
    #write_multi_features_to_csv(id_feature, ['daily_day_oncampus_noclass', 'daily_evening_oncampus_noclass', 'daily_night_oncampus_noclass'])
    #write_multi_features_to_csv(id_feature, ['daily_day_unique_oncampus', 'daily_evening_unique_oncampus', 'daily_night_unique_oncampus'])
    #write_multi_features_to_csv(id_feature, ['day_entropy_oncampus', 'evening_entropy_oncampus', 'night_entropy_oncampus'])
    write_multi_features_to_csv(id_feature, ['day_entropy_oncampus_30days', 'evening_entropy_oncampus_30days', 'night_entropy_oncampus_30days'])



    