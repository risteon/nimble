# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

from scipy import misc
import moviepy.editor as mpy

from ..core import Sink, ControllingSink


class ImageDisplaySink(Sink):
    def __init__(self, **kwargs):
        super(ImageDisplaySink, self).__init__(**kwargs)

    def set_data(self, data):
        misc.imshow(data)


class ImageVideoSink(ControllingSink):
    """Example for a sink that can only be used with run() and a seekable source."""

    def __init__(self, fps=2, filename=u"/tmp/nimble_video.mp4", name=u"UnnamedVideoSink"):
        super(ImageVideoSink, self).__init__(name=name)
        self._fps = fps
        self.filename = filename

    def run(self, stream):
        def make_frame(t):
            stream.seek(int(round(t*self._fps)))
            return stream.get_data()[:, :, :3]

        animation = mpy.VideoClip(make_frame, duration=(stream.size-1)/self._fps)
        animation.write_videofile(self.filename, fps=self._fps, codec='mpeg4')
