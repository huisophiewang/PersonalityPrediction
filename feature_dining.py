import os
import pprint
pp = pprint.PrettyPrinter(width=100)
from util import write_feature_to_csv, write_multi_features_to_csv
from util import get_entropy, get_time_var

dir = r'dataset\dinning'

def loc_entropy(id):
    fp = os.path.join(dir, r'u%s.txt' % id)
    fr = open(fp, 'rU')
    locs = {}
    for line in fr.readlines():
        items = line.rstrip('\n').split(",")
        loc = items[1]
        if not loc in locs:
            locs[loc] = 0
        locs[loc] += 1
    #pp.pprint(locs)
    print sum(locs.values())
    entropy = get_entropy(locs)
    print entropy
    return entropy

def meal_rate(id):
    fp = os.path.join(dir, r'u%s.txt' % id)
    fr = open(fp, 'rU')
    meals = {}
    for line in fr.readlines():
        items = line.rstrip('\n').split(",")
        meal = items[2]
        if not meal in meals:
            meals[meal] = 0
        meals[meal] += 1
    pp.pprint(meals)
    
    rates = []
    total = sum(meals.values())
    for meal in ['Breakfast', 'Lunch', 'Supper', 'Snack']:
        if meal in meals:
            rate = meals[meal]/float(total)
        else:
            rate = 0.0
        rates.append(rate)
    return rates

def time_var(id):
    fp = os.path.join(dir, r'u%s.txt' % id)
    fr = open(fp, 'rU')
    to_idx = {'Breakfast':0, 'Lunch':1, 'Supper':2, 'Snack':3}
    times = [[], [], [], []]
    for line in fr.readlines():
        items = line.rstrip('\n').split(",")
        time = items[0][11:]
        meal = items[2]
        idx = to_idx[meal]
        times[idx].append(time)
    
    vars = []
    for meal_times in times:
        if meal_times:
            var = get_time_var(meal_times)
            vars.append(var)
        else:
            vars.append(0.0)
    print vars
    return vars
            
        
    
def get_feature(func):
    id_feature = {}

    for file in os.listdir(dir):
        if not file.endswith('.txt') :
            continue
        id = file.split('.')[0][-2:]
        
        if id in ['20', '36', '42', '47', '43']:
            continue
        print '--------'
        print 'id: ' + id
        
        result = func(id)   
        id_feature[id] = result
        
    return id_feature  


if __name__ == '__main__':
    #id_feature = get_feature(loc_entropy)
    #write_feature_to_csv(id_feature, 'dining_loc_entropy', False)
    
#     id_features = get_feature(meal_rate)
#     write_multi_features_to_csv(id_features, ['breakfast','lunch','supper','snack'], False)
    
    id_features = get_feature(time_var)
    write_multi_features_to_csv(id_features, ['breakfast_var','lunch_var','supper_var','snack_var'])
    