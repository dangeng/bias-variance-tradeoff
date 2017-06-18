from sklearn.svm import SVR
import matplotlib.pyplot as plt
import numpy as np

def fit(C, epsilon):
    x = np.random.uniform(0, 100, size=(20,1))
    y = (np.sqrt(x) + np.random.normal(0, .5, size=(20,1))).ravel()
    x_mesh = np.array([[i] for i in np.arange(0,100,.5)])

    clf = SVR(C=C, epsilon=epsilon, kernel='poly', degree=2)
    clf.fit(x,y)

    plt.plot(x, y, 'ro')
    plt.plot(x, clf.predict(x), 'bo')
    plt.plot(x_mesh, clf.predict(x_mesh))
    plt.show()
