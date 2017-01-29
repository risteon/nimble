# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

import os
import imageio

from ..composition import SeekableSource


class ImageFileSource(SeekableSource):
    """

    """

    def __init__(self, filename_func, nb_images=None, **kwargs):
        self.parallel_possible = False
        self.cached = False

        self._filename_func = filename_func
        self._size = nb_images
        self._check_files()
        super(ImageFileSource, self).__init__(name=u"ImageFileSource", **kwargs)

    def _get_data_at(self, position):
        file = self._filename_func(position)
        im = imageio.imread(file)
        return im

    def _check_files(self):
        # check how many continuously numbered images are available
        if self._size is None:
            max_nb = int(1e12)
        else:
            max_nb = self._size

        counter = 0
        while os.path.isfile(self._filename_func(counter)) and counter < max_nb:
            counter += 1

        if self._size is None:
            self._size = counter
        elif self._size < counter:
            raise RuntimeError("Not all image files were found.")

        if self._size > 0:
            image = self._get_data_at(0)
            self._dtype = image.dtype
            self._shape = image.shape
        else:
            self._dtype = None
            self._shape = None

    @property
    def dtype(self):
        return self._dtype
