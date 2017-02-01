# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

from scipy import misc
import moviepy.editor as mpy

from ..core import Sink


class ImageDisplaySink(Sink):
    def __init__(self, **kwargs):
        super(ImageDisplaySink, self).__init__(**kwargs)

    def set_data(self, data):
        misc.imshow(data)


class ImageVideoSink(Sink):
    def __init__(self, fps=2, name=u"UnnamedVideoSink"):
        super(ImageVideoSink, self).__init__(name=name)
        self._fps = fps
        self._frames = []

    def set_data(self, data):
        self._frames.append(data)

    def write(self, filename):
        def make_frame(t):
            return self._frames[int(round(t*self._fps))][:, :, :3]

        animation = mpy.VideoClip(make_frame, duration=(len(self._frames)-1)/self._fps)
        animation.write_videofile(filename, fps=self._fps, codec='mpeg4')
