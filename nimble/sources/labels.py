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
        self.values = []
        self._load()
        super(TransformMatrixSource, self).__init__(name=u"TransformMatrixSource", **kwargs)

    def _load(self):
        with open(self._filename, 'r') as f:
            for line in f.readlines():
                transform = np.fromstring(line, dtype=np.float32, sep=' ')
                transform = transform.reshape(3, 4)
                transform = np.vstack((transform, [0, 0, 0, 1]))
                self.values.append(transform)
        self._size = len(self.values)
        self._shape = (4, 4)

    def get_data_at(self, position):
        return self.values[position]


class ValueFromTxtSource(SeekableSource):
    """Read values line by line from text file."""

    def __init__(self, filename, **kwargs):
        self.parallel_possible = False
        self.cached = True

        self._filename = filename
        self.values = []
        self._load()
        super(ValueFromTxtSource, self).__init__(name=u"ValueFromTxtSource", **kwargs)

    def _load(self):
        with open(self._filename, 'r') as f:
            for line in f.readlines():
                self.values.append(float(line))
        self._size = len(self.values)
        self._shape = (1,)

    def get_data_at(self, position):
        return self.values[position]
