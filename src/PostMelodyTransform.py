#!/usr/local/bin/python3
# coding=utf-8

import random
from Event import *
from Transforms import *
from Utils import *
from DurationPercents import DurationPercents

class PostMelodyTransform (Transform):

  def __init__(self, arrangement):
    super().__init__()
    self.arrangement = arrangement
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
    self._motion = self._generate_motion_patterns(random.randint(4, 40))
    # set up
    self._index_options = None
    self._should_post_transform = {}

  def _generate_motion_patterns(self, length):
    index = 0
    last = 0
    patterns = ['0']
    pos = ['0', '1', '2', '3', '4']
    neg = ['4', '3', '2', '1', '0']
    for i in range(0, length):
      index = last + random.choice([-1, 1])
      if index < 0:
        k = neg[int(-index / 3) % len(neg)]
        mstr = str(k)
        for j in range(0, -index % 3):
          mstr = mstr + '♭'
      else:
        k = pos[int(index / 3) % len(pos)]
        mstr = str(k)
        for j in range(0, index % 3):
          mstr = mstr + '♯'
      patterns.append(mstr)
      last = index
    return patterns

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

  def _get_should_post_transform(self, event):
    return self.arrangement.get_channel_should_post_transform(event.channel)
  
  def _process(self, events):
    copy = []
    index = None
    #print ("HOW MANY EVENTS %d" % len(events))
    count = 0
    for e in events:
      if not self._get_should_post_transform(e):
        copy.append(e)
        continue
      e.index = "" + self._motion[count % len(self._motion)]
      e.normalize()
      copy.append(e)
      index = e.index
      count = count + 1
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