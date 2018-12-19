#!/usr/local/bin/python3
# coding=utf-8

import random

from BaseEvent import *
from Event import Event
from Transforms import *
from Utils import *

from DurationValues import DurationValues
from DurationPercents import DurationPercents

class SplitTransform (Transform):

  def __init__(self, overall_percent = 100):
    super().__init__()

    # splits by duration
    self.splits = DurationPercents({
      16 : 90,
       8 : 80,
       4 : 50,
#       2 : 10,
       2 : 50,
       1 :  0
    }).set_default(0).set_overall(overall_percent)

    # triplets by duration
    self.triplets = DurationPercents({
      16 : 10,
       8 :  7,
       4 :  5,
       2 :  0,
       1 :  0
    }).set_default(0).set_overall(100)

    self.triplet_subdivide = 0
    
    # distribution by duration
    self.distributions = DurationValues({
      16 : EVENT_SPLIT2_DIV4_TYPES, #EVENT_SPLIT2_ALL_TYPES,
       8 : EVENT_SPLIT2_DIV4_TYPES,
       4 : [EVENT_SPLIT2_50_50],
       2 : [EVENT_SPLIT2_50_50],
       1 : [EVENT_SPLIT2_50_50]
    }).set_default([EVENT_SPLIT2_50_50])

    # swaps by duration
    self.swaps = DurationPercents({
      16 :  0,
       8 : 10,
       4 : 20,
       2 : 40,
       1 : 50
    }).set_default(0).set_overall(50)
    
  def set_overall_split_percent(self, percent):
    self.splits.set_overall(percent)
    return self
    
  def set_overall_swap_percent(self, percent):
    self.swaps.set_overall(percent)
    return self

  def transform(self, events):
    return self._split(events)

  # private methods
  def _split(self, events):
    xf = []
    for event in events:
      if not self.splits.choose(event.duration):
        xf.append(event)
      elif not self.triplets.choose(event.duration):
        (a, b) = event.bisect(random.choice(self.distributions.value(event.duration)))
        if self.swaps.choose(event.duration):
          #print ("SWAPPING")
          (y, x) = (a, b)
        else:
          (x, y) = (a, b)
        xf.extend(self._split([x]))
        xf.extend(self._split([y]))
      else:
        (a, b, c) = event.trisect()
        if self.triplet_subdivide:
          xf.extend(self._split([a]))
          xf.extend(self._split([b]))
          xf.extend(self._split([c]))
        else:
          xf.extend([a, b, c])
    return xf