import time
from wifi import get_in_loc_duration
from util import id_home, start_time_cut
import pprint
pp = pprint.PrettyPrinter(width=200)

def get_start_var(in_loc_duration, id):
    start_times = []
    for pair in in_loc_duration:
        seq = pair[1]
        pp.pprint(seq)
        for line in seq:
            loc = line[0][3:-1]
            start_time = time.strptime(line[1], "%H:%M:%S")
            if start_time > start_time_cut and not loc in id_home[id]:
                start_times.append(line[1])
                print line[1]
                break

    return start_times

fp = r'C:\Users\Sophie\workspace\Personality\dataset\sensing\wifi_location\wifi_location_u01.csv'
in_loc_duration = get_in_loc_duration(fp, duration_cut=60*5, sample_days=20, weekday_only=True)
get_start_var(in_loc_duration, '01')