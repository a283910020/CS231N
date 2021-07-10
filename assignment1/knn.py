import random
import numpy as np
from cs231n.data_utils import load_CIFAR10
import matplotlib.pyplot as plt

# This is a bit of magic to make matplotlib figures appear inline in the notebook
# rather than in a new window.
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# Some more magic so that the notebook will reload external python modules;
# see http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython

cifar10_dir = 'cs231n/datasets/cifar-10-batches-py'

# Cleaning up variables to prevent loading data multiple times (which may cause memory issue)
# try:
#    del X_train, y_train
#    del X_test, y_test
#    print('Clear previously loaded data.')
# except:
#    pass

X_train, y_train, X_test, y_test = load_CIFAR10(cifar10_dir)

# As a sanity check, we print out the size of the training and test data.
print('Training data shape: ', X_train.shape)
print('Training labels shape: ', y_train.shape)
print('Test data shape: ', X_test.shape)
print('Test labels shape: ', y_test.shape)

# Visualize some examples from the dataset.
# We show a few examples of training images from each class.
classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
num_classes = len(classes)
samples_per_class = 7
for y, cls in enumerate(classes):
    idxs = np.flatnonzero(y_train == y)
    idxs = np.random.choice(idxs, samples_per_class, replace=False)
    for i, idx in enumerate(idxs):
        plt_idx = i * num_classes + y + 1
        plt.subplot(samples_per_class, num_classes, plt_idx)
        plt.imshow(X_train[idx].astype('uint8'))
        plt.axis('off')
        if i == 0:
            plt.title(cls)
#plt.show()

num_training = 5000
mask = list(range(num_training))
X_train = X_train[mask]
y_train = y_train[mask]

num_test = 500
mask = list(range(num_test))
X_test = X_test[mask]
y_test = y_test[mask]

# Reshape the image data into rows
X_train = np.reshape(X_train, (X_train.shape[0], -1))
X_test = np.reshape(X_test, (X_test.shape[0], -1))
print(X_train.shape, X_test.shape)

from cs231n.classifiers import KNearestNeighbor

# Create a kNN classifier instance.
# Remember that training a kNN classifier is a noop:
# the Classifier simply remembers the data and does no further processing
# classifier = KNearestNeighbor()
# classifier.train(X_train, y_train)

# dists = classifier.compute_distances_two_loops(X_test)
# print(dists.shape)

