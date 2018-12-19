#!/usr/local/bin/python3
# coding=utf-8

import math
import midiutil
import random
import copy

from Chords import *
from scale_match import best_fit_scale
from scale_match import rescale_notes
from scale_match import generate_code_from_scale

CHORDS = Chords()

class Chord (object):

  def __init__(self, chord_root = 0, root = 60, notes = [], scale = [], time = 0, duration = 1, volume = 100):
    self.root = root
    self.set_notes(notes, scale, chord_root)
    self.time = time
    self.duration = duration
    self.volume = volume

  def copy(self):
    c = Chord()
    c.root = self.root
    c.set_notes(self._notes, self._scale, self.chord_root)
    c.time = self.time
    c.duration = self.duration
    c.volume = self.volume
    return c

  def set_notes(self, notes, scale, chord_root):
    if notes == None:
      notes = []
    self.chord_root = chord_root
    self._best_scale = best_fit_scale(notes)
    self._notes = copy.deepcopy(notes)
    self._scale = copy.deepcopy(scale)
    self._ineligible = None
    return self
    
  def get_notes(self):
    return self._notes
    
  def index_of_note(self, note):
    for i in range(0, len(self._notes)):
      if note % 12 == self._notes[i] % 12:
        return i
    return None

  def mode_code(self):
    scale = self._best_scale
    return generate_code_from_scale(scale)

  def note(self, index, offset = 0):
    ln = len(self._notes)
    if ln == 0:
      return None
    note = self._notes[(index + self.root_index()) % ln] # CAUTION THIS COULD HAVE A PROFOUND EFFECT ON GENERATION
    if offset == 0:
      return note
    c = note + offset
    return c
    rescaled = rescale_notes([c], self._best_scale)
    if rescaled and len(rescaled) > 0:
      return rescaled[0]
    return note
    #if offset == 0:
    #  return note
    #return self._nth_offset(note, offset)
    
    
  def rescale_note(self, note):
    rescaled = rescale_notes([note], self._best_scale)
    if rescaled and len(rescaled) > 0:
      return rescaled[0]
    return note

  def rescale_notes(self, notes):
    if notes == None:
      return None
    return rescale_notes(notes, self._best_scale)

  def root_index(self):
    r = (self.chord_root + self.root) % 12
    #print ("CHORD_ROOT %d" % r)
    for i in range(0, len(self._notes)):
      if self._notes[i] % 12 == r:
        return i
    return r
    #print ("root_index returning None")
    return None

  def similarity(self, other):
    a = self.absolute_notes()
    b = other.absolute_notes()
    intersect = list(set(a) & set(b))
    diff = abs(sum(a) / float(len(a)) - sum(b) / float(len(b)))
    return len(intersect) * 1 - diff

  def add_interval(self, note, octave = 0):
    self._notes.append(note + octave * INTERVAL_OCTAVE)
    return self

  def write_midi(self, midifile, track = 0, channel = 0):
    print("**** SHOULD NOT BE CALLED **")
    for n in self.absolute_notes():
      self._write_midi_absolute_note(midifile, n, track, channel)
    return self

  def set_root(self, root):
    self.root = root
    return self

  def set_time(self, time):
    self.time = time
    return self

  def set_duration(self, duration):
    self.duration = duration
    return self

  def set_volume(self, volume):
    self.volume = volume
    return self

  def chord(self, intervals, scale, chord_root, inversion = 0, octave = 0):
    notes = invert(intervals, inversion)
    oct = octave * INTERVAL_OCTAVE
    return self.set_notes([n + oct for n in notes], [n + oct for n in scale], chord_root)

  def notes(self):
    return self._notes

  def rest(self):
    self.set_notes([], [])
    return self

  def interpolate(self, chord, scale = None):
    notesa = self._notes
    notesb = chord.rebased_notes(self.root)
    notes = interpolate(notesa, notesb, scale)
    c = self.copy()
    c.time = (self.time + chord.time) / 2
    base_scale = set(self._scale).intersection(set(chord._scale))
    if scale:
      scale = base_scale.intersection(set(scale))
    else:
      scale = base_scale
    scale = sorted(list(scale))
    return c.chord(notes, scale)

  def invert(self, inversion):
    self.set_notes(invert(self._notes, inversion), self.chord_root)
    return self

  def absolute_notes(self):
    return [n + self.root for n in self._notes]

  def rebased_notes(self, key):
    base = self.root - key
    return [n + base for n in self._notes]

  def scale(self):
    return scale_from_notes(self.absolute_notes())

  def high(self):
    return max(self.absolute_notes() - root)

  def low(self):
    return min(self.absolute_notes() - root)
    
  def dissonant(self):
    # find if any two notes are separated by only 1/2 step
    notes = self.absolute_notes()
    for n in notes:
      for m in notes:
        if abs(n - m) == 1:
          return True
    return False
    
  def closest_inversion_of(self, chord):
    max = self.similarity(chord)
    best = chord
    notes = chord._notes
    scale = chord._scale
    for octave in [0, -1, 1]:
      for inversion in range(-3, 4):
        c = chord.copy()
        c.chord(notes, scale, inversion, octave)
        if c.dissonant():
          continue # not a contender
        score = self.similarity(c)
        if score > max:
          max = score
          best = c
    return best

  # CONVENIENCE
  
  def symbol_chord(self, symbol):
    c = self.copy()
    parts = symbol.split(':')
    duration = 1
    symbol = parts[0]
    if len(parts) > 1:
      duration = float(parts[1])
    parts = symbol.split('/')
    inversion = 0
    symbol = parts[0]
    if len(parts) > 1:
      inversion = int(parts[1])
    if symbol.lower() != 'r':
      (root, chord_root, notes, scale) = CHORDS.from_symbol(symbol)
      #print ("ROOT %d CHORD_ROOT %d NOTES " % (root, chord_root), notes, " SCALE ", scale)
      c.chord([n + root for n in notes], [n + root for n in scale], root, inversion, 0)
    else:
      c.rest()
    c.set_duration(duration)
    return c
    
  # private  
  def _next_offset(self, note, direction = 1):
    ineligible = self._ineligible_set()
    for i in range(direction * 1, direction * 12, direction):
      if not (i + note + 12) % 12 in ineligible:
        return i + note
    return None
    
  def _nth_offset(self, note, n):
    direction = (1, -1)[n < 0]
    off = note
    n = direction * n
    while off != None and n > 0:
      off = self._next_offset(off, direction)
      n = n - 1
    return off

  def _write_midi_absolute_note(self, midifile, note, track, channel):
    (time, duration, volume) = VARIATION.apply(self.time, self.duration, self.volume)
    if time < 0:
       time = 0
    midifile.addNote(track, channel, note, time, duration, volume)

  def _ineligible_set(self):
    if self._ineligible == None:
      ns = self._notes
      half_step_off = [(n + 1) % 12 for n in ns] + [(n - 1) % 12 for n in ns]
      ineligible_scale = list(set(range(0, 12)).difference([n % 12 for n in self._scale]))
      self._ineligible = set(half_step_off + ineligible_scale)
    return self._ineligible

# tests

def _test_chord():
  c = Chord().symbol_chord("III")
  for index in [0, 1, 2, 3, 4]:
    print("index: ", index, " = note: ", c.note(index, 0))
    for offset in [-3, -2, -1, 0, 1, 2, 3]:
      print("index: ", index, " = note: ", c.note(index, 0), " + offset: ", offset, " = note: ", c.note(index, offset))
      
if __name__ == '__main__':
  _test_chord()