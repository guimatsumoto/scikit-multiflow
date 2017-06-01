from abc import ABCMeta, abstractmethod


class BaseClassifier(metaclass=ABCMeta):
    """Base Classifier class
        create a flag to verify if it's the first run
    """
    def __init__(self):
        """ Initialization.
        """
        pass

    @abstractmethod
    def first_fit(self, X, y, classes = None):
        self.fit(X, y, classes)

    @abstractmethod
    def fit(self, X, y, classes = None):
        """Fit model.

        Parameters
        ----------
        X : array
            Samples
        y: array
           True labels
        classes: array, shape (n_classes,), optional
                 Classes.
                 Can be obtained via `np.unique(y)` but note that 'y' doesn't need to contain all labels in `classes`
        """
        pass

    @abstractmethod
    def partial_fit(self, X, y, classes=None):
        """Partial (incremental) fit.
        For online methods.

        Parameters
        ----------
        X : array
            Samples
        y: array
           True labels
        classes: array, shape (n_classes,), optional
                 Classes.
                 Can be obtained via `np.unique(y)` but note that 'y' doesn't need to contain all labels in `classes`

        """
        pass

    @abstractmethod
    def predict(self, X):
        """Predict using the model.

        Parameters
        ----------
        X : array
            Samples

        Returns
        -------
        array, shape (n_samples,)
            Returns the predicted label for each sample in X.
        """
        pass

    @abstractmethod
    def predict_proba(self, X):
        """Probability estimation.

        Parameters
        ----------
        X : array
            Samples

        Returns
        -------
        array, shape (n_samples, n_classes)
            Returns the probability of the sample for each class in the model.
        """
        pass

    @abstractmethod
    def score(self, X, y):
        pass