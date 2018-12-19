#!/usr/local/bin/python3
# coding=utf-8

import math
import random
import time
import os

from Chord import *
from Sequence import *
from Event import *
from Midi import *

FILE_PREFIX = "m"

class Track (object):
  
  def __init__(self, root = 60):
    self.initial_time = 0
    self.root = root
    self.volume = 100 # 127 is max
    self.tempo = 120
    self.template_text = None
    self.template = Sequence()
    self.duration = 0
    self.base_chords = None
    self.chord_id = None

  def open(self, channel_count):
    self.midi = Midi(channel_count).open()
    return self

  def set_dynamics(self, channel, period, overall = 1.0, offset = 0, min_max = (0, 127)):
    self.midi.set_dynamics(channel, period, overall, offset, min_max)
    return self

  def set_base_volume(self, volume):
    self.volume = volume
    return self
    
  def set_root(self, root):
    self.root = root
    return self
    
  def set_tempo(self, tempo):
    self.tempo = tempo
    return self

  def set_base_chords(self, chords):
    self.base_chords = chords
    self.chord_id = None
    if self.base_chords:
      self.chord_id = '-'.join([Chords.safe_symbol(x) for x in self.base_chords])
    # get this into the filename
    return self
    
  def add_chords_xyzw(self, chords):
    duration = self.template.duration()
    self.template.toChordsXYZW(chords, self.root, self.duration)
    self.duration = self.duration + duration
    return self

  def generate(self, generator, chords, times = 1):
    labels = generator.labels()
    duration = generator.duration()
    label_count = len(labels)
    for i in range(0, len(chords), label_count):
      template = generator.next()
      self.template_text = template
      self.template.parse(self.template_text)
      map = {}
      for j in range(0, len(labels)):
        if i + j >= len(chords):
          value = chords[-1]
        else:
          value = chords[i + j]
        map[labels[j]] = value
      s = self.template.resolved(map)
      self.template = s
      self.template.to_chords(map, self.root, self.duration)
      self.duration = self.duration + duration
    return self

  def flush(self):
    arrangement = self.midi.get_arrangement()
    self.template.write(self.midi, arrangement)
    self.template = Sequence()
    if self.template_text:
      self.template.parse(self.template_text)
    return self

  def save(self):
    self.flush()
    filename = '_'.join([FILE_PREFIX, self.chord_id])
    dir = "generated/%s" % self.chord_id
    if not os.path.isdir(dir):
      dir = "generated"
    self.midi.set_directory(dir)
    self.midi.set_filename(filename)
    self.midi.close()
