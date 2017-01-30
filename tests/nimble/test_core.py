import pytest

import numpy as np

from nimble.core import Source, Sink


def test_source_sink():

    class A(Source):
        def _get_data_impl(self):
            return np.array([42], dtype=np.int32)

        def advance(self):
            return True

    class B(Sink):
        def set_data(self, data):
            pass

    a = A()
    b = B()
    assert a.advance()
    assert a.get_data() == np.array([42])
    b.set_data(a.get_data())
    assert a.shape is None
