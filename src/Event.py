#!/usr/local/bin/python3
# coding=utf-8

import random
import copy
from Chord import Chord
from BaseEvent import BaseEvent
import Midi
from Utils import *

class Event (BaseEvent):

  def __init__(self, name = None, index = None, time = None, duration = 4, octave = 0, volume = 100, pitches = [], mode = None, channel = 0):
    super().__init__(name, [], time, duration, volume, channel)

    self.index = index
    self.octave = octave
    self.pitches = pitches
    self.mode = mode
    self.ch = None
    self.rescale = True
    self.defaults = self.defaults.update({
      'N' : [],
      'o' : 0,
      'M' : None
    })

  def copy(self):
    e = Event(self.name, self.index, self.time, self.duration, self.octave, self.volume, self.pitches, self.mode, self.channel)
    e.midinotes = self.midinotes
    if self.ch != None:
       e.ch = self.ch.copy()
    return e

  def is_valid(self):
    return not None in [self.name, self.time, self.duration, self.octave, self.volume]
    
  def parse_name(self, name):
    self.name = name
    parts = self.name.split('.')
    self.name = parts[0]
    if len(parts) > 1 and len(parts[1]) > 0:
      self.index = parts[1]
      self.index = self._normalize_index()
      #print("!!INDEX = " + str(self.index))
    return self
    
  def parse_arguments(self, text):
    super().parse_arguments(text)
    value = BaseEvent.parse_op_int_array('N', text)
    if value != None: self.pitches = value
    value = BaseEvent.parse_op_int('M', text)
    if value != None: self.mode = value
    value = BaseEvent.parse_op_int('o', text)
    if value != None: self.octave = value
    return self

  def normalize(self):
    if self.ch != None and self.midinotes != None and len(self.midinotes) > 0:
      notes = self.notes(self.ch)
      if notes != None and len(notes) > 0:
        self.midinotes = [n + 12 * self.octave for n in notes]
    #print("OCTAVE %d" % self.octave)
    return self

  def renormalize(self):
    self.midinotes = []
    return self.normalize()

  def notes(self, chord):
    notes = self._parse_index(self.index, chord)
    if self.rescale:
      return chord.rescale_notes(notes)
    return notes

  def resolve_chord_name(self, map, with_index = True):
    name = self.name
    if self.name == None:
      raise RuntimeError("Event name is none")
    if not self.name.startswith('@'):
      if not self.name in map:
        raise RuntimeError("Unrecognized event chord/note name %s, missing from map" % self.name)
      else:
        name = '@' + str(map[self.name])
    if with_index and self.index != None:
      name = name + (".%s" % self.index)
    return name
    
  def resolved_event(self, map, root, resolve_index = True):
    e = self.copy()
    e.name = e.resolve_chord_name(map, False)
    c = e.chord(map, root, 0)
    notes = copy.deepcopy(c.get_notes())
    e.ch = c
    if e.mode == None:
      e.mode = c.mode_code()
    e.pitches = notes
    e.midinotes = e.pitches[:]
    if resolve_index:
      if len(notes) < 3:
        names = ["@%d" % n for n in notes]
        e.name = ','.join(names)
        e.index = None
    e = e.normalize()
    return e
    
  def chord_symbol(self, map):
    if self.name == None:
      raise RuntimeError("No event name given")
    chord = None
    if self.name.startswith('@'):
      chord = self.name[1:]
    elif not self.name in map:
      raise RuntimeError("Unrecognized event chord/note name %s, missing from map" % self.name)
    else:
      chord = str(map[self.name])
    return chord + ":%.3f" % (self.duration / 4.0)

  def chord(self, map, root, time = 0):
    symbol = self.chord_symbol(map)
    c = Chord().symbol_chord(symbol)
    if self.index != None:
      c.set_notes(self.notes(c), c.scale, c.chord_root)
    c.set_time((self.time + time) / 4.0)
    if not self.octave:
      self.octave = 0
    c.set_root(root + self.octave * 12)
    return c
    
  def get_defaults(self):
    defaults = super().get_defaults()
    defaults.update({
      'N' : None,
      'o' : 0,
      'N' : [],
      'M' : None
    })
    return defaults
    
  def get_final_notes(self):
    return [n + 12 * self.octave for n in super().get_final_notes()]
    
  def format_name(self):
    name = self.name
    if name == None:
      return ''
    if self.index != None and len(self.index.strip()) > 0:
      name = name + (".%s" % self.index)
    return name

  def format(self):
    pitches = self.pitches
    if pitches != None and len(pitches) != 0:
      pitches = ','.join(["%d" % p for p in pitches])
    else:
      pitches = None
    return super().format({ 'o' : self.octave, 'M' : self.mode, 'N' : pitches })

  def _parse_num(self, value):
    try:
      return int(value)
    except:
      pass
    return None
    
  def _parse_note_number(self, index):
    num = None
    if index == None or len(index) == 0:
      return None
    if index == '*':
      num = random.choice(range(0, 12))
    else:
      num = self._parse_num(index)
      if num == None:
        return None
    return num
    
  @staticmethod
  def _split_num(index, delimiter):
    if index == None or len(index) == 0:
      return (None, None)
    pieces = index.split(delimiter)
    if len(pieces) < 2:
      return (None, None)
    (first, last) = pieces
    if len(first) == 0:
      first = None
    if len(last) == 0:
      last = None
    return (first, last)
    
  def _normalize_index(self):
    return self.index
    if self.index == None:
      return self.index
    self.index = str(self.index)
    if len(self.index) == 0:
      self.index = None
      return self.index
    prevlen = 0
    replacements = {
      '#b' : '', 'b#' : '', '♭#' : '', '#♭' : '',
      '♯b' : '', 'b♯' : '', '♭♯' : '', '♯♭' : '',
      '+-' : '', '-+' : ''
    }
    while prevlen != len(self.index):
      prevlen = len(self.index)
      for k, v in replacements.items():
        self.index = self.index.replace(k, v)
    return self.index

  def _parse_note_indicator(self, index, chord):
    num = None
    if index == None or len(index) == 0 or \
      index.startswith('-') or index.startswith('+') or \
      (not '+' in index and not '-' in index):
      return None
    if '+' in index:
      (first, last) = self._split_num(index, '+')
    if '-' in index:
      (first, last) = self._split_num(index, '-')
    if first == None:
      return None
    num = self._parse_note_index(first, chord)
    if num == None:
      return None
    offset = self._parse_num(index)
    if offset == None:
      offset = 0
    return chord.note(num, offset)

  def _parse_note_index(self, index, chord):
    num = self._parse_note_number(index)
    if num == None:
      return None
