#!/usr/local/bin/python3
# coding=utf-8

import random
from Event import *
from Transforms import *
from Utils import *

def _append_to_index(index, suffix):
  if index == None:
    index = '0'
  if suffix is None or suffix == '':
    return index
  parts = index.split(',')
  copy = []
  for p in parts:
    if p in ['0', '1', '2', '3', '4', '*']:
      p = p + suffix
    copy.append(p)
  return ','.join(copy)

class OrnamentTransform (Transform):

  def __init__(self):
    super().__init__()
    self.min_target_note_duration = 4
    self.ornament_note_duration = 0.5
    self.start_volume = 0.25 #.0
    self.end_volume = 1.0
    self.before_note = False
    
  def set_min_target_note_duration(self, duration):
    self.min_target_note_duration = duration
    return self
    
  def set_note_duration(self, duration):
    self.ornament_note_duration = duration
    return self
    
  def set_before_note(self, before_note):
    self.before_note = before_note
    return self
    
  def get_directions(self):
    return ['`♭`♭', '`♭']

  def transform(self, events):
    copy = []
    dirs = self.get_directions()
    delta_volume = (self.end_volume - self.start_volume) / (len(dirs) + 1)
    total_duration = len(dirs) * self.ornament_note_duration
    if self.before_note:
      total_duration = 0
    for e in events:
      if e.duration >= max(self.min_target_note_duration, total_duration):
        if e.index != _append_to_index(e.index, '?'):
          index = e.index
          base_volume = e.volume
          e.time += total_duration
          e.duration -= total_duration
          c = e
          notes = []
          for i in range(0, len(dirs)):
            c = c.copy()
            c.index = _append_to_index(index, dirs[-(i + 1)])
            c.duration = self.ornament_note_duration
            c.time = c.time - c.duration
            if c.time < 0:
              break
            c.volume = base_volume * (self.end_volume - ((i + 1) * delta_volume))
            notes.append(c)
          notes.reverse()
          copy.extend(notes)
      copy.append(e)
    return copy

class GlissandoTransform (OrnamentTransform):

  def __init__(self):
    super().__init__()
    self._count = 6
    self._direction = '`♭'
    
  def set_direction(self, dir):
    self._direction = dir
    return self
    
  def set_count(self, count):
    self._count = count
    return self

  def get_directions(self):
    dirs = []
    offset = ''
    for i in range(0, self._count):
      offset = offset + self._direction
      dirs.append(offset)
    dirs.reverse()
    return dirs

class GraceTransform (GlissandoTransform):

  def __init__(self):
    super().__init__()
    self.set_count(2)
    self.set_direction('`♭')

class RingTransform (GlissandoTransform):

  def __init__(self):
    super().__init__()
    self.set_count(2)
    self.set_direction('')
    
class TrillTransform (OrnamentTransform):

  def __init__(self):
    super().__init__()
    self.set_count(6)
    self.set_direction('`♯`♯')
    
  def set_direction(self, dir):
    self._direction = dir
    return self
    
  def set_count(self, count):
    self._count = count
    return self
    
  def get_directions(self):
    pattern = ['', self._direction]
    return pattern * int(self._count / 2)
    
class MordentTransform (TrillTransform):

  def __init__(self):
    super().__init__()
    self.set_count(2)
    
class TurnTransform (OrnamentTransform):

  def __init__(self):
    super().__init__()
    
  def get_directions(self):
    return ['', '`♯`♯', '', '`♭`♭']
    
class DoubleTurnTransform (OrnamentTransform):

  def __init__(self):
    super().__init__()
    
  def get_directions(self):
    return ['', '`♯', '`♯`♯', '`♯', '', '`♭', '`♭`♭', '`♭']

############ TESTS ############

def _test_one_ornament(transform):
  print("------")
  spec = "@IIIMaj7:T0:D4:c1 @I.0:T4.2:D4 @IIIMaj7.*:T0:D4:c1"
  events = [e.resolved_event(None, 60, False) for e in Event().parse_all(spec)]
  events = transform.transform(events)
  events = [e.normalize() for e in events]
  print(Event.format_all(events))

def _test_ornaments():
  _test_one_ornament(GraceUpTransform())
  _test_one_ornament(GlissandoTransform())

if __name__ == '__main__':
  _test_ornaments()