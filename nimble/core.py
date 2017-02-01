# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from six import with_metaclass
from abc import ABCMeta, abstractmethod


class DataSpec:
    def __init__(self):
        self.dtype = None
        self.shape = None


class Source(with_metaclass(ABCMeta, object)):
    """Abstract base class
    """

    def __init__(self, name=u"UnnamedSource", **kwargs):
        self.name = name
        # These properties should have been set
        # by the child class, as appropriate.
        if not hasattr(self, 'seekable'):
            self._seekable = False
        if not hasattr(self, 'parallel_possible'):
            self.parallel_possible = False
        if not hasattr(self, 'cached'):
            self.cached = False

        # Shape can vary
        if not hasattr(self, '_shape'):
            self._shape = None
        # Data can vary
        if not hasattr(self, '_dtype'):
            self._dtype = None

        self._data = None

    def get_data(self):
        return self._data

    @abstractmethod
    def advance(self):
        pass

    @property
    def seekable(self):
        """"""

        return self._seekable

    @property
    def dtype(self):
        """Get type of returned data

        :return: data type. None if data can vary.
        """
        return self._dtype

    @property
    def shape(self):
        """Get shape of returned data

        :return: Tuple describing shape. None if shape varies.
        """
        return self._shape

    @property
    def size(self):
        if self._seekable:
            return self._size
        else:
            return None

    def has_fixed_shape(self):
        if self._shape is None:
            return False
        if isinstance(self._shape, tuple):
            return None not in self._shape
        return True


class SeekableSource(Source):
    def __init__(self, **kwargs):
        self._seekable = True
        super(SeekableSource, self).__init__(**kwargs)
        self.position = None

    def seek(self, position):
        if position >= self.size:
            return False
        self._data = self._get_data_at(position)
        self.position = position
        return True

    def advance(self):
        if self.position is None:
            p = 0
        else:
            p = self.position + 1
        return self.seek(p)

    @abstractmethod
    def _get_data_at(self, position):
        pass


class Sink(with_metaclass(ABCMeta, object)):
    """Abstract base class for all sinks."""

    def __init__(self, name=u"UnnamedSink", **kwargs):
        self.name = name
        # Arbitrary input shape
        if not hasattr(self, '_input_shape'):
            self._input_shape = None
        # Arbitrary input data
        if not hasattr(self, '_input_dtype'):
            self._input_dtype = None

    def __call__(self, stream):
        return stream.apply_filter(self)

    def set_data(self, data):
        pass

    def run_impl(self, stream):
        """Default implementation: exhaust stream and do nothing with data."""
        while stream.advance():
            self.set_data(stream.get_data())

    @property
    def input_dtype(self):
        return self._input_dtype

    @property
    def input_shape(self):
        return self._input_shape


class Filter(with_metaclass(ABCMeta, object)):
    """Abstract base class for all filters."""

    def __init__(self, name=u"UnnamedFilter", **kwargs):
        self._name = name
        self._cache_output = None

    def filter(self, data):
        """Default implementation: do nothing."""

        return data

    def __call__(self, stream):
        return stream.apply_filter(self)
