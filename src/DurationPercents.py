#!/usr/local/bin/python3
# coding=utf-8

from MusicUtils import *
from Utils import *
from DurationValues import DurationValues

class DurationPercents (DurationValues):

  def __init__(self, table = None):
    if table == None:
      table = {
        16 : 50.0,
         8 : 50.0,
         4 : 50.0,
         2 : 50.0,
         1 : 50.0
      }
    super().__init__(table)
    self._overall = 100

  def set_overall(self, percent):
    self._overall = float(percent)
    return self

  def set_default(self, percent):
    return super().set_default(float(percent))

  def set_percent(self, duration, percent):
    return self.set_value(self, duration, float(percent))

  def percent(self, duration):
    return float(self.value(duration))
    
  def choose(self, duration):
    return is_percent(self.percent(duration) * (float(self._overall) / 100.0))