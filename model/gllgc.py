#!/usr/bin/env python
#-*- coding: utf-8 -*-

import graphlab as gl
import numpy as np
import pandas as pd

from base import *

class LogisticClassifier(BaseClassifier):
    """
    Wrapper of Graph Lab Logistic Classifier

    Parameters
    ----------
    max_iterations : int, optional
        The maximum number of iterations for boosting. Each iteration results
        in the creation of an extra tree.

    max_depth : float, optional
        Maximum depth of a tree.


    """

    def __init__(self, l2_penalty=0.01, l1_penalty=0.0,
                    solver='auto', feature_rescaling=False,
                    convergence_threshold=0.01, step_size=1.0,
                    lbfgs_memory_level=11, max_iterations=10,
                    class_weights=None, validation_set=None,
                    verbose=True):
        """
        For this model, the Newton-Raphson method is equivalent to the iteratively
        re-weighted least squares algorithm. If the l1_penalty is greater than 0,
        use the ‘fista’ solver.

        The model is trained using a carefully engineered collection of methods
        that are automatically picked based on the input data.
        The "newton" method works best for datasets with plenty of examples and few features
        (long datasets).

        Limited memory BFGS (lbfgs) is a robust solver for wide datasets (i.e datasets
        with many coefficients). fista is the default solver for l1-regularized linear
        regression. The solvers are all automatically tuned and the default options
        should function well.

        See the solver options guide for setting additional parameters for each of the solvers.
        """
        self.l2_penalty = l2_penalty
        self.l1_penalty = l1_penalty
        self.solver = solver
        self.feature_rescaling = feature_rescaling
        self.convergence_threshold = convergence_threshold
        self.step_size = step_size
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
        self.model = gl.logistic_classifier.create(
                X, target='target',
                l2_penalty = self.l2_penalty, l1_penalty = self.l1_penalty,
                solver = self.solver, feature_rescaling = self.feature_rescaling,
                convergence_threshold = self.convergence_threshold,
                step_size = self.step_size, lbfgs_memory_level = self.lbfgs_memory_level,
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

        X = gl.SFrame(pd.DataFrame(X))
        preds = self.model.predict_topk(X, output_type = 'probability',
                                   k = self.num_class)
        preds['id'] = preds['id'].astype(int) + 1
        preds = preds.unstack(['class', 'probability'], 'probs').unpack(
                                'probs', '')

        preds = preds.sort('id')
        # print preds['id']

        del preds['id']
        return preds.to_dataframe().as_matrix()

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
        coefficients = self.model['coefficients']
        coefficients.print_rows(num_rows=num_rows)


if __name__ == "__main__":
    X = np.random.randn(10,3)
    y = np.random.randint(0, 2, 10)
    clf = LogisticClassifier()
    clf.fit(X, y)
    yhat = clf.predict(X)
