# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

import os
import numpy as np
import math
from PIL import Image, ImageDraw

from ..core import Filter


class Speedometer(Filter):
    def __init__(self, min_value=0.0, max_value=1.0, **kwargs):
        self._input_shape = 1,
        self._input_dtype = None

        image_filename = os.path.join(os.path.dirname(__file__), os.path.pardir,
                                      os.path.pardir, u"resources", u"speedometer.png")
        self._image = Image.open(image_filename)
        self._shape = self._image.size + (4,)
        self._dtype = np.uint8
        super(Speedometer, self).__init__(name=u"SpeedometerFilter", **kwargs)

        self.min_value = min_value
        self.max_value = max_value
        self._range = self.max_value - self.min_value

        self._center_h = self._shape[0] // 2 + 30
        self._center_w = self._shape[1] // 2

    def filter(self, data):

        zero = 2.617993878   # 5/6 PI
        v = (data[0] - self.min_value) / self._range * 4.188790205 + zero

        radius = self._shape[0]*0.43
        h_e = math.sin(v) * radius + self._center_h
        w_e = math.cos(v) * radius + self._center_w

        copy = self._image.copy()
        draw = ImageDraw.Draw(copy)
        draw.line((self._center_w, self._center_h, w_e, h_e), fill=(249, 155, 20, 255), width=20)

        return np.asarray(copy)
