from __future__ import absolute_import

from six import with_metaclass
from abc import ABCMeta, abstractmethod

import bisect
import numpy as np


class Source(with_metaclass(ABCMeta)):
    """Abstract base class
    """

    def __init__(self, name=u"UnnamedSource", **kwargs):
        self.name = name
        # These properties should have been set
        # by the child class, as appropriate.
        if not hasattr(self, 'seekable'):
            self.seekable = False
        if not hasattr(self, 'parallel_possible'):
            self.parallel_possible = False
        if not hasattr(self, 'cached'):
            self.cached = False
        # Shape can vary
        if not hasattr(self, '_shape'):
            self._shape = None

    def get_data(self):
        return self._get_data_impl()

    @abstractmethod
    def _get_data_impl(self):
        pass

    @abstractmethod
    def advance(self):
        pass

    @property
    @abstractmethod
    def dtype(self):
        pass

    @property
    def shape(self):
        """Get shape of returned data

        :return: Tuple describing shape. None if shape varies.
        """
        return self._shape

    @property
    def size(self):
        if self.seekable:
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
        self._cache = None
        self.seekable = True
        super(SeekableSource, self).__init__(**kwargs)
        self.position = None

    def seek(self, position):
        if position >= self.size:
            return False
        self._cache = self._get_data_at(position)
        self.position = position
        return True

    def advance(self):
        if self.position is None:
            p = 0
        else:
            p = self.position + 1
        return self.seek(p)

    def _get_data_impl(self):
        return self._cache

    @abstractmethod
    def _get_data_at(self, position):
        pass


class MergeSource(SeekableSource):
    """
    """

    def __init__(self, sources, **kwargs):
        self.sources = sources
        self.cached = True
        self.parallel_possible = True
        self._size = sources[0].size
        name = ""
        for source in self.sources:
            if not source.seekable:
                raise RuntimeError("Can only merge seekable sources.")
            if not source.cached:
                self.cached = False
            if not source.parallel_possible:
                self.parallel_possible = False
            if source.size < self._size:
                self._size = source.size
            name += source.name

        self._shape = tuple(s.shape for s in self.sources)
        self._dtype = tuple(s.dtype for s in self.sources)
        super(MergeSource, self).__init__(name=name, **kwargs)

    def _get_data_at(self, position):
        for s in self.sources:
            s.seek(position)
        return tuple(s.get_data() for s in self.sources)

    @property
    def dtype(self):
        return self._dtype


class ConcatenateSource(SeekableSource):
    """
    """

    def __init__(self, sources, **kwargs):
        self.sources = sources
        self.position_resolver = []

        position = 0
        self._shape = self.sources[0].shape
        self._dtype = self.sources[0].dtype
        self.cached = True
        self.parallel_possible = True
        for source in self.sources:
            if not source.seekable:
                raise RuntimeError("Can only merge seekable sources.")
            if not source.cached:
                self.cached = False
            if not source.parallel_possible:
                self.parallel_possible = False
            if self._shape != source.shape:
                self._shape = None
            if self._dtype != source.dtype:
                self._dtype = None
            position += source.size
            self.position_resolver.append(position)

        self._size = position
        super(ConcatenateSource, self).__init__(**kwargs)

    def _get_data_at(self, position):
        source_index = bisect.bisect(self.position_resolver, position)
        if source_index == len(self.position_resolver):
            raise RuntimeError("Invalid position")
        if source_index > 0:
            position -= self.position_resolver[source_index-1]
        s = self.sources[source_index]
        s.seek(position)
        return s.get_data()

    @property
    def dtype(self):
        return self._dtype


class LabeledDataSource(MergeSource):
    """This is a MergeSource with two inputs.

    First is interpreted as data, second as label.
    """

    def __init__(self, data_source, label_source, **kwargs):
        super(LabeledDataSource, self).__init__([data_source, label_source], **kwargs)


class VStackSource(SeekableSource):
    """Stack data from source 'vertically'

    """

    def __init__(self, source, dim_size, **kwargs):
        self._source = source
        # Todo: handle sources returning tuples
        if not self._source.has_fixed_shape():
            raise RuntimeError(u"Cannot stack sources without fixed data size.")
        if self._source.dtype is None:
            raise RuntimeError(u"Cannot stack sources without fixed data type.")
        self._shape = (dim_size,) + self._source.shape
        self._dtype = self._source.dtype
        self._dim_size = dim_size
        self._size = max(source.size - dim_size + 1, 0)

        self.cached = source.cached
        self.parallel_possible = source.parallel_possible
        super(VStackSource, self).__init__(name=u"vstacked {}".format(self._source.name), **kwargs)

    def _get_data_at(self, position):
        arr = np.empty(shape=self._shape, dtype=self._dtype)
        for i in range(self._dim_size):
            self._source.seek(position + i)
            arr[i, ...] = self._source.get_data()
        return arr

    @property
    def dtype(self):
        return self._dtype
