#!/usr/local/bin/python3
# coding=utf-8

import math
import numpy
from scipy.optimize import linear_sum_assignment

HEPTATONIC_SCALES = [
  [0, 2, 4, 5, 7, 9, 11], # ionian | diatonic | major
  [0, 2, 4, 5, 7, 9, 10], # mixolydian
  [0, 2, 3, 5, 7, 8, 10], # aeolian | natural minor | melodic minor desc
  [0, 2, 4, 6, 7, 9, 11], # lydian
  [0, 2, 3, 5, 7, 9, 10], # dorian
  [0, 1, 3, 5, 7, 8, 10], # phrygian
  [0, 2, 3, 5, 7, 8, 11], # harmonic minor | aeolian #7
  [0, 2, 3, 5, 7, 9, 11], # melodic minor asc | jazz minor 1 | ionian b3
  [0, 1, 3, 5, 6, 8, 10], # locrian
  [0, 1, 4, 5, 7, 8, 10], # flamenco | phrygian #4
  [0, 1, 4, 5, 7, 8, 11], # double harmonic major | phrygian #4 #7
  [0, 2, 3, 6, 7, 8, 11], # hungarian minor | aeolian #4 #7
  [0, 1, 3, 5, 7, 9, 10], # jazz minor mode 2
  [0, 2, 4, 6, 8, 9, 11], # jazz minor mode 3
  [0, 2, 4, 6, 7, 9, 10], # jazz minor mode 4
  [0, 2, 4, 5, 7, 8, 10], # jazz minor mode 5
  [0, 2, 3, 5, 6, 8, 10], # jazz minor mode 6
  [0, 1, 3, 4, 6, 8, 10]  # jazz minor mode 7
]

def complement_notes(notes):
  new = []
  for i in range(0, 12):
    if not i in notes:
      new.append(i)
  return new

def avoid_notes(chord_notes):
  new = []
  for i in range(0, 12):
    if (i + 1) % 12 in chord_notes or (i + 13) % 12 in chord_notes:
      new.append(i)
  return new

def available_notes(chord_notes):
  new = []
  for i in range(0, 12):
    if not (i + 1) % 12 in chord_notes and not (i + 13) % 12 in chord_notes:
      new.append(i)
  return new

def count_common_notes(scale, notes):
  count = 0
  scale = set([n % 12 for n in scale])
  for n in set(notes):
    if (n % 12) in scale:
      count = count + 1
  return count
  
def max_match_heptatonic_scale(notes):
  max = 0
  best = []
  for scale in HEPTATONIC_SCALES:
    count = count_common_notes(scale, notes)
    if count > max:
      max = count
      best = scale
  return best
  
def min_match_heptatonic_scale(notes):
  min = 1000
  best = []
  for scale in HEPTATONIC_SCALES:
    count = count_common_notes(scale, notes)
    if count < min:
      min = count
      best = scale
  return best
  
def max_match_scale(notes, scales):
  max = -1
  best = []
  for scale in scales:
    count = count_common_notes(scale, notes)
    if count > max:
      max = count
      best = scale
  return best
  
def min_match_scales(notes, scales):
  min = 1000
  bests = []
  for scale in HEPTATONIC_SCALES:
    count = count_common_notes(scale, avoid)
    if count < min:
      min = count
      bests = [scale]
    elif count == min:
      bests.append(scale)
  return bests
  
def best_fit_scale(notes, scales = HEPTATONIC_SCALES):
  avoid = avoid_notes(notes)
  bests = min_match_scales(avoid, scales)
  return max_match_scale(notes, bests)

