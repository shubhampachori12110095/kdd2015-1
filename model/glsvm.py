#!/usr/bin/env python
#-*- coding: utf-8 -*-

import graphlab as gl
import numpy as np
import pandas as pd

from base import *

class SVMClassifier(BaseClassifier):
    """
    Wrapper of Graph Lab SVM Classifier

    Parameters
    ----------
    max_iterations : int, optional
        The maximum number of iterations for boosting. Each iteration results
        in the creation of an extra tree.

    max_depth : float, optional
        Maximum depth of a tree.


    """

    def __init__(self, penalty=10.0, solver='auto', feature_rescaling=True,
                    convergence_threshold=0.01, lbfgs_memory_level=11,
                    max_iterations=10, class_weights=None,
                    validation_set=None, verbose=False):

        self.penalty = penalty
        self.solver = solver
        self.feature_rescaling = feature_rescaling
        self.convergence_threshold = convergence_threshold
        self.lbfgs_memory_level = lbfgs_memory_level
        self.max_iterations = max_iterations
        self.class_weights = class_weights
        self.validation_set = validation_set
        self.verbose = verbose

    def fit(self, X, y):
        """
        Fit the model according to the given training data

        Parameters
        ----------
        X: {array-like}, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features

        y: array-like, shape (n_samples,)
            Target vector relative to X.

        Returns
        -------
        self : object
            return self.
        """

        X = gl.SFrame(pd.DataFrame(X))
        X['target'] = y
        self.model = gl.svm_classifier.create(
                X, target='target',
                penalty = self.penalty,
                solver = self.solver, feature_rescaling = self.feature_rescaling,
                convergence_threshold = self.convergence_threshold,
                lbfgs_memory_level = self.lbfgs_memory_level,
                max_iterations = self.max_iterations, class_weights = self.class_weights,
                validation_set = self.validation_set, verbose = self.verbose)


        self.num_class = len(np.unique(y))

    def predict_proba(self, X):
        """
        Probability estimates.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]

        Returns
        -------
        T : array-like, shape = [n_samples, n_classes]
            Returns the probability of the sample for each class in the model
        """

        # http://forum.dato.com/discussion/706/binary-classification-probabilities-class-labels

        X = gl.SFrame(pd.DataFrame(X))
        preds = self.model.predict(X, output_type="margin")

        # return preds.to_dataframe().as_matrix()

    def predict(self, X):
        """
        Class estimates.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]

        Returns
        -------
        yhat: array-like, shape = (n_samples, )
            Returns the predicted class of the sample
        """
        X = gl.SFrame(pd.DataFrame(X))
        yhat = self.model.predict(X)
        return np.array(yhat)

    def evaluate(self, X, y):
        X = gl.SFrame(pd.DataFrame(X))
        X['target'] = y
        return self.model.evaluate(X, metric='accuracy')

    def print_coefficients(self, num_rows=18):
        pass

if __name__ == "__main__":
    X = np.random.randn(10,3)
    y = np.random.randint(0, 2, 10)
    clf = SVMClassifier()
    clf.fit(X, y)
    print y
    yhat = clf.predict_proba(X)
    print yhat