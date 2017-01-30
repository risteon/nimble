from __future__ import print_function

import numpy as np

from nimble.filters import Speedometer
from nimble.sinks import ImageDisplaySink


def main():

    speedo = Speedometer(0.0, 1.0)
    sp = speedo.filter(np.asarray([0.5]))

    # show image
    display = ImageDisplaySink()
    display.set_data(sp)


if __name__ == "__main__":
    main()
