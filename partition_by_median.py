import numpy as np

print np.median([1, 2, 3, 4])
fp = r"data\matrix_data\all_wifi_features.csv"
data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)

x_cols = [1,2,3]
y_cols = range(4, 19)

import statsmodels