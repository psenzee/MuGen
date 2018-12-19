#!/usr/local/bin/python3
# coding=utf-8

import random
import copy
import math
import Midi
from Chord import Chord
import Utils
import Swinger

EVENT_SPLIT2_25_75 = 0.25
EVENT_SPLIT2_33_67 = 0.3333333
EVENT_SPLIT2_50_50 = 0.50
EVENT_SPLIT2_67_33 = 0.6666666
EVENT_SPLIT2_75_25 = 0.75
EVENT_SPLIT2_DIV3_TYPES = [EVENT_SPLIT2_33_67, EVENT_SPLIT2_67_33]
EVENT_SPLIT2_DIV4_TYPES = [EVENT_SPLIT2_25_75, EVENT_SPLIT2_50_50, EVENT_SPLIT2_75_25]
EVENT_SPLIT2_ALL_TYPES = EVENT_SPLIT2_DIV4_TYPES + EVENT_SPLIT2_DIV3_TYPES

class BaseEvent (object):

  def __init__(self, name = None, midinotes = [], time = 0, duration = 4, volume = 100, channel = 0, root = 60):
    self._initialize()
    self.name = name
    self.time = time
    self.channel = channel
    self.duration = duration
    self.volume = volume
    self.root = root
    self.midinotes = midinotes
    
  def copy(self):
    return BaseEvent(self.name, self.midinotes[:], self.time, self.duration, self.volume, self.channel, self.root)

  def is_valid(self):
    return not None in [self.time, self.duration, self.volume, self.channel]
    
  # turn a higher level value into a lower-level representation
  def normalize(self):
    return self

  def parse(self, text):
    # format: <name>:T<time in 16ths>:D<duration in 16ths = 4>:v<volume 0-100 = 100>:[<comma separated list of notes]
    self._initialize()
    pieces = text.strip().split(':')
    if len(pieces) == 0:
      return None
    if pieces[0] == '#':
      return None # comment
    self.parse_name(pieces[0])
    for p in pieces:
      self.parse_arguments(p)
    return self

  def parse_arguments(self, text):
    value = BaseEvent.parse_op_int_array('[', text)
    if value != None: self.midinotes = value
    value = BaseEvent.parse_op_int('c', text)
    if value != None: self.channel = value
    value = BaseEvent.parse_op_float('T', text)
    if value != None: self.time = value
    value = BaseEvent.parse_op_float('D', text)
    if value != None: self.duration = value
    value = BaseEvent.parse_op_int('v', text)
    if value != None: self.volume = value
    value = BaseEvent.parse_op_int('r', text)
    if value != None: self.root = value
    return self

  def stretch(self, factor):
    self.time = float(self.time * factor)
    self.duration = float(self.duration * factor)
    return self
    
  def shift(self, offset):
    self.time = self.time + float(offset)
    return self
    
  def bisect(self, factor = EVENT_SPLIT2_50_50):
    (a, b) = (self.copy(), self.copy())
    duration = float(a.duration * factor)
    a.duration = duration
    b.duration = b.duration - a.duration
    b.time = a.time + a.duration
    return [a, b]
    
  def trisect(self):
    (a, b, c) = (self.copy(), self.copy(), self.copy())
    a.duration = b.duration = (a.duration / 3.0)
    b.time = a.time + a.duration
    c.time = b.time + b.duration
    c.duration = c.duration - (a.duration + b.duration)
    return [a, b, c]

  def clean(self):
    self.duration = self._clean_temporal_value(self.duration)
    self.time = self._clean_temporal_value(self.time)
    return self

  def parse_name(self, name):
    self.name = name
    return self
    
  def get_defaults(self):
    return {
      'T' : 0,
      'D' : 4,
      'v' : 100,
      'c' : 0,
      '[' : [],
      'r' : 60
    }

  def format(self, additional_map = None):
    name = self.format_name()
    duration = float(int(self.duration * 4.0 + 0.5)) * 0.25
    time = float(int(self.time * 4.0 + 0.5)) * 0.25
    keys = ['T', 'D', 'v', 'c', '[', 'r']
    map = {
      'T' : BaseEvent.format_temporal_value(time),
      'D' : BaseEvent.format_temporal_value(duration),
      'v' : self.volume,
      'c' : self.channel,
      '[' : self.format_midinotes(),
      'r' : self.root
    }
    if additional_map != None:
      keys.extend(additional_map.keys())
      map.update(additional_map)
    defaults = self.get_defaults()
    parts = [name]
    for key in keys:
      value = map[key]
      default = defaults[key]
      if value == '':
        value = None
      if value != None and value != default:
        parts.append(key + "%s" % (value,))
    formatted = ':'.join(parts)
    return formatted

  def _initialize(self):
    self.name = None
    self.time = 0
    self.duration = 4
    self.volume = 100
    self.channel = 0
    self.midinotes = []
    self.defaults = {
      'T' : 0,
      'D' : 4,
      'v' : 100,
      'c' : 0,
      '[' : [],
      'r' : 60
    }

  def format_name(self):
    name = self.name
    if name == None:
      name = ''
    return name

  def format_midinotes(self):
    if self.midinotes is None:
      return ''
    return ','.join(["%d" % int(n) for n in self.midinotes])

  def parse_all(self, text):
    items = text.split(' ')
    results = []
    for item in items:
      item = item.strip()
      e = self.copy().parse(item)
      if e != None:
        results.append(e)
    return results
    
  def get_final_notes(self):
    return self.midinotes
    
  def _final_post_transform_note(self, n, centers):
    if centers == None or self.channel >= len(centers):
      return n
    center = centers[self.channel]
    if center != None:
      (a,  b,  c)  = (n, n - 12, n + 12)
      (ac, bc, cc) = (math.fabs(a - center), math.fabs(b - center), math.fabs(c - center))
      minabc = min(ac, bc, cc)
      if minabc == ac:
        return a
      if minabc == bc:
        return b
      if minabc == cc:
        return c
    return n
    
  def write(self, midi, centers = None):
    self.normalize()
    notes = self.get_final_notes()
    if notes == None or len(notes) == 0:
      return self
    for n in notes:
      t = Swinger.swing(self.time)
      #print ("time before swing: %.2f after: %.2f" % (self.time, t))
      midi.write_note(self.channel, self._final_post_transform_note(n, centers) + self.root, t, self.duration, self.volume)
    return self

  def add_time(self, time):
    self.time = self.time + time
    return self

  @staticmethod
  def format_all(events):
    return ' '.join([e.format() for e in events])

  @staticmethod
  def clean_all(events):
    events = [x.clean() for x in events]
    return sorted(events, key=lambda x: x.time)
    
  # private methods
  @staticmethod
  def parse_op_value(op, text):
    if text.startswith(op):
      return text[len(op):]
    return None

  @staticmethod
  def parse_op_int(op, text):
    value = BaseEvent.parse_op_float(op, text)
    if value == None:
      return None
    return int(math.floor(value + 0.5))
    
  @staticmethod
  def parse_op_float(op, text):
    value = BaseEvent.parse_op_value(op, text)
    if value == None or len(value) == 0:
      return None
    return float(value)
    
  @staticmethod
  def parse_op_array(op, text):
    value = BaseEvent.parse_op_value(op, text)
    if value == None:
      return None
    return value.split(',')

  @staticmethod
  def parse_op_int_array(op, text):
    values = BaseEvent.parse_op_array(op, text)
    if values == None:
      return None
    return [int(v) for v in values if len(v) > 0]

  @staticmethod
  def _clean_temporal_value(value):
    value = float(int(value * 4.0 + 0.5)) * 0.25
    if int(value) == int(value + 0.999):
      value = int(value)
    return value
    
  @staticmethod
  def format_temporal_value(value):
    value = BaseEvent._clean_temporal_value(value)
    if value == int(value):
      return "%d" % int(value)
    return "%.2f" % float(value)
    
def _test_base_events():
  spec = ":[0,4,7:T0:D4:c1:r60 :[0:T4.2:D4:r60 :[0,4,7:T0:D4:c2:r60 :[0:T4.2:D4:c3:r60 "
  #spec = ":[60:T4:D4:c1"
  events = BaseEvent().parse_all(spec)
  #print (BaseEvent.format_all(events))
  midi = Midi.Midi()
  midi.open('miditest')
  newlist = []
  for e in events:
    newlist.extend(e.bisect())
  events = newlist
  for e in events:
    e.write(midi)
  print (BaseEvent.format_all(events))
  midi.close()

if __name__ == '__main__':
  _test_base_events()
