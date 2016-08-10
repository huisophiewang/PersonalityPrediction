import os
import json
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(width=100)
from util import write_feature_to_csv

questions = ["Dimensions protestors",     #2013-04-24-22:41:36
            "Administration's response",  #2013-04-26-02:50:26
            "Dartmouth now",              #2013-04-27-10:47:19
            "Dimensions",
            "Cancelled Classes"]


ids = ['%02d' % i for i in range(60)]
count = {id:0 for id in ids}
#q1 = {id:'NA' for id in ids}

id_value = {}
for question in questions[2:-2]:
    print '========================================='
    print question
    dir = r'dataset\EMA\response\%s' % question
    for file in os.listdir(dir):
        id = file.split('.')[0][-2:]
        fr = open(os.path.join(dir, file))
        data = json.load(fr)

        if not data:
            continue
        print '-------------'
        print id
        count[id] += 1
        pairs = []
        for entry in data:
            time = datetime.fromtimestamp(entry['resp_time']).strftime('%Y-%m-%d-%H:%M:%S')
            print time
            pp.pprint(entry)
            pos = 0
            neg = 0
            for key, value in entry.items():
                if key != 'resp_time' and len(value) == 1:
                    if key in ['empathic', 'appreciative', 'proud']:
                        pos += int(value) - 1
                    if key in ['disappointed', 'angry', 'saddened', 'frustrated', 'apathetic']:
                        # scale down
                        neg += - (int(value)-1)*0.6  
            sum = pos + neg
            print sum
            pairs.append((time, sum))
        pairs = sorted(pairs, key=lambda item: datetime.strptime(item[0], "%Y-%m-%d-%H:%M:%S"))
        value = 0.0
        for pair in pairs:
            if pair[1] != 0.0:
                value = pair[1]
                break
        print value 
        id_value[id] = value
        
            
                               
#pp.pprint(count)
#write_feature_to_csv(count, 'reply_count', False)
#write_feature_to_csv(id_value, 'q3', False)