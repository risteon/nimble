from __future__ import division

import numpy as np
from scipy.misc import imresize

# scale Label
SCALING_FACTOR = 0.1


def convert_to_scaled_floats(x):
    r = x.astype(np.float32)
    r /= 255
    return r


def flip_axis(x, axis):
    x = np.asarray(x).swapaxes(axis, 0)
    x = x[::-1, ...]
    x = x.swapaxes(0, axis)
    return x


def resize_image(image, shape):
    return imresize(image, shape, interp='lanczos')


def resize_and_crop_image(image, shape):
    if image.shape == shape:
        return image
    rows, cols, _ = image.shape
    rows_n, cols_n, _ = shape
    resize_fraction = float(max(rows_n/rows, cols_n/cols))
    res = imresize(image, resize_fraction, interp='bicubic')
    d_rows, d_cols = res.shape[0] - rows_n, res.shape[1] - cols_n
    if d_rows == 0:
        s = int(d_cols/2)
        r = d_cols - s
        return res[:, s: -r, :]
    elif d_cols == 0:
        # choose to return the lower part of the picture
        # TODO: generalize this behavior?
        #s = int(d_rows / 2)
        #r = d_rows - s
        return res[d_rows:, :, :]
    else:
        assert False


class PreprocessedSequenceGenerator:
    def __init__(self, batch_generator,
                 to_scaled_floats=False,
                 scaling_factor=SCALING_FACTOR,
                 resize=False,
                 flip_horizontal=False,
                 flip_vertical=False,
                 flip_sequence=False):
        self.__dict__.update(locals())
        self._generator = batch_generator
        # Assume dimension ordering: [(batch,) frame, row, column, channel]
        # these indices are counted excluding (!) the batch dimension
        self.img_frame_index = 0
        self.img_row_index = 1
        self.img_col_index = 2

    def flow(self, prob=0.5):
        for batch, labels in self._generator:
            # these transforms can be performed on the whole batch
            transf_batch, transf_labels = self._transform(batch, labels)

            # iterate over data in batch for random transforms
            for i in range(transf_batch.shape[0]):
                transf_batch[i, ...], transf_labels[i, ...] =\
                    self._random_transform(transf_batch[i, ...], transf_labels[i, ...], prob)
            yield transf_batch, transf_labels

    def _transform(self, batch, labels):
        if self.resize is not False:
            transformed = np.empty((batch.shape[0], batch.shape[1]) + self.resize, batch.dtype)
            for i in np.ndindex(batch.shape[0], batch.shape[1]):
                transformed[i + (Ellipsis,)] = resize_and_crop_image(batch[i + (Ellipsis,)], self.resize)
        else:
            transformed = batch
        if self.to_scaled_floats:
            transformed = convert_to_scaled_floats(transformed)

        # Todo: Scale down labels
        labels *= self.scaling_factor
        return transformed, labels

    def _random_transform(self, data, label, prob):
        if self.flip_horizontal:
            if np.random.random() < prob:
                data = flip_axis(data, self.img_col_index)
        if self.flip_vertical:
            if np.random.random() < prob:
                data = flip_axis(data, self.img_row_index)
        if self.flip_sequence:
            if np.random.random() < prob:
                data = flip_axis(data, self.img_frame_index)
                label = -label
        return data, label
