# -*- coding: utf-8 -*-
from __future__ import absolute_import

import numpy as np

from .core import DataSpec, Source, Filter


class Stream(Source):
    def __init__(self, data_spec):
        super(Stream, self).__init__()
        self._inputs = tuple()
        self._data_spec = data_spec
        self._operation = None
        self._source_stream = False

    @classmethod
    def from_sources(cls, sources):
        self = cls(DataSpec)
        self._source_stream = True
        if isinstance(sources, tuple):
            self._inputs = sources
        else:
            self._inputs = sources,
            self._size = sources.size
            self._seekable = sources.seekable
        return self

    @classmethod
    def from_filtered_stream(cls, inputs, op=Filter()):
        # Todo: read data spec from input
        self = cls(DataSpec())
        self._operation = op

        if isinstance(inputs, tuple):
            self._inputs = inputs
            self._source_stream = True
            for i in inputs:
                if not i._source_stream:
                    self._source_stream = False
        else:
            self._inputs = inputs,
            self._size = inputs.size
            self._seekable = inputs.seekable
            self._source_stream = inputs._source_stream
        return self

    def apply_filter(self, op):
        return Stream.from_filtered_stream(self, op=op)

    def is_source_stream(self):
        return bool(self._source_stream)

    def advance(self):
        for inp in self._inputs:
            inp.advance()
        self._data_impl()

    def seek(self, position):
        """A stream may be seekable."""

        try:
            for inp in self._inputs:
                inp.seek(position)
            self._data_impl()

        except AttributeError:
            print(u"This stream is not seekable, because it is not connected to a seeakble source.")
            raise

    def _data_impl(self):
        if len(self._inputs) > 1:
            self._data = tuple(inp.get_data() for inp in self._inputs)
        else:
            self._data = self._inputs[0].get_data()

        if self._operation:
            self._data = self._operation.filter(self._data)
