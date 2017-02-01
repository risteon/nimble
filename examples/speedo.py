from __future__ import print_function

from nimble.sources import IntegerSource
from nimble.filters import Speedometer
from nimble.sinks import ImageVideoSink


def main():

    ints = IntegerSource(start=0, stop=101)
    speedo = Speedometer(0.0, 100.0)
    sink = ImageVideoSink(fps=20)

    while ints.advance():
        sink.set_data(speedo.filter(ints.get_data()))

    sink.write(filename=u"/tmp/nimble_speedo.mp4")

if __name__ == "__main__":
    main()
