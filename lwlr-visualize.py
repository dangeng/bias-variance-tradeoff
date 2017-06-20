"""
This module implements the Lowess function for nonparametric regression.

Functions:
lowess Fit a smooth nonparametric regression curve to a scatterplot.

For more information, see

William S. Cleveland: "Robust locally weighted regression and smoothing
scatterplots", Journal of the American Statistical Association, December 1979,
volume 74, number 368, pp. 829-836.

William S. Cleveland and Susan J. Devlin: "Locally weighted regression: An
approach to regression analysis by local fitting", Journal of the American
Statistical Association, September 1988, volume 83, number 403, pp. 596-610.
"""

# Authors: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#
# License: BSD (3-clause)

from math import ceil
import numpy as np
from scipy import linalg


def lowess(x, y, f=2. / 3., iter=3):
    """lowess(x, y, f=2./3., iter=3) -> yest

    Lowess smoother: Robust locally weighted regression.
    The lowess function fits a nonparametric regression curve to a scatterplot.
    The arrays x and y contain an equal number of elements; each pair
    (x[i], y[i]) defines a data point in the scatterplot. The function returns
    the estimated (smooth) values of y.

    The smoothing span is given by f. A larger value for f will result in a
    smoother curve. The number of robustifying iterations is given by iter. The
    function will run faster with a smaller number of iterations.
    """
    n = len(x)
    r = int(ceil(f * n))
    h = [np.sort(np.abs(x - x[i]))[r] for i in range(n)]
    w = np.clip(np.abs((x[:, None] - x[None, :]) / h), 0.0, 1.0)
    w = (1 - w ** 3) ** 3
    yest = np.zeros(n)
    delta = np.ones(n)
    for iteration in range(iter):
        for i in range(n):
            weights = delta * w[:, i]
            b = np.array([np.sum(weights * y), np.sum(weights * y * x)])
            A = np.array([[np.sum(weights), np.sum(weights * x)],
                          [np.sum(weights * x), np.sum(weights * x * x)]])
            beta = linalg.solve(A, b)
            yest[i] = beta[0] + beta[1] * x[i]

        residuals = y - yest
        s = np.median(np.abs(residuals))
        delta = np.clip(residuals / (6.0 * s), -1, 1)
        delta = (1 - delta ** 2) ** 2

    return yest

if __name__ == '__main__':
    import math
    n = 150
    x = np.random.uniform(0, 2 * math.pi, size=n)
    x.sort()
    y = np.sin(x) + 0.3 * np.random.randn(n)

    import pylab as pl

    train_err = []
    actual_err = []
    
    x_test = np.random.uniform(0, 2 * math.pi, 1000)
    y_test = np.sin(x_test) + 0.3 * np.random.randn(1000)


    for f in np.arange(.01,.98,.01):
        yest = lowess(x, y, f=1-f, iter=3)
        pl.clf()
        pl.plot(x, y, 'rx', label='y noisy')
        pl.plot(x, yest, label='y pred')
        pl.savefig('figures-1/' + str(int(np.round(f*100))) + '.png', format='png')

        training_error = np.mean(np.abs(yest-y))

        #test data
        pred = np.interp(x_test, x, yest)

        actual_error = np.mean(np.abs(pred-y_test))
        train_err.append(training_error)
        actual_err.append(actual_error)

        print 1-f

    for i in range(len(train_err)):
        pl.clf()
        pl.xlim([-1,97])
        pl.scatter(np.arange(len(train_err)), train_err, marker='o', c='r')
        pl.scatter(np.arange(len(train_err)), actual_err, marker='o', c='b')
        pl.scatter(np.arange(len(train_err))[i], actual_err[i], marker='o', c='y', s=100)
        pl.scatter(np.arange(len(train_err))[i], train_err[i], marker='o', c='y', s=100)
        pl.savefig('errors-1/' + str(i) + '.png', format='png')
