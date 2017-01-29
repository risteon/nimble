import pytest

import numpy as np

from nimble.sources import IntegerIdentitySource
from nimble.composition import ConcatenateSource, VStackSource


def test_concatenate_sources():
    nb_elements = 14
    ints_a = IntegerIdentitySource(size=nb_elements)
    ints_b = IntegerIdentitySource(size=nb_elements)
    ints_c = IntegerIdentitySource(size=nb_elements)

    s = ConcatenateSource([ints_a, ints_b, ints_c])
    assert s.seekable
    assert s.cached
    assert s.parallel_possible
    assert s.size == 3 * nb_elements

    assert s.get_data() is None
    assert s.advance()
    assert s.get_data() == 0
    assert s.seek(nb_elements)
    assert s.get_data() == 0
    assert s.advance()
    assert s.get_data() == 1
    assert not s.seek(s.size)
    assert s.get_data() == 1

    while s.advance():
        assert s.get_data() == s.position % nb_elements


def test_concatenate_same_source():
    nb_elements = 345
    source = IntegerIdentitySource(size=nb_elements)
    concat = ConcatenateSource([source, source])
    assert concat.size == 2*nb_elements
    assert concat.seekable
    assert concat.cached
    assert concat.parallel_possible

    assert concat.advance()
    assert concat.get_data() == 0
    assert concat.advance()
    assert concat.get_data() == 1
    assert source._get_data_at(42) == 42
    assert concat.get_data() == 1


def test_vstack_source():
    ints = IntegerIdentitySource()
    dim_size = 8
    stacked = VStackSource(ints, dim_size)
    assert stacked.has_fixed_shape()
    assert stacked.shape == (8, 1)
    assert stacked.advance()
    data = stacked.get_data()
    assert data.shape == stacked.shape == (8, 1)
    np.testing.assert_equal(stacked.get_data(), np.reshape(np.arange(8), data.shape))
    assert not stacked.seek(ints.size - (dim_size//2))


if __name__ == '__main__':
    pytest.main([__file__])
