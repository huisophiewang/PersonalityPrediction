import os
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def pca(X, d):
    N, D = X.shape
    #print N, D
    X_mean = np.mean(X, axis=0)
    #print X_mean

    Z = np.zeros((D, N))
    for i in range(N):
        Z[:,i] = X[i] - X_mean

    #print Z
    Ux, Sx, Vx = np.linalg.svd(Z)
    print Sx
    #print len(Sx)
    #plot_singular_values(Sx)
    U = Ux[:,:d]
    #print U
    mu = X_mean
    Y = np.zeros((N, d))
    for i in range(N):
        Y[i] = np.dot(U.T, (X[i]-X_mean))
    #print Y
    #print Y.shape
    #np.savetxt('pca_all_freq_pat_support40.csv', Y, delimiter=',')
    np.savetxt('pca95_all_features_extra.csv', Y, delimiter=',')
    
    
    return U, mu, Y

def plot(Y):
    plt.plot(Y[:,0], Y[:,1], 'ro')
    plt.show()

def plot_singular_values(S):
    n = len(S)
    plt.title('singular values')
    plt.plot(range(n), S, 'ro')
    plt.show()
    
def get_covariance(m):
    cov = 0.0
    n = len(m)
    m_mean = np.mean(m, axis=0)
    for i in range(n):
        cov += np.sum((m[i]-m_mean)**2)
    cov /= n
    print cov
    return cov
    
def sklearn_pca(X, d):
    N, D = X.shape
    X_mean = np.mean(X, axis=0)
    #print X_mean
    Z = np.zeros((D, N))
    for i in range(N):
        Z[:,i] = X[i] - X_mean
        
    sklearn_pca = PCA(n_components=2, svd_solver='full')
    Y_sklearn = sklearn_pca.fit_transform(Z.T)
    #print Y_sklearn
    return Y_sklearn

def pca_select_d(X, percent=0.95):
    x_cov = get_covariance(X)
    D = X.shape[1]
    print D
    for j in range(1, D):
        print j
        Y = pca(X, d=j)[2]
        y_cov = get_covariance(Y)
        if y_cov >= percent*x_cov:
            break
    return j   
    
if __name__ == '__main__':
    fp = os.path.join('result', 'feature', 'all_freq_pat_support40.csv')
    fp = os.path.join('result', 'feature', 'all_features_extra.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)

    X = data[:,1:-1]
    #best_d = pca_select_d(X, percent=0.95)
    U, mu, Y = pca(X, 8)


