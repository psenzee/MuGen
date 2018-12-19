#!/usr/local/bin/python3
# coding=utf-8

import math
import numpy
from random import shuffle
from copy import deepcopy
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

def transpose(scale, key):
  return [(n + key) % 12 for n in scale]

def scales_all_keys(scales):
  out_scales = []
  for scale in scales:
    for i in range(0, 12):
      out_scales.append(transpose(scale, i))
  return out_scales

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
  scales = copy.deepcopy(HEPTATONIC_SCALES)
  random.shuffle(scales)
  for scale in scales:
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
  return sorted(best)
  
def max_match_scale(notes, scales):
  max = -1
  best = []
  for scale in scales:
    count = count_common_notes(scale, notes)
    if count > max:
      max = count
      best = scale
  return sorted(best)
  
def min_match_scales(notes, scales):
  min = 1000
  bests = []
  for scale in scales:
    count = count_common_notes(scale, notes)
    if count < min:
      min = count
      bests = [sorted(scale)]
    elif count == min:
      bests.append(sorted(scale))
  return bests
  
def best_fit_scale(notes):
  scales = scales_all_keys(HEPTATONIC_SCALES)
  bests = min_match_scales(avoid_notes(notes), scales)
  return max_match_scale(notes, bests)

def format_notes(notes):
  return '[' + ' '.join(['%d' % n for n in sorted(notes)]) + ']'
  
def _closest_note_in_scale(n, scale):
  for i in range(0, 6):
    if (n + i) % 12 in scale:
      return n + i
    if (n - i + 12) % 12 in scale:
      return n - i
  return None
  
def generate_code_from_scale(scale):
  bits = 0
  scale = set([n % 12 for n in scale])
  for i in range(0, 12):
    if i in scale:
      bits = bits | (1 << i)
  return bits
  
def rescale_notes(notes, scale):
  return [_closest_note_in_scale(n, set(scale)) for n in notes]

def _test_best_fit_scale(chord):
  parts = ["Chord: " + format_notes(sorted(chord))]
  scale = best_fit_scale(chord)
  parts.append("BestFit: " + format_notes(sorted(scale)))
  final = list(set(scale).union(set([c % 12 for c in chord])))
  if len(final) != len(scale):
    parts.append("BestFit(+Chord): " + format_notes(final))
  print (" ".join(parts))
  print ("Rescaled Chromatic: " + format_notes(rescale_notes(range(-12, 24), final)))

if __name__ == '__main__':
  from Chords import *
  chords = [
    CHORD3_MAJOR, CHORD3_MINOR, CHORD3_SUS2, CHORD3_SUS4, CHORD3_DIM, CHORD3_AUG,
    CHORD4_MINOR_MIN7, CHORD4_MINOR7, CHORD4_MINOR_MAJ7, CHORD4_MINOR6, CHORD5_MINOR9,
    CHORD4_MAJOR_MIN7, CHORD4_MAJOR6, CHORD4_DOM7, CHORD4_MAJOR_MIN7,
    CHORD4_MAJOR_MAJ7, CHORD4_MAJOR7, CHORD4_SUS2_MAJ7, CHORD4_SUS2_MIN7,
    CHORD4_SUS4_MAJ7, CHORD4_SUS4_MIN7, CHORD4_DIM7, CHORD4_AUG7, CHORD5_DOM7_FLAT9,
    CHORD5_DOM9
  ]
  for c in chords:
    _test_best_fit_scale(c)
  
