# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..composition import SeekableSource

import numpy as np


class IntegerSource(SeekableSource):
    """Return integer ranges."""

    def __init__(self, start=0, stop=np.iinfo(np.uint32).max, step=1, name=u"IntegerSource"):
        self.parallel_possible = True
        self.cached = True
        self._shape = 1,
        self._dtype = np.uint32
        self._start = start
        self._stop = stop
        self._step = step
        self._size = abs((stop - start) // step)
        super(IntegerSource, self).__init__(name=name)

    def _get_data_at(self, position):

        return np.array([self._start + position * self._step], dtype=self._dtype)

    @property
    def dtype(self):
        return self._dtype
