from __future__ import print_function

import sys
from scipy import misc

from nimble.sources import KittiOdometrySource


def main():

    if len(sys.argv) < 2:
        print("Specify the Kitti dataset root folder as argument")
        return

    kitti_data = KittiOdometrySource(sys.argv[1], 3)
    kitti_data.advance()
    kitti_data.seek(42)     # only for seekable sources
    data, label = kitti_data.get_data()

    # print transform matrix
    print("Transform: ")
    print(label)
    # show image
    misc.imshow(data)


if __name__ == "__main__":
    main()
