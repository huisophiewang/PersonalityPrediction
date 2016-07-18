import datetime 
import pprint
pp = pprint.PrettyPrinter(width=100)
from prep_wifi_loc import get_in_loc_duration
from feature_class import get_class_schedule

def get_deadlines():
    id_deadlines = {}
    fr = open(r'dataset\education\deadlines.csv', 'rU')
    days = fr.readline().rstrip('\n').split(",")[1:]
    #print days
    for line in fr.readlines():
        items = line.rstrip('\n').split(",")
        id = items[0][1:]
        #print '---------'
        #print id
        deadlines = []
        for i, item in enumerate(items[1:]):
            if int(item) != 0:
                #print i
                deadlines.append(days[i])
        #print len(deadlines)
        id_deadlines[id] = deadlines
    return id_deadlines

def analyze(id, id_deadlines):   
    deadlines = id_deadlines[id]
    pre_deadlines = []
    for deadline in deadlines:
        print deadline
        pre_deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d") - datetime.timedelta(1)
        pre_deadline = pre_deadline.strftime("%Y-%m-%d")
        pre_deadlines.append(pre_deadline)
    in_loc_duration = get_in_loc_duration(id)
    for pair in in_loc_duration:
        dt, seq = pair[0], pair[1]
        weekday = datetime.datetime.strptime(dt, "%Y-%m-%d").strftime("%A")
        if dt in deadlines or dt in pre_deadlines:
            print dt + ' ' + weekday
            pp.pprint(seq)

    
    
if __name__ == '__main__':
    id_deadlines = get_deadlines()
    id = '02'
    schedule = get_class_schedule(id)
    pp.pprint(schedule)
    analyze(id, id_deadlines)
            
    