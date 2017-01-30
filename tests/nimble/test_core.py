import pytest

import numpy as np

from nimble.core import Source


def test_source():

    class S(Source):
        def _get_data_impl(self):
            return np.array([42], dtype=np.int32)

        def advance(self):
            return True

        def dtype(self):
            return np.int32

    s = S()
    assert s.advance()
    assert s.get_data() == np.array([42])
    assert s.shape is None
