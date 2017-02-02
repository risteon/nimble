# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..core import Source, SeekableSource

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


class UniformRandomSource(Source):
    """Random values in a given shape."""

    def __init__(self, shape, name=u"", **kwargs):
        self.parallel_possible = True
        self.cached = False
        self._shape = shape
        self._dtype = np.float64
        self._cache = None
        super(UniformRandomSource, self).__init__(name=name, **kwargs)

    def _get_data_impl(self):
        return self._cache

    def advance(self):
        self._cache = np.random.rand(self._shape)
        return True
