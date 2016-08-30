from util import write_multi_features_to_csv
import pprint
pp = pprint.PrettyPrinter(width=100)

#########################################
# missing: none
# outliers: 00, 13

def get_features():
    id_feature = {}
    fr = open(r'dataset\education\piazza.csv', 'rU')
    cols = fr.readline()
    print cols
    lines = fr.readlines()
    for line in lines:
        items = line.rstrip().split(',') 
        id = items[0][1:]
        if id in ['00', '13']:
            continue
        id_feature[id] = [int(x) for x in items[1:]]
    pp.pprint(id_feature)
    return id_feature
        
        
if __name__ == '__main__':
    id_features = get_features()
    write_multi_features_to_csv(id_features, ['days', 'views', 'contributions', 'questions', 'notes', 'answers'])