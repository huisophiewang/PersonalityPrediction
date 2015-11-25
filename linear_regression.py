import numpy as np


fp = r"data\matrix_data\all_wifi_features.csv"
x_cols = [1,2,3]
y_cols = range(4, 19)


data_x = np.loadtxt(fp, delimiter=",", skiprows = 1, usecols=x_cols)
data_y = np.genfromtxt(fp, delimiter=",", skiprows = 1, usecols=y_cols)
print data_y

n = data_x.shape[0]