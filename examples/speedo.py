from __future__ import print_function

from nimble.graph import Pipeline

from nimble.sources import IntegerSource
from nimble.filters import Speedometer
from nimble.sinks import ImageVideoSink


def main():

    pipeline = Pipeline()

    pipeline.add(IntegerSource(start=0, stop=101))
    pipeline.add(Speedometer(0.0, 100.0))
    pipeline.add(ImageVideoSink(filename=u"/tmp/nimble_speedo.mp4", fps=20))

    pipeline.run()


if __name__ == "__main__":
    main()
