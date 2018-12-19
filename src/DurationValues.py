#!/usr/local/bin/python3
# coding=utf-8

from MusicUtils import *

class DurationValues (object):

  def __init__(self, table = None):
    super().__init__()
    self._table = {}
    if table:
      self._table = table
    self._default = None

  def set_default(self, value):
    self._default = value
    return self

  def set_value(self, duration, value):
    self._table[duration] = value
    return self

  def value(self, duration):
    return value_by_duration(duration, self._table, self._default)