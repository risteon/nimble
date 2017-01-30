# -*- coding: utf-8 -*-
import pytest
import tempfile
import os
import numpy as np


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


@pytest.fixture(scope="module")
def test_image_path():
    image_filename = os.path.join(os.path.dirname(__file__),
                                  os.path.pardir, u"resources", u"test_image.png")

    return image_filename, (400, 600, 4)
