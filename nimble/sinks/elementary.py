# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from ..core import Sink


class ConsoleSink(Sink):
    """This sink prints all data."""

    def __init__(self):
        super(ConsoleSink, self).__init__(name=u"ConsoleSink")

    def set_data(self, data):
        print(data)
