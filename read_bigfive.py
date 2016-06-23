
from util import traits
    
to_scale = {"Disagree strongly": 1,
            "Disagree a little": 2,
            "Neither agree nor disagree": 3,
            "Agree a little": 4,
            "Agree strongly": 5}

reverse = [6, 21, 31, 2, 12, 27, 37, 8, 18, 23, 43, 9, 24, 34, 35, 41]

idx = {'extra':[1, 6, 11, 16, 21, 26, 31, 36],
     'agrbl' : [2, 7, 12, 17, 22, 27, 32, 37, 42],
     'consc' : [3, 8, 13, 18, 23, 28, 33, 38, 43],
     'neuro' : [4, 9, 14, 19, 24, 29, 34, 39],
     'openn' : [5, 10, 15, 20, 25, 30, 35, 40, 41, 44]}


fr = open(r'dataset\survey\BigFive.csv', 'rU')
cols = fr.readline()

fw = open(r'dataset\survey\BigFivePost.csv', 'a')
outlabels = ['uid']
outlabels.extend(traits)
fw.write(','.join(outlabels) + '\n')

lines = fr.readlines()
for line in lines:
    items = line.rstrip().split(',')
    
    print '==========='
    id = items[0]
    print id
    type = items[1]
    #print type
    scores = []
    outline = [id]
    for item in items[2:]:
        if item in to_scale:
            score = to_scale[item]
            scores.append(score)
        else:
            scores.append('nan')
            
    for trait in traits:
        #print trait
        trait_scores = []
        
        for i in idx[trait]:

            if i in reverse and scores[i-1]!='nan':                              
                scores[i-1] = 6 - scores[i-1]
 
            trait_scores.append(scores[i-1])
        
        
        avg = 0
        n = 0
        for s in trait_scores:
            if s != 'nan':
                avg += s
                n += 1
        avg = avg / float(n)
        outline.append("{0:.3f}".format(avg))
        
        print str(trait) + ': ' + "{0:.3f}".format(avg)
        print trait_scores
            
    if type == 'post':        
        fw.write(','.join(outline) + '\n')
        
fw.close()

    
    
