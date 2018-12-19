#!/usr/local/bin/python3
# coding=utf-8

import random
from Event import *
from Transforms import *
from Utils import *
from DurationPercents import DurationPercents

class Melody2Transform (Transform):

  def __init__(self):
    super().__init__()
    self.base_indices = ['0', '1', '2', '3', '4']
  
    # default options
    self.set_use_altered(False)
    self.use_chords = False
    self.note_vs_chord_frequency = 1
    self.accidentals_for_durations_under = 16.0#1.0
    self.use_full_chords = DurationPercents({
      16 :  0,
       8 : 10,
       4 : 20,
       2 : 40,
       1 : 50
    }).set_default(0)

    # set up
    self._index_options = None

  def set_use_altered(self, use_altered):
    self._index_options = None
    self.index_options = self.base_indices * 4
    offsets = []
    if use_altered:
      offsets = ['1♭', '2♯']
    for i in self.base_indices:
      offsets.extend(['%s+1' % i, '%s-1' % i, '%s+2' % i, '%s-2' % i])
    self.index_options = self.index_options + offsets
    return self

  def set_use_accidentals_for_durations_under(self, value):
    self.accidentals_for_durations_under = value
    return self

  def set_use_chords(self, value):
    self.use_chords = value
    return self

  def transform(self, events):
    return self._process(events)

  # private methods
  def _options(self): 
    if self._index_options == None:
      options = ['0', '1', '2', '3', '4']
      copy = []
      for option in options:
        copy.append(option)
        copy.append(option + '♭')
        copy.append(option + '♯')
        copy.append(option + '♭♭')
        copy.append(option + '♯♯')
      random.shuffle(copy)
      self._index_options = copy
      self._index_options = options
    return self._index_options

  def _random_option(self):
    return random.choice(self._options())
  
  def _process(self, events):
    copy = []
    index = None
    #print ("HOW MANY EVENTS %d" % len(events))
    for e in events:
      if e.index == None:
        e.index = self._random_option()
      if index == None:
        index = e.index
      e.index = self._index_direction(index, e.duration, random.choice([1, -1]))
      copy.append(e)
      index = e.index
    return copy

  def _index_direction(self, index, duration, direction):
    if index == None or direction == 0:
      return index
    copy = []
    for i in index.split(','):
      if direction < 0:
        i = i + '♭'
      else:
        i = i + '♯'
      copy.append(i)
    return ','.join(copy)