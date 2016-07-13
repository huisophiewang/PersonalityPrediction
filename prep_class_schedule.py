from datetime import datetime
from prep_wifi_loc import get_in_loc_duration

week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_late_time(id, schedule):
    excluded = []
    for day in week:
        if not day in schedule:
            excluded.append(day)
           
    ## keep weekdays
    in_loc_duration_weekdays = []
    in_loc_duration = get_in_loc_duration(id)
    for pair in in_loc_duration:   
        seq = pair[1]
        date_obj = datetime.strptime(pair[0], "%Y-%m-%d")
        weekday = date_obj.strftime("%A")   
        if weekday in excluded:
            continue
        in_loc_duration_weekdays.append((pair[0], pair[1]))
    
    ## use the first 20 weekdays
    result = []
    for pair in in_loc_duration_weekdays[:20]:
        seq = pair[1]
        date_obj = datetime.strptime(pair[0], "%Y-%m-%d")
        weekday = date_obj.strftime("%A")
        print '-----------'
        print weekday  
        daily_result = []
        for idx, schedule_info in enumerate(schedule[weekday]):
            #print schedule_info
            schedule_loc = schedule_info[0]
            for actual_info in seq:
                actual_loc = actual_info[0][3:-1]
                if actual_loc == schedule_loc:
                    schedule_time = datetime.strptime(schedule_info[1], "%H:%M")
                    actual_time = datetime.strptime(actual_info[1][:-3], "%H:%M")
                    if schedule_time > actual_time:
                        diff = (schedule_time - actual_time).seconds / 60.0
                        daily_result.append(-diff)
                    else:
                        diff = (actual_time - schedule_time).seconds / 60.0
                        daily_result.append(diff)
                    break
            if len(daily_result) != idx+1:
                daily_result.append('NA')  
        print daily_result   
        result.extend(daily_result)
        #print
        #pp.pprint(seq)
    return result


            
        

    
    
    
    
    