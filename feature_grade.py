from util import write_feature_to_csv

def get_feature():
    fr = open(r'dataset\education\grades.csv', 'rU')
    cols = fr.readline()
    id_feature = {}
    for line in fr.readlines():
        items = line.split(',')
        id = items[0][1:]
        grade = float(items[3])
        id_feature[id] = grade
    return id_feature


if __name__ == '__main__':
    id_feature = get_feature()
    write_feature_to_csv(id_feature, 'grade', False)
    