#    remap = [2, 1, 0]
#    if num in remap:
#      num = remap[num]  #dis gon get crazay
    return chord.note(num)
    
  def _parse_single_altered_index(self, index, chord):
    if any_suffix(index, ['`b', '`♭', '`#', '`♯']):
      pair = (index[-2:], index[0:-2])
    elif any_suffix(index, ['b', '♭', '#', '♯']):
      pair = (index[-1:], index[0:-1])
    else:
      return None
    (suffix, index) = pair
    num = self._parse_index(index, chord)[0]
    num += (0, -1)[suffix in ['b', '♭', '`b', '`♭']]
    num += (0,  1)[suffix in ['#', '♯', '`#', '`♯']]
    if not suffix.startswith('`'):
      return num #chord.rescale_note(num)
    return num

  def _parse_index(self, index, chord):
    initial = index
    if index == None or len(index) == 0:
      return None
    num = self._parse_note_indicator(index, chord)
    if num != None:
      return [num]
    num = self._parse_note_index(index, chord)
    if num != None:
      return [num]
    parts = index.split(',')
    if len(parts) > 1:
      result = []
      for part in parts:
        nums = self._parse_index(part, chord)
        result = result + nums
      return list(set(result))
    index = parts[0]
    num = self._parse_single_altered_index(parts[0], chord)
    if num == None:
      raise RuntimeError("Unrecognized format in _parse_index: %s" % initial)
    return [num]
    """
    # do the single parse
    last = index[-1]
    rest = index[0:-1]
    nums = self._parse_index(rest, chord)
    if last in ['b', '♭']:
      return [chord.rescale_note(nums[0] - 1)]
    if last in ['#', '♯']:
      return [chord.rescale_note(nums[0] + 1)]
    raise RuntimeError("Unrecognized format in _parse_index: %s" % initial)
    """

  @staticmethod
  def _variable(var, index):
    if index != None and len(index) > 0:
      return var + "." + index
    return var
    
  @staticmethod
  def _time(time = 0):
    if time == None:
      time = 0
    return "T%d" % int(time)

  @staticmethod
  def _duration(duration = 4):
    if duration == None:
      duration = 4
    return "D%d" % int(duration)

  @staticmethod
  def _octave(octave = None):
    if octave == None or len(str(octave)) == 0:
      return None
    octave = int(octave)
    if octave > 0:
      return "o+%d" % octave
    return "o%d" % octave

def _test_events():
  spec = "@IIIMaj7:T0:D4:c1 @I.0:T4.2:D4 @I.0♭:T4.2:D4 @I.0`♭:T4.2:D4 @IIIMaj7.*:T0:D4:c1"
  #spec = ":[60:T4:D4:c1"
  events = [e.resolved_event(None, 60, False).renormalize() for e in Event().parse_all(spec)]
  for e in events:
    print (e.format())
  print (Event.format_all(events))
  midi = Midi.Midi(1)
  midi.open('miditest')
  newlist = []
  for e in events:
    newlist.extend(e.bisect())
  events = newlist
  for e in events:
    e.write(midi)
  print (Event.format_all(events))
  midi.close()

if __name__ == '__main__':
  _test_events()
