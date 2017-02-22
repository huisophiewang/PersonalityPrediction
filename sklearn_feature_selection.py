
import os
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

fp = os.path.join('result', 'feature', 'all_features_extra_cls.csv')
data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
#np.random.shuffle(data)
x = data[:, 1:-1]
y = data[:,-1]
# create a base classifier used to evaluate a subset of attributes
model = LogisticRegression()
# create the RFE model and select 3 attributes
rfe = RFE(model, 3)
rfe = rfe.fit(x, y)
# summarize the selection of the attributes
print(rfe.support_)
print(rfe.ranking_)