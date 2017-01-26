from __future__ import division
from builtins import range

import numpy as np


def make_image_grid(data, nb_rows=None, nb_cols=None, has_channels=True):
    """

    """
    if has_channels:
        nb_res_channels = 3
    else:
        nb_res_channels = 2

    if len(data.shape) < nb_res_channels:
        raise RuntimeError("Invalid data array.")
    # flatten out the all dimensions before the actual images
    data_shaped = np.reshape(data, (-1,) + data.shape[-nb_res_channels:])
    # Calculate number of rows and cols in mosaic
    nb_data = data_shaped.shape[0]
    if nb_cols is None or nb_rows is None:
        if nb_cols is None and nb_rows is None:
            nb_cols = 1
        if nb_cols is None:
            nb_cols = (nb_data + nb_rows - 1)//nb_rows
        elif nb_rows is None:
            nb_rows = (nb_data + nb_cols - 1)//nb_cols
    # Create empty target array with correct dimensions
    height = data.shape[len(data.shape) - nb_res_channels]
    width = data.shape[len(data.shape) - nb_res_channels + 1]
    if has_channels:
        shape = (nb_rows * height, nb_cols * width, data.shape[-1])
    else:
        shape = (nb_rows * height, nb_cols * width)
    mosaic = np.empty(shape, dtype=data.dtype)
    # paste all images into mosaic
    for r in range(nb_rows):
        for c in range(nb_cols):
            mosaic[r*height:(r+1)*height, c*width:(c+1)*width, ...] = data_shaped[r*nb_cols+c]

    return mosaic
