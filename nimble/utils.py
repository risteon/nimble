from __future__ import division

import struct
import numpy as np


def unpack_floats(batch_labels):

    shape = batch_labels[..., 0].shape
    floats = np.empty(shape, np.float32)
    for index, _ in np.ndenumerate(floats):
        floats[index] = struct.unpack('f', batch_labels[index + (slice(0, 4),)])[0]

    return floats


def unpack_float64s(batch_labels):

    shape = batch_labels[..., 0].shape
    floats = np.empty(shape, np.float64)
    for index, _ in np.ndenumerate(floats):
        floats[index] = struct.unpack('d', batch_labels[index + (slice(0, 8),)])[0]

    return floats


def calculate_labels(batch_labels):
    floats = unpack_floats(batch_labels)
    return np.mean(floats, axis=-1)


def one_hot_encoding(vector, nb_classes):
    """
    Converts an input 1-D vector of integers into an output
    2-D array of one-hot vectors, where an i'th input value
    of j will set a '1' in the i'th row, j'th column of the
    output array.

    Example:
        v = np.array((1, 0, 4))
        one_hot_v = one_hot_encoding(v)
        print one_hot_v

        [[0 1 0 0 0]
         [1 0 0 0 0]
         [0 0 0 0 1]]
    """

    assert isinstance(vector, np.ndarray)
    assert len(vector) > 0

    result = np.zeros(shape=(len(vector), nb_classes), dtype=np.float32)
    result[np.arange(len(vector)), vector] = 1.0
    return result