# plt.imshow(dists, interpolation='none')
# plt.show()
#
# print("here's Q1'")
# # TODO Inline Question 1
# #
# # Notice the structured patterns in the distance matrix, where some rows or columns are visible brighter.
# # (Note that with the default color scheme black indicates low distances while white indicates high distances.)
# #
# # What in the data is the cause behind the distinctly bright rows?
# # What causes the columns?
#
# # Now implement the function predict_labels and run the code below:
# # We use k = 1 (which is Nearest Neighbor).
# num = 1
# y_test_pred = classifier.predict_labels(dists, k=num)
#
# # Compute and print the fraction of correctly predicted examples
# num_correct = np.sum(y_test_pred == y_test)
# accuracy = float(num_correct) / num_test
# print('when k = %d Got %d / %d correct => accuracy: %f' % (num, num_correct, num_test, accuracy))
# num = 5
# y_test_pred = classifier.predict_labels(dists, k=num)
# num_correct = np.sum(y_test_pred == y_test)
# accuracy = float(num_correct) / num_test
# print('when k = %d Got %d / %d correct => accuracy: %f' % (num, num_correct, num_test, accuracy))
#
#
# # TODO Inline Question 2
#
# # Now lets speed up distance matrix computation by using partial vectorization
# # with one loop. Implement the function compute_distances_one_loop and run the
# # code below:
# dists_one = classifier.compute_distances_one_loop(X_test)
#
# # To ensure that our vectorized implementation is correct, we make sure that it
# # agrees with the naive implementation. There are many ways to decide whether
# # two matrices are similar; one of the simplest is the Frobenius norm. In case
# # you haven't seen it before, the Frobenius norm of two matrices is the square
# # root of the squared sum of differences of all elements; in other words, reshape
# # the matrices into vectors and compute the Euclidean distance between them.
# difference = np.linalg.norm(dists - dists_one, ord='fro')
# print('One loop difference was: %f' % (difference, ))
# if difference < 0.001:
#     print('Good! The distance matrices are the same')
# else:
#     print('Uh-oh! The distance matrices are different')
#
# # Now implement the fully vectorized version inside compute_distances_no_loops
# # and run the code
# dists_two = classifier.compute_distances_no_loops(X_test)
#
# # check that the distance matrix agrees with the one we computed before:
# difference = np.linalg.norm(dists - dists_two, ord='fro')
# print('No loop difference was: %f' % (difference,))
# if difference < 0.001:
#     print('Good! The distance matrices are the same')
# else:
#     print('Uh-oh! The distance matrices are different')
#
# # Let's compare how fast the implementations are
# def time_function(f, *args):
#     """
#     Call a function f with args and return the time (in seconds) that it took to execute.
#     """
#     import time
#     tic = time.time()
#     f(*args)
#     toc = time.time()
#     return toc - tic
#
# two_loop_time = time_function(classifier.compute_distances_two_loops, X_test)
# print('Two loop version took %f seconds' % two_loop_time)
#
# one_loop_time = time_function(classifier.compute_distances_one_loop, X_test)
# print('One loop version took %f seconds' % one_loop_time)
#
# no_loop_time = time_function(classifier.compute_distances_no_loops, X_test)
# print('No loop version took %f seconds' % no_loop_time)
#
# # You should see significantly faster performance with the fully vectorized implementation!
#
# # NOTE: depending on what machine you're using,
# # you might not see a speedup when you go from two loops to one loop,
# # and might even see a slow-down.
#
# # TODO Inline Question Cross-validation
# num_folds = 5
# k_choices = [1, 3, 5, 8, 10, 12, 15, 20, 50, 100]
#
# ################################################################################
# # TODO:                                                                        #
# # Split up the training data into folds. After splitting, X_train_folds and    #
# # y_train_folds should each be lists of length num_folds, where                #
# # y_train_folds[i] is the label vector for the points in X_train_folds[i].     #
# # Hint: Look up the numpy array_split function.                                #
# ################################################################################
# # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
#
# X_train_folds = np.array_split(X_train, num_folds)
# y_train_folds = np.array_split(y_train.reshape(-1, 1), num_folds)
#
# # print(X_train_folds)
# # print(y_train_folds)
#
# # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
#
# # A dictionary holding the accuracies for different values of k that we find
# # when running cross-validation. After running cross-validation,
# # k_to_accuracies[k] should be a list of length num_folds giving the different
# # accuracy values that we found when using that value of k.
# k_to_accuracies = {}
#
# ################################################################################
# # TODO:                                                                        #
# # Perform k-fold cross validation to find the best value of k. For each        #
# # possible value of k, run the k-nearest-neighbor algorithm num_folds times,   #
# # where in each case you use all but one of the folds as training data and the #
# # last fold as a validation set. Store the accuracies for all fold and all     #
# # values of k in the k_to_accuracies dictionary.                               #
# ################################################################################
# # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
#
# for i in k_choices:
#     k_to_accuracies.setdefault(i, [])
#
# for i in range(num_folds):
#     classifier = KNearestNeighbor()
#     X_val_train = np.vstack(X_train_folds[0:i] + X_train_folds[i + 1:])
#     y_val_train = np.vstack(y_train_folds[0:i] + y_train_folds[i + 1:])
#     y_val_train = y_val_train[:, 0]
#
#     classifier.train(X_val_train, y_val_train)
#     dists = classifier.compute_distances_no_loops(X_val_train)
#     for j in k_choices:
#         y_val_pred = classifier.predict(X_train_folds[i], k=j)
#         num_correct = np.sum(y_val_pred == y_train_folds[i][:, 0])
#         accuracy = float(num_correct) / len(y_val_pred)
#         k_to_accuracies[j].append(accuracy)
#
# # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
#
# # Print out the computed accuracies
# for k in sorted(k_to_accuracies):
#     for accuracy in k_to_accuracies[k]:
#         print('k = %d, accuracy = %f' % (k, accuracy))

# TODO:  choose the best value for k
# Based on the cross-validation results above, choose the best value for k,
# retrain the classifier using all the training data, and test it on the test
# data. You should be able to get above 28% accuracy on the test data.
print("k = ", 6)
classifier = KNearestNeighbor()
classifier.train(X_train, y_train)
y_test_pred = classifier.predict(X_test, k=6)

# Compute and display the accuracy
num_correct = np.sum(y_test_pred == y_test)
accuracy = float(num_correct) / num_test
print('Got %d / %d correct => accuracy: %f' % (num_correct, num_test, accuracy))
# ans = []
# for best_k in range(1, 20):
#     print("k = ", best_k)
#     classifier = KNearestNeighbor()
#     classifier.train(X_train, y_train)
#     y_test_pred = classifier.predict(X_test, k=best_k)
#
#     # Compute and display the accuracy
#     num_correct = np.sum(y_test_pred == y_test)
#     accuracy = float(num_correct) / num_test
#     ans.append(accuracy)
#     print('Got %d / %d correct => accuracy: %f' % (num_correct, num_test, accuracy))
# print("the best k = ", np.argmax(ans) + 1)