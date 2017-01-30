from __future__ import absolute_import

from six import with_metaclass
from abc import ABCMeta, abstractmethod


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


class Sink(with_metaclass(ABCMeta)):
    """Abstract base class for all sinks."""

    def __init__(self, name=u"UnnamedSink", **kwargs):
        self.name = name

    @abstractmethod
    def set_data(self, data):
        pass
