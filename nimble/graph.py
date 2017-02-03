# -*- coding: utf-8 -*-
from __future__ import absolute_import

from abc import abstractmethod

from .core import DataSpec, Filter, Source, Sink, ControllingSink, MasterSinkWrapper
from .streaming import Stream


class FlowGraph(Filter):
    """"""

    def __init__(self, **kwargs):
        super(FlowGraph, self).__init__(**kwargs)
        self._source = None
        self._master_sink = None
        self._stream = None
        #
        self._assembled = False

    def run(self):
        """"""
        if not self._assembled:
            self.assemble()

        self._master_sink.run(self._stream)

    def assemble(self):
        self._assemble_impl()
        self._assembled = True

    def filter(self, data):
        """"""
        # Todo: filtering may be difficult on arbitrary flow graphs
        if not self._assembled:
            raise RuntimeError("Must first assemble Graph.")
        return self._stream.filter(data)

    @abstractmethod
    def _assemble_impl(self):
        pass


class Network(FlowGraph):
    """"""

    def __init__(self, input_stream, output_stream, **kwargs):
        super(Network, self).__init__(**kwargs)
        self._input = input_stream
        self._output = output_stream


class Pipeline(FlowGraph):
    """"""

    def __init__(self, **kwargs):
        super(Pipeline, self).__init__(**kwargs)
        self._filters = []

    def add_filter(self, filter):
        self._filters.append(filter)

    def set_source(self, source):
        self._source = source

    def set_sink(self, sink):
        self._master_sink = sink

    def add(self, nimble_object):
        if isinstance(nimble_object, Source):
            if not self._source and not self._filters:
                self.set_source(nimble_object)
            else:
                raise ValueError("You can only add a source at the beginning")
        elif isinstance(nimble_object, Sink):
            if self._source:
                self.set_sink(nimble_object)
            else:
                raise ValueError("You can only add a sink after a source or filter")
        elif isinstance(nimble_object, Filter):
            if self._source and not self._master_sink:
                self.add_filter(nimble_object)
            else:
                ValueError("You can only add a filter after a source and before adding a sink.")
        else:
            raise ValueError("Unknown object.")

    def _assemble_impl(self):
        if self._source:
            s = Stream.from_sources(self._source)
        else:
            s = Stream(DataSpec())

        for f in self._filters:
            s = f(s)

        self._stream = s
        if self._master_sink and not isinstance(self._master_sink, ControllingSink):
            self._master_sink = MasterSinkWrapper(self._master_sink)
