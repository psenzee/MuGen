#!/usr/local/bin/python3
# coding=utf-8

import math
import random
from Transforms import Transform
from Event import Event
from Generators import Generator
from MusicUtils import *

class TemplateGenerator (Generator):

  def __init__(self, transform, templates, label_count = 2, period = 2, octave = 0):
    super().__init__()
    self._pattern = [None] * period
    self._labels = ['X', 'Y', 'Z', 'W'][:label_count]
    self._period = period
    self._state = 0
    self._transform = transform
    self._templates = templates
    self._octave = octave
    self._name = None

  def set_name(self, name):
    self._name = name
    return self

  def labels(self):
    return self._labels
    
  def duration(self):
    return 16

  def template(self):
    return self._templates[self._state % len(self._templates)]

  def next(self):
    formatted = []
    n = self._state
    if self._period:
      n = self._state % self._period
    if self._period and self._pattern[n] != None:
      formatted = self._pattern[n]
    else:
      t = self.template()
      for p in split_event_symbols(t):
        o = octave_str(self._octave)
        transformed = self._transform.transform([Event().parse(p + o)])
        formatted.append(Event.format_all(transformed))
    if self._period and self._pattern[n] == None:
      self._pattern[n] = formatted
    self._state = self._state + 1
    formatted = (" -D%d " % self.duration()) + ' '.join(formatted) + ' | '
    if self._name != None:
      print("TEMPLATE: %s" % self._name)
#   print ("FORMATTED " + formatted)
    return formatted
    
class RandomTemplateGenerator (TemplateGenerator):

  def template(self):
    return random.choice(self._templates)
