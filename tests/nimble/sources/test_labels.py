# -*- coding: utf-8 -*-
import pytest
import numpy as np

import tempfile

from nimble.test_utils import txt_values, transform_values
from nimble.sources import ValueFromTxtSource


def test_value_from_txt_source(txt_values):
    file, values = txt_values

    source = ValueFromTxtSource(file.name)
    assert source.size == 6
    assert source.shape == (1,)
    assert source.get_data() is None

    v = []
    while source.advance():
        v.append(source.get_data())

    assert v == values


if __name__ == '__main__':
    pytest.main([__file__])
