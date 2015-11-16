import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from pprint import pprint
import os

def loc_subj(fp, loc_freq):

    with open(fp, 'rU') as fr:
        lines = fr.readlines()
        for line in lines:
            atts = line.strip('\n').split(",")
            if atts[4].startswith('in'):
                loc = atts[4][3:-1]
                if loc not in loc_freq:
                    loc_freq[loc] = 0
                    loc_freq[loc] += 1
                else:
                    loc_freq[loc] += 1
    

    return loc_freq

def bar_plot(loc_freq):
    loc_freq = sorted(loc_freq.items(), key=lambda x: x[1])  
    pprint(loc_freq) 
    print len(loc_freq) 
    
    locations = [x[0] for x in loc_freq]
    y_pos = np.arange(len(locations))
    frequencies = [x[1] for x in loc_freq]
    
    plt.barh(y_pos, frequencies, align='center')
    plt.yticks(y_pos, locations)
    plt.xlabel('frequency')
    plt.show()
    
def get_all_locs():
    dir = r"data\by subjects"
    loc_freq = {}
    for file in os.listdir(dir):
        if not file.endswith('.csv'):
            continue
        fp = os.path.join(dir, file)
        loc_freq = loc_subj(fp, loc_freq)
    #bar_plot(loc_freq)
    print loc_freq.keys()
    
def bar_plot_3d(loc_freq):
    
    pass


if __name__ == '__main__':  
#     x = [1,1,2,3]
#     y = [1,2,3,4]
#     z = [0,0,0, 0]
#     dx = 1
#     dy = 1
#     dz = [4,5,6, 7]
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.bar3d(x,y,z, dx, dy, dz)
#     ax.set_yticks([1,2,3])
#     ax.set_yticklabels(['a', 'b', 'c'])
#     plt.show()

#     fp = r"C:\Users\Sophie\Smart Phone Project Local\by subjects\wifigps_subject05.csv"
#     loc_freq = loc_subj(fp, {})
#     bar_plot(loc_freq)

    get_all_locs()
    
   

            