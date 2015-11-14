import csv
import time
import os
from pprint import pprint

DATA_PATH = r"C:\Users\Sophie\Smart Phone Project\raw data slightly revised\wifigpsmerge.csv"
output_path = r"C:\Users\Sophie\Smart Phone Project\raw data slightly revised"



# for i in range(43):
#     output_fp = os.path.join(output_path, 'wifigps_subject' + '%02d' % i + '.csv')
#     print output_fp
#     with open(output_fp, 'wb') as fw:
#         writer = csv.writer(fw, delimiter=',')
        

with open(DATA_PATH, 'rU') as fr:
    reader = csv.reader(fr)
    labels = reader.next()
    print labels
    for row in reader:
        #print row
        id = int(row[0])
 
        output_fp = os.path.join(output_path, 'wifigps_subject' + '%02d' % id + '.csv')
        with open(output_fp, 'a') as fw:
            fw.write(','.join(row) + '\n')
            fw.close()