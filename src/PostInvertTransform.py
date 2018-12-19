#!/usr/local/bin/python3
# coding=utf-8

import random
from Event import *
from Transforms import *
from Utils import *

class PostInvertTransform (Transform):

  def __init__(self):
    pass

  def transform(self, events):
    events = [e.normalize() for e in events]
    center = self._center_note(events)
    for e in events:
      notes = []
      o = 0
      for n in e.midinotes:
        while n - center > 12:
          n -= 12
          o -= 1
        while n - center < -12:
          n += 12
          o += 1
        notes.append(n)
      e.octave += o
      e.midinotes = notes
    return events

  def _center_note(self, events):
    sum = 0.00
    count = 0
    for e in events:
      for n in e.midinotes:
        if n != None:
          sum += n
          count += 1
    return sum / count