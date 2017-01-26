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


class SeekableSource(Source):
    def __init__(self, **kwargs):
        self._cache = None
        self.seekable = True
        super(SeekableSource, self).__init__(**kwargs)
        self.position = None

    def seek(self, position):
        if position >= self.size:
            return False
        self._cache = self.get_data_at(position)
        return True

    def advance(self):
        if self.position is None:
            self.position = 0
        else:
            self.position += 1
        return self.seek(self.position)

    def _get_data_impl(self):
        return self._cache


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
        super(MergeSource, self).__init__(name=name, **kwargs)

    def get_data_at(self, position):
        return tuple(s.get_data_at(position) for s in self.sources)


class LabeledDataSource(MergeSource):
    """This is a MergeSource with two inputs.

    First is interpreted as data, second as label.
    """

    def __init__(self, data_source, label_source, **kwargs):
        super(LabeledDataSource, self).__init__([data_source, label_source], **kwargs)
