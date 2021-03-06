__author__ = 'Guilherme Matsumoto'

import numpy as np
from skmultiflow.data.base_instance_stream import BaseInstanceStream
from sklearn.datasets import make_multilabel_classification


class MultilabelGenerator(BaseInstanceStream):
    """ MultilabelGenerator

    This generator creates a stream of samples for a multilabel problem. 
    It uses the make_multilabel_classification function from scikit-learn, 
    which creates a batch setting multilabel classification problem. These 
    samples are then sequentially fed by the next_instance function.

    Parameters
    ----------
    n_samples: int (Default: 40000)
        Total amount of samples to generate.

    n_features: int (Default: 100)
        Number of features to generate.

    n_targets: int (Default: 1)
        Number of targeting tasks to generate.
        
    n_labels: int (Default: 2)
        Number of labels to generate.
        
    Examples
    --------
    >>> # Imports
    >>> from skmultiflow.data.generators.multilabel_generator import MultilabelGenerator
    >>> # Setting up the stream
    >>> stream = MultilabelGenerator(n_samples=40000, n_features=10, n_targets=4, n_labels=4)
    >>> stream.prepare_for_use()
    >>> # Retrieving one sample
    >>> stream.next_instance()
    (array([[ 7.,  2.,  7.,  5.,  3.,  2.,  6.,  8.,  3.,  6.]]), array([[1, 1, 1, 1]]))
    >>> # Retrieving 10 samples
    >>> stream.next_instance(10)
    (array([[  2.,   2.,   5.,   2.,   5.,   5.,   4.,   2.,   3.,   5.],
       [  2.,   1.,   5.,   5.,   1.,   1.,   7.,  10.,   5.,   4.],
       [  6.,   5.,  11.,   6.,  11.,   0.,   4.,   6.,   0.,   1.],
       [  9.,   6.,   4.,   4.,   3.,   9.,   6.,   8.,   9.,   0.],
       [  5.,   3.,   5.,   2.,   5.,   3.,   4.,  10.,   5.,   1.],
       [ 12.,   8.,   9.,   9.,   2.,   5.,   8.,   8.,   4.,   2.],
       [  9.,   8.,   3.,   3.,   4.,   5.,   8.,  11.,   3.,   2.],
       [  5.,   5.,   3.,   0.,   7.,   4.,   7.,   8.,   9.,   0.],
       [  4.,   2.,  11.,   4.,   7.,   2.,   4.,   4.,   3.,   4.],
       [  5.,   0.,  10.,   6.,   6.,   6.,   5.,   4.,  11.,   3.]]), array([[0, 1, 1, 1],
       [1, 1, 1, 1],
       [1, 0, 0, 0],
       [0, 0, 1, 1],
       [1, 1, 1, 1],
       [1, 0, 1, 1],
       [1, 0, 1, 0],
       [0, 1, 1, 1],
       [1, 1, 1, 1],
       [0, 1, 1, 1]]))
    >>> stream.estimated_remaining_instances()
    39989
    >>> stream.has_more_instances()
    True

    """

    def __init__(self, n_samples=40000, n_features=20, n_targets=5, n_labels=2):
        super().__init__()
        self.X = None
        self.y = None
        self.num_samples = 0
        self.num_features = 0
        self.num_target_tasks = 0
        self.num_labels = 0
        self.instance_index = 0
        self.current_instance_y = None
        self.current_instance_x = None
        self.__configure(n_samples, n_features, n_targets, n_labels)

    def __configure(self, n_samples, n_features, n_targets, n_labels):
        """ __configure

        Uses the make_multilabel_classification function from scikit-learn 
        to generate a multilabel classification problem. This problem will 
        be kept in memory and provided as demanded.

        Parameters
        ----------
        n_samples: int
            Total amount of samples to generate.

        n_features: int
            Number of features to generate.

        n_targets: int
            Number of targeting tasks to generate.
        
        n_labels: int
            Number of labels to generate.

        """
        self.X, self.y = make_multilabel_classification(n_samples=n_samples, n_features=n_features, n_classes=n_targets, n_labels=n_labels)
        self.num_samples = n_samples
        self.num_features = n_features
        self.num_target_tasks = n_targets
        self.num_labels = n_labels

    def estimated_remaining_instances(self):
        return (self.num_samples - self.instance_index)

    def has_more_instances(self):
        return (self.num_samples - self.instance_index > 0)

    def next_instance(self, batch_size=1):
        """ next_instance
        
        Return batch_size samples from the X and y matrices stored in
        memory.
        
        Parameters
        ----------
        batch_size: int
            The number of samples to return.
        
        Returns
        -------
        tuple or tuple list
            Return a tuple with the features matrix and the labels matrix for 
            the batch_size samples that were requested.
        
        """
        self.instance_index += batch_size
        try:
            self.current_instance_x = self.X[self.instance_index - batch_size:self.instance_index,:]
            self.current_instance_y = self.y[self.instance_index - batch_size:self.instance_index,:]
            if self.num_target_tasks < 2:
                self.current_instance_y = self.current_instance_y.flatten()

        except IndexError:
            self.current_instance_x = None
            self.current_instance_y = None

        return (self.current_instance_x, self.current_instance_y)

    def is_restartable(self):
        return True

    def restart(self):
        pass

    def has_more_mini_batch(self):
        pass

    def get_num_nominal_attributes(self):
        pass

    def get_num_numerical_attributes(self):
        pass

    def get_num_values_per_nominal_attribute(self):
        pass

    def get_num_attributes(self):
        return self.num_features

    def get_num_targets(self):
        return self.num_target_tasks

    def get_attributes_header(self):
        pass

    def get_classes_header(self):
        pass

    def get_last_instance(self):
        return self.current_instance_x, self.current_instance_y

    def prepare_for_use(self):
        pass

    def get_plot_name(self):
        return 'Multilabel dataset'

    def get_classes(self):
        return np.unique(self.y)

    def get_class_type(self):
        return 'stream'

    def get_info(self):
        return 'MultilabelGenerator: n_samples: ' + str(self.num_samples) + \
               ' - n_features: ' + str(self.num_features) + \
               ' - n_targets: ' + str(self.num_target_tasks) + \
               ' - n_labels:' + str(self.num_labels)

    def get_num_targeting_tasks(self):
        return self.num_target_tasks
