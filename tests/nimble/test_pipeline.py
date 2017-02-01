# -*- coding: utf-8 -*-
import pytest

from nimble.core import Filter, Sink
from nimble.streaming import Stream
from nimble.graph import Pipeline
from nimble.sources import UniformRandomSource


def test_pipeline_basic():

    pipeline = Pipeline()

    pipeline.set_source(UniformRandomSource())
    pipeline.add_filter(Filter())
    pipeline.add_filter(Filter())
    pipeline.set_sink(Sink())

    pipeline.run()


if __name__ == '__main__':
    pytest.main([__file__])
