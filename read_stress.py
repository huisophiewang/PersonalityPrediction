
to_scale = {"Never": 0,
            "Almost never": 1,
            "Sometime": 2,
            "Fairly often": 3,
            "Very often": 4}

reverse = [4, 5, 7, 8]

fr = open(r'dataset\survey\PerceivedStressScale.csv', 'rU')
cols = fr.readline()

fw = open(r'dataset\survey\PerceivedStressScalePost.csv', 'a')
outlabels = ['uid', 'stress']
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
            if i+1 in reverse:
                score = 4 - to_scale[item]
            else:
                score = to_scale[item]
            scores.append(score)
          
    stress = sum(scores)    
    outline.append(str(stress))
    if type == 'post':       
        print scores   
        print outline
        fw.write(','.join(outline) + '\n')
        
fw.close()