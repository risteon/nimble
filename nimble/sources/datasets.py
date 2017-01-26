# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from ..composition import LabeledDataSource
from .images import ImageFileSource
from .labels import TransformMatrixSource


class KittiOdometrySource(LabeledDataSource):
    """Read images and ground truth poses of the Kitti dataset.

    http://www.cvlibs.net/datasets/kitti/
    Currently, this only reads the left image.
    """

    def __init__(self, kitti_root_path, sequence, **kwargs):
        self.seekable = True
        self.parallel_possible = False
        self.cached = False

        self._sequence = sequence
        self._sequence_folder = os.path.join(kitti_root_path, u"sequences", u"{:02d}".format(self._sequence),
                                             u"image_2")
        poses_file = os.path.join(kitti_root_path, u"poses", u"{:02d}.txt".format(self._sequence))

        image_source = ImageFileSource(self._image_filename)
        label_source = TransformMatrixSource(poses_file)

        super(KittiOdometrySource, self).__init__(data_source=image_source, label_source=label_source, **kwargs)

    def _image_filename(self, position):
        return os.path.join(self._sequence_folder, "{:06}.png".format(position))
