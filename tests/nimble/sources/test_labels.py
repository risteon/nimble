import pytest
import numpy as np

import tempfile

from nimble.sources import ValueFromTxtSource


@pytest.fixture(scope="function")
def txt_values():
    values = [23.0, 24.0, 25e-2, -26, -27.0, -28e3]
    b_string = b''
    for v in values:
        b_string += '{}\n'.format(v).encode()

    fp = tempfile.NamedTemporaryFile()
    fp.write(b_string)
    fp.seek(0)
    yield fp, values
    fp.close()


@pytest.fixture(scope="function")
def transform_values():
    t = np.asarray([1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.])
    t = np.reshape(t, (4, 3))


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
