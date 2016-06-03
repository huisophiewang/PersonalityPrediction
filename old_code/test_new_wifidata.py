import os
from utilities import CUR_DIR, get_wifi_seqs

id_feature = {}
addr_dir = os.path.join(CUR_DIR, 'data', 'by_subjects')
for file in os.listdir(addr_dir):
    if not file.endswith('.csv'):
        continue
    
    id = file.split('.')[0][-2:]
    if int(id) >= 45:
        continue     
#         if id in WIFI_OFF_CAMPUS:
#             continue
    fp = os.path.join(addr_dir, file)
    print '----------'
    print 'id: ' + id
    
    #seqs = get_wifi_seqs(fp, 60*10, 20)
    seqs = get_wifi_seqs(fp, 60*5, 30)