# -*- coding: utf-8 -*-
from __future__ import absolute_import

from scipy import misc

from ..core import Sink


class ImageDisplaySink(Sink):
    def __init__(self, **kwargs):
        super(ImageDisplaySink, self).__init__(**kwargs)

    def set_data(self, data):
        misc.imshow(data)