class Scale (object):
  
  def __init__(self):
    self._root = 0
    self._notes = set([])
    
  def copy(self):
    s = Scale()
    s._root = self._root
    s._notes = set(list(self._notes))
    return s
    
  def set_root(self, n):
    self._root = n % 12
    return self

  def get_root(self):
    return self._root
    
  def set_notes(self, notes):
    self._notes = set([n % 12 for n in notes])
    return self

  def resolved_notes(self):
    return sorted([(n + self._root) % 12 for n in self._notes])
    
  def add_note(self, n):
    self._notes.insert(n % 12)
    return self
    
  def intersected(self, other):
    c = self.copy()
    notes = set([(n - c._root) % 12 for n in other.resolved_notes()])
    c._notes = notes.intersection(c._notes)
    return c

  def unioned(self, other):
    c = self.copy()
    notes = set([(n - c._root) % 12 for n in other.resolved_notes()])
    c._notes = notes.union(c._notes)
    return c

  def full_scale(self):
    return [n for n in range(0, 127) if (n % 12) in self._notes]
    
  def complemented(self):
    new = []
    for i in range(0, 12):
      if not i in self._notes:
        new.append(i)
    s = self.copy()
    s._notes = new
    return s
    
  def avoid(self, notes):
    new = []
    for i in range(0, 12):
      if (i + 1) % 12 in self._notes or (i + 13) % 12 in self._notes:
        new.append(i)
    s = self.copy()
    s._notes = new
    return s

  def available(self, notes):
    new = []
    for i in range(0, 12):
      if not (i + 1) % 12 in self._notes and not (i + 13) % 12 in self._notes:
        new.append(i)
    s = self.copy()
    s._notes = new
    return s
    
  def match_scale(self, notes):
    min = 1000
    best = []
    for scale in HEPTATONIC_SCALES:
      count = count_common_notes(scale, notes)
      if count < min:
        min = count
        best = notes
    return best

  def ionian(self):                return self.set_notes([0, 2, 4, 5, 7, 9, 11]) # I
  def dorian(self):                return self.set_notes([0, 2, 3, 5, 7, 9, 10]) # II
  def phrygian(self):              return self.set_notes([0, 1, 3, 5, 7, 8, 10]) # III
  def lydian(self):                return self.set_notes([0, 2, 4, 6, 7, 9, 11]) # IV
  def mixolydian(self):            return self.set_notes([0, 2, 4, 5, 7, 9, 10]) # V   ionian b7
  def aeolian(self):               return self.set_notes([0, 2, 3, 5, 7, 8, 10]) # VI
  def locrian(self):               return self.set_notes([0, 1, 3, 5, 6, 8, 10]) # VII

  def harmonic_minor(self):        return self.set_notes([0, 2, 3, 5, 7, 8, 11]) #     aeolian #7
  def flamenco(self):              return self.set_notes([0, 1, 4, 5, 7, 8, 10]) #     phrygian #4
  def double_harmonic_major(self): return self.set_notes([0, 1, 4, 5, 7, 8, 11]) #     phrygian #4 #7
  def hungarian_minor(self):       return self.set_notes([0, 2, 3, 6, 7, 8, 11]) #     aeolian #4 #7
  def melodic_minor_asc(self):     return self.set_notes([0, 2, 3, 5, 7, 9, 11]) #     ionian b3

  def melodic_minor_desc(self):    return self.aeolian()
  def diatonic(self):              return self.ionian()
  def major(self):                 return self.ionian()
  def natural_minor(self):         return self.aeolian()

  def jazz_minor_mode1(self):      return self.set_notes([0, 2, 3, 5, 7, 9, 11]) #     ionian b3
  def jazz_minor_mode2(self):      return self.set_notes([0, 1, 3, 5, 7, 9, 10])
  def jazz_minor_mode3(self):      return self.set_notes([0, 2, 4, 6, 8, 9, 11])
  def jazz_minor_mode4(self):      return self.set_notes([0, 2, 4, 6, 7, 9, 10])
  def jazz_minor_mode5(self):      return self.set_notes([0, 2, 4, 5, 7, 8, 10])
  def jazz_minor_mode6(self):      return self.set_notes([0, 2, 3, 5, 6, 8, 10])
  def jazz_minor_mode7(self):      return self.set_notes([0, 1, 3, 4, 6, 8, 10])

  def chromatic(self):             return self.set_notes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
  
  def diminished_a(self):          return self.set_notes([0, 1, 3, 4, 6, 7, 9, 10])
  def diminished_b(self):          return self.set_notes([0, 2, 3, 5, 6, 8, 9, 11])

  def whole_tone(self):            return self.set_notes([0, 2, 4, 6, 8, 10])
  def prometheus(self):            return self.set_notes([0, 2, 4, 7, 8, 10])    #     whole tone #4

  def pentatonic(self):            return self.set_notes([0, 2, 4, 7, 9])

  def minor_thirds(self):          return self.set_notes([0, 3, 6, 9])
  def major_thirds(self):          return self.set_notes([0, 4, 8])
  def tritones(self):              return self.set_notes([0, 6])
    
  def format(self):
    return ' '.join(["%d" % n for n in sorted(self.resolved_notes())])

def _generate_modes(base_scale, prefix):
  notes = [n + 12 for n in base_scale] + [n + 24 for n in base_scale]
  notes = base_scale + notes
  for j in range(0, 7):
    ns = []
    for i in range(0, 7):
      ns.append("%d" % (notes[i + j] - notes[j]))
    print (("def %s_mode%d(self): " % (prefix, j + 1)) + "return self.set_notes([" + ", ".join(ns) + "])")
    
def _generate_key_from_scale(scale):
  bits = 0
  scale = set([n % 12 for n in scale])
  for i in range(0, 12):
    if i in scale:
      bits = bits | (1 << i)
  return bits
  
def _generate_scale_from_key(bits):
  scale = []
  for i in range(0, 12):
    if bits & (1 << i):
      scale.append(i)
  return scale

def _generate_diatonic_modes():
  _generate_modes([0, 2, 4, 5, 7, 9, 11], 'diatonic')
  
def _generate_jazz_modes():
  _generate_modes([0, 2, 3, 5, 7, 9, 11], 'jazz_minor')

def _generate_diminished():
  (nsa, nsb) = ([], [])
  (stepa, stepb) = (0, 0)
  for i in range(0, 8):
    nsa.append("%d" % stepa)
    nsb.append("%d" % stepb)
    if i % 2 == 0:
      stepa = stepa + 1
      stepb = stepb + 2
    else:
      stepb = stepb + 1
      stepa = stepa + 2
  print ("def diminished_a(self): return self.set_notes([" + ", ".join(nsa) + "])")
  print ("def diminished_b(self): return self.set_notes([" + ", ".join(nsb) + "])")

def _generate_keys():
  for scale in HEPTATONIC_SCALES:
    key = _generate_key_from_scale(scale)
    print(scale, " key %d" % key, " out ", _generate_scale_from_key(key))
  
def _test_generate_modes():
  _generate_diminished()
  _generate_diatonic_modes()
  _generate_jazz_modes()
  _generate_keys()

def _test_intersection_1():
  a = Scale()
  a.set_root(60)
  a.diatonic()
  b = Scale()
  b.set_root(64)
  b.diatonic()
  c = a.intersected(b)
  print("A: " + a.format())
  print("B: " + b.format())
  print("C: " + c.format())
  
def _test_intersection_2():
  a = Scale()
  a.set_root(60)
  a.diatonic()
  b = Scale()
  b.set_root(60)
  b.jazz_minor_mode1()
  c = a.intersected(b)
  print("A: " + a.format())
  print("B: " + b.format())
  print("C: " + c.format())
  
if __name__ == '__main__':
  _test_generate_modes()
  _test_intersection_1()
  _test_intersection_2()
