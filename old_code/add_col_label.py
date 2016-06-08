import os
from utilities import CUR_DIR

output_dir = "C:\Users\Sophie\Documents\Statistics\project\gps_addr"
input_dir = "C:\Users\Sophie\workspace\Personality\data\gps_osm"

for file in os.listdir(input_dir):
    if not file.endswith('.csv'):
        continue
    
    id = file.split('.')[0][-2:]
    fr = open(os.path.join(input_dir, file), 'rU')
    fw = open(os.path.join(output_dir, file), 'a')
    fw.write(r"id,time,latitude,longitude,wifi_prep,addr" + '\n')
    lines = fr.readlines()
    for line in lines:
        fw.write(line)
    fw.close()