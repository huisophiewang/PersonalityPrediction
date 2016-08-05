import csv


q1 = {"Excellent": 100,
      "Very good": 75,
      "Good": 50,
      "Fair": 25,
      "Poor": 0}

q2 = {"Yes, limited a lot": 0,
      "Yes, limited a little": 50,
      "No, not limited at all": 100}


q34 = {"No, none of the time": 1,
       "Yes, a little of the time": 1,
       "Yes, some of the time": 0,
       "Yes, most of the time": 0,
       "Yes, all of the time": 0}

q5 = {"Not at all": 100, 
      "A little bit": 75, 
      "Moderately": 50, 
      "Quite a bit": 25, 
      "Extremely": 0}

q6t = {"All of the time": 100,
      "Most of the time": 80,
      "A good bit of the time": 60,
      "Some of the time": 40,
      "A little of the time": 20,
      "None of the time": 0}

q6r = {"All of the time": 0,
      "Most of the time": 20,
      "A good bit of the time": 40,
      "Some of the time": 60,
      "A little of the time": 80,
      "None of the time": 100}

q7 = {"None of the time": 100,
      "A little of the time": 75,
      "Some of the time": 50,
      "Most of the time": 25,
      "All of the time": 0}

to_scale = [q1, q2, q2, q34, q34, q34, q34, 
            q5, q6t, q6t, q6r, q7]

