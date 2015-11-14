import os

import statsmodels.api as sm
import numpy as np
import pandas
import patsy
from patsy.highlevel import dmatrices, dmatrix

# by default, not necessary
#patsy.missing.NAAction(on_NA='drop', NA_types=['None', 'NaN'])

cur_dir = os.path.dirname(os.path.realpath(__file__))

feature = 'entropy'

fp = os.path.join(cur_dir, 'data', 'matrix_data', 'feature_' + feature + '.csv')

df = pandas.read_csv(fp)
print df
# print df.shape
# print df.dtypes

# y1, X = dmatrices('consc ~ entropy', data=df)
# mod1 = sm.OLS(y1, X)
# res1 = mod1.fit()
# print res1.summary()

big_five = ['extra', 'agrbl', 'consc', 'neuro', 'open']
others = ['assertive', 'activity', 'altruism', 'compliance', 'order', 'discipline', 'anxiety', 'depression', 'aesthetics', 'ideas']
all = big_five + others

for i in range(len(all)):
    
    print "#####################################################################################################"
    print all[i]

    y, X = dmatrices('%s ~ %s' % (all[i], feature), data=df)
    mod = sm.OLS(y, X)
    res = mod.fit()
    print res.summary()

# y2, X = dmatrices('open ~ entropy', data=df)
# mod2 = sm.OLS(y2, X)
# res2 = mod2.fit()
# print res2.summary()
# 
# y3, X = dmatrices('activity ~ entropy', data=df)
# mod3 = sm.OLS(y3, X)
# res3 = mod3.fit()
# print res3.summary()