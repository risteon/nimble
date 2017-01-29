# -*- coding: utf-8 -*-
from __future__ import absolute_import

import numpy as np

from ..composition import SeekableSource


class TransformMatrixSource(SeekableSource):
    """ Read transform matrices from text file.

    Each line has to consist of 12 values.
    """

    def __init__(self, filename, **kwargs):
        self.parallel_possible = False
        self.cached = True

        self._filename = filename
        self.values = None
        self._load()
        super(TransformMatrixSource, self).__init__(name=u"TransformMatrixSource", **kwargs)

    def _load(self):
        self._dtype = np.float32
        v = []
        with open(self._filename, 'r') as f:
            for line in f.readlines():
                transform = np.fromstring(line, dtype=self._dtype, sep=' ')
                transform = transform.reshape(3, 4)
                transform = np.vstack((transform, [0, 0, 0, 1]))
                v.append(transform)
        self._size = len(v)
        self._shape = (4, 4)
        self.values = np.vstack(v)

    def _get_data_at(self, position):
        return self.values[position]

    @property
    def dtype(self):
        return self._dtype


class ValueFromTxtSource(SeekableSource):
    """Read values line by line from text file."""

    def __init__(self, filename, **kwargs):
        self.parallel_possible = False
        self.cached = True

        self._filename = filename
        self.values = None
        self._load()
        super(ValueFromTxtSource, self).__init__(name=u"ValueFromTxtSource", **kwargs)

    def _load(self):
        v = []
        with open(self._filename, 'r') as f:
            for line in f.readlines():
                v.append(float(line))
        self._size = len(v)
        self.values = np.asarray(v)
        self._shape = (1,)

    def _get_data_at(self, position):
        return self.values[position]

    @property
    def dtype(self):
        return np.float32
