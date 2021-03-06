"""Machine Learning Online Class Exercise 8 |a Anomly Detection and Collaborative Filtering
Instructions
------------
This file contains code that helps you get started on the
exercise. You will need to complete the following functions:
   estimateGaussian
   selectThreshold
   cofiCostFunc
For this exercise, you will not need to change any code in this file,
or any other files other than those mentioned above.
"""

# Imports:
import scipy.io as io
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import multivariate_normal
import ex8helper as helper


def main():
    #  ================== Part 1: Load Example Dataset  ===================
    #  We start this exercise by using a small dataset that is easy to
    #  visualize.
    #  Our example case consists of 2 network server statistics across
    #  several machines: the latency and throughput of each machine.
    #  This exercise will help us find possibly faulty (or very fast) machines.

    print('Visualizing example dataset for outlier detection.\n')

    #  The following command loads the dataset. You should now have the
    #  variables X, Xval, yval in your environment
    mat = io.loadmat('./data/ex8data1.mat')
    X = mat['X']

    #  Visualize the example dataset
    plt.scatter(
        X[:, 0],
        X[:, 1],
        marker='x',
        color='b',
        s=5)

    plt.axis([0, 30, 0, 30])
    plt.xlabel('Latency (ms)')
    plt.ylabel('Throughput (mb/s)')
    plt.show()

    input('Part 1 completed. Program paused. Press enter to continue: ')

    #  ================== Part 2: Estimate the dataset statistics ===================
    #  For this exercise, we assume a Gaussian distribution for the dataset.
    #  We first estimate the parameters of our assumed Gaussian distribution,
    #  then compute the probabilities for each of the points and then visualize
    #  both the overall distribution and where each of the points falls in
    #  terms of that distribution.
    print('Visualizing Gaussian fit...\n')

    mean = np.mean(X, axis=0)
    variance = np.var(X, axis=0)

    #  Returns the density of the multivariate normal at each data point (row)
    #  of X
    P = multivariate_normal.pdf(
        X,
        mean=mean,
        cov=variance)

    #  Visualize the fit
    helper.visualizeFit(X, mean, variance)
    plt.scatter(
        X[:, 0],
        X[:, 1],
        marker='x',
        color='b',
        s=5)

    plt.xlabel('Latency (ms)')
    plt.ylabel('Throughput (mb/s)')
    plt.show()

    input('Part 2 completed. Program paused. Press enter to continue: ')

    #  ================== Part 3: Find Outliers ===================
    #  Now you will find a good epsilon threshold using a cross-validation set
    #  probabilities given the estimated Gaussian distribution
    print('Visualize outliers...\n')

    Xval = mat['Xval']
    yval = mat['yval'].flatten()
    pval = multivariate_normal.pdf(
        Xval,
        mean=mean,
        cov=variance)

    F1, epsilon = helper.selectThreshold(yval, pval)

    print('Best epsilon found using cross-validation: {:.2e}'.format(epsilon))
    print('Best F1 on Cross Validation Set:  {:.6f}'.format(F1))
    print('    (you should see a value epsilon of about 8.99e-05)')
    print('    (you should see a Best F1 value of  0.875000)')

    #  Find the outliers in the training set and plot the
    outliers = X[P < epsilon, :]

    #  Draw a red circle around those outliers
    helper.visualizeFit(X, mean, variance)
    plt.scatter(
        X[:, 0],
        X[:, 1],
        marker='x',
        color='b',
        s=5)
    plt.scatter(
        outliers[:, 0],
        outliers[:, 1],
        s=80,
        facecolors='none',
        edgecolors='r')

    plt.xlabel('Latency (ms)')
    plt.ylabel('Throughput (mb/s)')
    plt.show()

    input('\nPart 3 completed. Program paused. Press enter to continue: ')

    #  ================== Part 4: Multidimensional Outliers ===================
    #  We will now use the code from the previous part and apply it to a
    #  harder problem in which more features describe each datapoint and only
    #  some features indicate whether a point is an outlier.
    print('Testing with Multidimensional Outliers...\n')

    #  Loads the second dataset. You should now have the
    #  variables X, Xval, yval in your environment
    mat = io.loadmat('./data/ex8data2.mat')
    X = mat['X']
    Xval = mat['Xval']
    yval = mat['yval'].flatten()

    #  Apply the same steps to the larger dataset
    mean = np.mean(X, axis=0)
    variance = np.var(X, axis=0)

    #  Training set
    P = multivariate_normal.pdf(
        X,
        mean=mean,
        cov=variance)

    #  Cross-validation set
    pval = multivariate_normal.pdf(
        Xval,
        mean=mean,
        cov=variance)

    #  Find the best threshold
    F1, epsilon = helper.selectThreshold(yval, pval)

    outliers = (P < epsilon).astype(np.int)
    print('Best epsilon found using cross-validation: {:.2e}'.format(epsilon))
    print('Best F1 on Cross Validation Set:  {:.6f}'.format(F1))
    print('    (you should see a value epsilon of about 1.38e-18)')
    print('    (you should see a Best F1 value of  0.615385)')
    print('Total number of Outliers found = {}'.format(np.sum(outliers)))

    input('\nPart 4 completed. Program completed. Press enter to exit: ')

if __name__ == '__main__':
    main()
