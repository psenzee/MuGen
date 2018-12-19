#!/usr/local/bin/python3
# coding=utf-8

import random
import copy
from Chord import Chord
from Event import Event
from SequenceInfo import SequenceInfo
from MusicUtils import *
from Utils import *
from PostMelodyTransform import *
from PostInvertTransform import *
from InstrumentRoles import *

class Sequence (object):

  def __init__(self, text = None):
    self.events = []
    self.chords = []
    self.infos = []
    self.templates = []
    self.resolved_events = []
    self.max_duration = 0
    self.min_time = 1000000
    self.max_time = 0
    self.max_event = None
    self.min_event = None
    if text != None:
      self.parse(text)

  def copy(self):
    s = Sequence()
    s.events = copy.deepcopy(self.events)
    s.chords = copy.deepcopy(self.chords)
    s.infos = copy.deepcopy(self.infos)
    s.templates = copy.deepcopy(self.templates)
    s.resolved_events = copy.deepcopy(self.resolved_events)
    s.max_duration = self.duration()
    return s

  def info(self):
    duration = -1
    for i in self.infos:
      if i != None and i.duration != None and i.duration > duration:
        duration = i.duration
    if duration != -1:
      si = SequenceInfo()
      si.duration = duration
      return si
    return None

  def duration(self):
    max = -1
    for i in self.infos:
      if i != None and i.duration != None and i.duration > max:
        max = i.duration
    for e in self.events:
      if e.time < self.min_time:
        self.min_time = e.time
        self.min_event = e
      if e.time + e.duration > self.max_time:
        self.max_time = e.time + e.duration
        self.max_event = e
    self.max_duration = self.max_time
    return self.max_duration
    
  def parse(self, text):
    self.events = []
    symbols = split_event_symbols(text)
    for symbol in symbols:
      if symbol.startswith('-'):
        self._add_info(symbol[len('-'):])
      else:
        self._add_symbol(symbol)
        
  def resolved(self, map):
    s = self.copy()
    s.events = [e.resolved_event(map, 60, False) for e in self.events]
    return s

  def format(self, resolve_map = None, include_info = True):
    info = []
    this_info = self.info()
    if include_info and this_info:
      info = ["-%s" % this_info.format()]
    formatted = [e.format() for e in self.events]
    if resolve_map != None:
      formatted = [e.resolve_event(resolve_map).format() for e in self.events]
    return " ".join(info + formatted)
    
  def format_resolved(self, include_info = True):
    info = []
    this_info = self.info()
    if include_info and this_info:
      info = ["-%s" % this_info.format()]
    formatted = [e.format() for e in self.resolved_events]
    return " ".join(info + formatted)
    
  def stretch(self, factor):
    infos = []
    for i in self.infos:
      i.stretch(factor)
      infos.append(i)
    self.infos = infos
    events = []
    for e in self.events:
      e.stretch(factor)
      events.append(e)
    self.events = events
    return self
    
  def shift(self, offset):
    events = []
    for e in self.events:
      e.shift(offset)
    events.append(e)
    self.events = events
    return self

  def to_chords(self, map, root = 60, time = 0):
    symbols = []
    for e in self.events:
      symbol = e.chord_symbol(map)
      symbols.append(symbol)
      c = e.chord(map, root, time)
      self.chords.append(c)
      e = e.resolved_event(map, False)
      e.add_time(time)
      self.resolved_events.append(e)
    #print("SYMS ", symbols)
    return self.chords

  def transform(self, transformer):
    events = []
    for e in self.events:
      events.extend(transformer.transform(e))
    self.events = events
    return self

  def _post_transform(self, arrangement):
    transforms = [PostMelodyTransform(arrangement)]#, PostInvertTransform()]
    events = [e.normalize() for e in self.resolved_events]
    for t in transforms:
      events = t.transform(events)
    return events
    
  def _center_note(self, events, channel):
    sum = 0.00
    count = 0
    for e in events:
      if e.channel == channel and e.midinotes:
        for n in e.midinotes:
          if n != None:
            sum += n
            count += 1
    if count == 0:
      return None
    return sum / count
    
  def get_channel_centers(self):
    centers = []
    for i in range(0, 16):
       if i in [LOCAL_CHANNEL_DRUMS, LOCAL_CHANNEL_BASS]:
         centers.append(None)
       else:
         centers.append(self._center_note(self.events, i))
    return centers

  def write(self, midi, arrangement):
    print("SEQUENCE: " + self.format())
    self.events = self._post_transform(arrangement)
    centers = self.get_channel_centers()
    for e in self.events:
      e.write(midi, centers)
    return None
    
  @staticmethod
  def retime(text, time, multiplier = 1, max = 64):
    for i in range(0, max):
      text = text.replace(":T%d:" % i, ":~^&*%d:" % i)
    for i in range(0, max):
      text = text.replace(":~^&*%d:" % i, ":T%d:" % (time + int(i * multiplier)))
    return text
    
  # private
  def _normalize(self, clean = False):
    events = self.events
    if clean:
      events = Events.clean_all(events)
    sorted(events, key=lambda x: x.time)
    self.events = events
    return self
    
  def _add_symbol(self, text):
    e = Event()
    e = e.parse(text)
    if e != None and e.is_valid():
      self.events.append(e)
      return e
    return None
    
  def _add_info(self, text):
    i = SequenceInfo()
    i = i.parse(text)
    if i and i.is_valid():
      self.infos.append(i)
      return i
    return None

# -------------------------------------------------------------------------------------

def _test_sequence():
  template = """
-D16 C:T0:D4:o-1 C:T0:D2:o+1 E:T0:D2:o+1 G:T2:D2:o+1 G:T4:D4:o-1 C:T4:D2:o+1 E:T4:D2:o+1
b:T6:D4:o+1 D:T6:D4:o+1 b:T8:D4:o-1 G:T10:D2:o+1 b:T12:D4:o+1 D:T12:D4:o+1 G:T14:D2:o+1
G:T12:D4:o-1
"""
  rt = Sequence2()
  rt.parse(template)
  print (rt.format())
  map = { 'b' : '10-', 'C' : 0, 'D' : 2, 'E' : 4, 'G' : '7-' }
  rt.to_chords(map)
  print ("done")

if __name__ == '__main__':
  _test_sequence()