def get_final_score(scores):
    I1 = scores[0]
    I4 = scores[1]
    I6 = scores[2]
    I18 = scores[3]
    I15 = scores[4]
    I14 = scores[5]
    I19 = scores[6]
    I22 = scores[7]
    I26 = scores[8]
    I27 = scores[9]
    I28 = scores[10]
    I32 = scores[11]
    
    ## q1
    if I1==0:
        GH1_1=1
    elif I1>=0:
        GH1_1=0
    if I1==25:
        GH1_2=1
    elif I1>=0:
        GH1_2=0
    if I1==50:
        GH1_3=1
    elif I1>=0:
        GH1_3=0
    if I1==75:
        GH1_4=1
    elif I1>=0:
        GH1_4=0
        
    ## q2a
    if I4==0:
        PF02_1=1
    elif I4>=0:
        PF02_1=0
    if I4==50:
        PF02_2=1
    elif I4>=0:
        PF02_2=0
        
    ## q2b
    if I6==0:
        PF04_1=1
    elif I6>=0:
        PF04_1=0
    if I6==50:
        PF04_2=1
    elif I6>=0:
        PF04_2=0
    
    ########################
    ## doesn't match, actual questionnaire has 5 options
    ## q4a
    if I14==0:
        RP2_1=1
    elif I14>=0:
        RP2_1=0
    ## q3b
    if I15==0:
        RP3_1=1
    elif I15>=0:
        RP3_1=0
    ## q3a
    if I18==0:
        RE2_1=1
    elif I18>=0:
        RE2_1=0
    ## q4b
    if I19==0:
        RE3_1=1
    elif I19>=0:
        RE3_1=0
        
    ## q5
    if I22==0:
        BP2_1=1
    elif I22>=0:
        BP2_1=0
    if I22==25:
        BP2_2=1
    elif I22>=0:
        BP2_2=0
    if I22==50:
        BP2_3=1
    elif I22>=0:
        BP2_3=0
    if I22==75:
        BP2_4=1
    elif I22>=0:
        BP2_4=0
        
    ## q6a    
    if I26==0:
        EM3_1=1
    elif I26>=0:
        EM3_1=0
    if I26==20:
        EM3_2=1
    elif I26>=0:
        EM3_2=0
    if I26==40:
        EM3_3=1
    elif I26>=0:
        EM3_3=0
    if I26==60:
        EM3_4=1
    elif I26>=0:
        EM3_4=0
    if I26==80:
        EM3_5=1
    elif I26>=0:
        EM3_5=0
    ## q6b
    if I27==0:
        EN2_1=1
    elif I27>=0:
        EN2_1=0
    if I27==20:
        EN2_2=1
    elif I27>=0:
        EN2_2=0
    if I27==40:
        EN2_3=1
    elif I27>=0:
        EN2_3=0
    if I27==60:
        EN2_4=1
    elif I27>=0:
        EN2_4=0
    if I27==80:
        EN2_5=1
    elif I27>=0:
        EN2_5=0
    ## q6c
    if I28==0:
        EM4_1=1
    elif I28>=0:
        EM4_1=0
    if I28==20:
        EM4_2=1
    elif I28>=0:
        EM4_2=0
    if I28==40:
        EM4_3=1
    elif I28>=0:
        EM4_3=0
    if I28==60:
        EM4_4=1
    elif I28>=0:
        EM4_4=0
    if I28==80:
        EM4_5=1
    elif I28>=0:
        EM4_5=0
        
    ## q7
    if I32==0:
        SF2_1=1
    elif I32>=0:
        SF2_1=0
    if I32==25:
        SF2_2=1
    elif I32>=0:
        SF2_2=0
    if I32==50:
        SF2_3=1
    elif I32>=0:
        SF2_3=0
    if I32==75:
        SF2_4=1
    elif I32>=0:
        SF2_4=0
        
    RAWPCS12 = (PF02_1 *  -7.23216) + (PF02_2 * -3.45555) + \
                (PF04_1 *  -6.24397) + (PF04_2 * -2.73557) + \
                (RP2_1  *  -4.61617) + (RP3_1  * -5.51747) + \
                (BP2_1  * -11.25544) + (BP2_2  * -8.38063) + \
                (BP2_3  *  -6.50522) + (BP2_4  * -3.80130) + \
                (GH1_1  *  -8.37399) + (GH1_2  * -5.56461) + \
                (GH1_3  *  -3.02396) + (GH1_4  * -1.31872) + \
                (EN2_1  *  -2.44706) + (EN2_2  * -2.02168) + \
                (EN2_3  *  -1.61850) + (EN2_4  * -1.14387) + \
                (EN2_5  *  -0.42251) + (SF2_1  * -0.33682) + \
                (SF2_2  *  -0.94342) + (SF2_3  * -0.18043) + \
                (SF2_4  *   0.11038) + (RE2_1  *  3.04365) + \
                (RE3_1  *   2.32091) + (EM3_1  *  3.46638) + \
                (EM3_2  *   2.90426) + (EM3_3  *  2.37241) + \
                (EM3_4  *   1.36689) + (EM3_5  *  0.66514) + \
                (EM4_1  *   4.61446) + (EM4_2  *  3.41593) + \
                (EM4_3  *   2.34247) + (EM4_4  *  1.28044) + \
                (EM4_5  *   0.41188)
                
    RAWMCS12 = (PF02_1 *   3.93115) + (PF02_2 *   1.86840) + \
                (PF04_1 *   2.68282) + (PF04_2 *   1.43103) + \
                (RP2_1  *   1.44060) + (RP3_1  *   1.66968) + \
                (BP2_1  *   1.48619) + (BP2_2  *   1.76691) + \
                (BP2_3  *   1.49384) + (BP2_4  *   0.90384) + \
                (GH1_1  *  -1.71175) + (GH1_2  *  -0.16891) + \
                (GH1_3  *   0.03482) + (GH1_4  *  -0.06064) + \
                (EN2_1  *  -6.02409) + (EN2_2  *  -4.88962) + \
                (EN2_3  *  -3.29805) + (EN2_4  *  -1.65178) + \
                (EN2_5  *  -0.92057) + (SF2_1  *  -6.29724) + \
                (SF2_2  *  -8.26066) + (SF2_3  *  -5.63286) + \
                (SF2_4  *  -3.13896) + (RE2_1  *  -6.82672) + \
                (RE3_1  *  -5.69921) + (EM3_1  * -10.19085) + \
                (EM3_2  *  -7.92717) + (EM3_3  *  -6.31121) + \
                (EM3_4  *  -4.09842) + (EM3_5  *  -1.94949) + \
                (EM4_1  * -16.15395) + (EM4_2  * -10.77911) + \
                (EM4_3  *  -8.09914) + (EM4_4  *  -4.59055) + \
                (EM4_5  *  -1.95934)
    
    RPCS12 = RAWPCS12 + 56.57706
    RMCS12 = RAWMCS12 + 60.75781
    
    return (RPCS12, RMCS12)
                
                
if __name__ == '__main__':
    fr = open(r'dataset\survey\vr_12.csv', 'rU')
    cols = fr.readline()
    fw = open(r'dataset\survey\vr_12Post.csv', 'a')
    outlabels = ['uid', 'pcs', 'mcs']
    fw.write(','.join(outlabels) + '\n')
    for line in csv.reader(fr):
        print line
        items = line
        print '==========='
        id = items[0]
        print id
        type = items[1]
        if type == 'post':
            scores = []
            outline = [id]
            for i, item in enumerate(items[2:14]):
                print i, item
                print to_scale[i]
                score = to_scale[i][item] 
                scores.append(score)
            psc, msc = get_final_score(scores)
            outline.append("{0:.3f}".format(psc))
            outline.append("{0:.3f}".format(msc))
            fw.write(','.join(outline) + '\n')
    fw.close()
        
    


           