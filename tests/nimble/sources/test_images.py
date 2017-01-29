# -*- coding: utf-8 -*-
import pytest

import os

from nimble.test_utils import test_image
from nimble.sources import ImageFileSource


def test_image_file_source(test_image):
    filename, shape = test_image

    def filename_func(position):
        if position == 0:
            return filename
        else:
            return u"doesnt_exist"

    images = ImageFileSource(filename_func=filename_func)
    assert images.size == 1
    assert images.get_data() is None
    assert images.advance()
    image = images.get_data()
    assert image.shape == shape
