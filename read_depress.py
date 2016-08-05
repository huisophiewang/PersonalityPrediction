to_scale = {"Not at all": 0,
            "Several days": 1,
            "More than half the days": 2,
            "Nearly every day": 3}


fr = open(r'dataset\survey\PHQ-9.csv', 'rU')
cols = fr.readline()

fw = open(r'dataset\survey\PHQ-9Post.csv', 'a')
outlabels = ['uid', 'depress']
fw.write(','.join(outlabels) + '\n')

lines = fr.readlines()
for line in lines:
    items = line.rstrip().split(',')
    
    print '==========='
    id = items[0]
    print id
    type = items[1]
    
    scores = []
    outline = [id]    
    for i, item in enumerate(items[2:]):
        if item in to_scale:
            score = to_scale[item]
            scores.append(score)
          
    depress = sum(scores)    
    outline.append(str(depress))
    if type == 'post':       
        print scores   
        print outline
        fw.write(','.join(outline) + '\n')
        
fw.close()