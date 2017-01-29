# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..composition import SeekableSource

import numpy as np


class IntegerIdentitySource(SeekableSource):
    """Return the integer used as position argument."""

    def __init__(self, size=np.iinfo(np.uint32).max, **kwargs):
        self.parallel_possible = True
        self.cached = True
        self._shape = 1,
        self._size = size
        super(IntegerIdentitySource, self).__init__(name=u"IntegerIdentitySource", **kwargs)

    def _get_data_at(self, position):
        return np.array([position])

    @property
    def dtype(self):
        return np.uint32
