#!/usr/local/bin/python3
# coding=utf-8

import math
import numpy
from scipy.optimize import linear_sum_assignment

OCTAVE                    = 12
MAX_NOTE                  = 127
INVALID_NOTE              = 128

BASE_b3                   = [3]
BASE_b5                   = [6]
BASE_b7                   = [10]
BASE_CHROMATIC            = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
BASE_MINOR                = [0, 2, 3, 5, 7, 8, 11]
BASE_MINORb7              = [0, 2, 3, 5, 7, 8, 10]
BASE_WHOLE_TONE           = [0, 2, 4, 6, 8, 10]
BASE_MINOR_STEPS          = [0, 3, 6, 9]
BASE_MAJOR_STEPS          = [0, 4, 7, 11]
BASE_TRITONES             = [0, 6]
BASE_DIATONIC             = [0, 2, 4, 5, 7, 9, 11]
BASE_DIATONICb7           = [0, 2, 4, 5, 7, 9, 10]
BASE_DIATONICs5           = [0, 2, 4, 6, 7, 9, 11]
BASE_DIATONIC_PLUSb7      = sorted(BASE_DIATONIC + BASE_b7)
BASE_DIATONIC_PLUSb3b7    = sorted(BASE_DIATONIC + BASE_b3 + BASE_b7)
BASE_PENTATONIC           = [0, 2, 4, 7, 9]
BASE_PENTATONIC_PLUSb7    = sorted(BASE_PENTATONIC + BASE_b7)
BASE_PENTATONIC_PLUSb3b7  = sorted(BASE_PENTATONIC + BASE_b3 + BASE_b7)

def normalized_scale(root, base_scale):
  return set([(n + root) % 12 for n in base_scale])

def diatonic(root):
  return normalized_scale(root, BASE_DIATONIC)

SCALE_CHROMATIC  = set([n for n in range(-128, 128)])
SCALE_DIATONIC_C = set([n for n in range(-128, 128) if n % 12 in [0, 2, 4, 5, 7, 9, 11]])

SCALE_DIATONIC_C_LIST = [n for n in range(-128, 128) if n % 12 in [0, 2, 4, 5, 7, 9, 11]]
SCALE_DIATONIC_F_LIST = [n for n in range(-128, 128) if n % 12 in [5, 7, 9, 10, 0, 2, 4]]
SCALE_DIATONIC_FSH_LIST = [n for n in range(-128, 128) if n % 12 in [6, 8, 10, 11, 1, 3, 5]]

def invert(notes, inversion = 1):
  if len(notes) > 1 and inversion != 0:
    reverse = inversion > 0
    direction = math.copysign(1, inversion)
    inversion = abs(inversion)
    for i in range(0, inversion):
      notes = sorted(notes, reverse=reverse)
      value = notes.pop() + OCTAVE * direction
      notes.append(value)
  return [int(n) for n in sorted(notes, reverse=True)]
  
def dissonant(notes):
  # find if any two notes are separated by only 1/2 step
  for n in notes:
    for m in notes:
      if abs(n - m) == 1:
        return True
  return False

def _map_cost(map):
  sum = 0
  for (m, n) in map:
    sum = sum + abs(m - n)
  return sum

def _map_sets(notesa, notesb, log = False):
  lena = len(notesa)
  lenb = len(notesb)
  if lena == 0 or lenb == 0:
    return None
  elif lena > lenb:
    notesb = notesb + [INVALID_NOTE] * (lena - lenb)
  elif lenb > lena:
    notesa = notesa + [INVALID_NOTE] * (lenb - lena)
  arr = []
  for n in notesa:
    subarr = []
    for m in notesb:
      subarr.append(int(abs(n - m)))
    arr.append(subarr)
  costs = numpy.array(arr)
  rows, cols = linear_sum_assignment(costs)
  if log:
    print ("rows " + str(rows))
    print ("cols " + str(cols))
  map = []
  for i in range(0, len(rows)):
    map.append((notesa[rows[i]], notesb[cols[i]]))
  if log:
    print ("map  " + str(map))
    print ("cost " + str(_map_cost(map)))
  return map
  
def closest_scale_note(n, scale, max = 12):
  for m in range(0, max):
    if n + m in scale:
      return n + m
    if n - m in scale:
      return n - m
  return None

def interpolate(notesa, notesb, scale, log = False):
  map = _map_sets(notesa, notesb, log)
  notes = []
  if scale == None:
    scale = SCALE_CHROMATIC
  for (a, b) in map:
    if a == INVALID_NOTE or b == INVALID_NOTE:
      continue
    diff = int((a - b) / 2)
    note = closest_scale_note(b + diff, scale, max = 5)
    if note:
      notes.append(note)
  return notes

def notes_mod_12(notes):
  return [n % 12 for n in notes]
  
def note_in_set_mod_12(note, set):
  return (note % 12) in [n % 12 for n in set]

def scale_from_notes(notes):
  mod12 = set([n % 12 for n in notes])
  return [n for n in range(0, 127) if (n % 12) in mod12]

INTERVAL_ROOT       = 0
INTERVAL_MIN_2ND    = 1
INTERVAL_MAJ_2ND    = 2
INTERVAL_MIN_3RD    = 3
INTERVAL_MAJ_3RD    = 4
INTERVAL_4TH        = 5
INTERVAL_AUG_4TH    = 6
INTERVAL_DIM_5TH    = 6
INTERVAL_5TH        = 7
INTERVAL_AUG_5TH    = 8
INTERVAL_MIN_6TH    = 8
INTERVAL_MAJ_6TH    = 9
INTERVAL_MIN_7TH    = 10
INTERVAL_MAJ_7TH    = 11
INTERVAL_OCTAVE     = 12
INTERVAL_FLAT_9TH   = INTERVAL_OCTAVE + INTERVAL_MIN_2ND
INTERVAL_9TH        = INTERVAL_OCTAVE + INTERVAL_MAJ_2ND
INTERVAL_11TH       = INTERVAL_OCTAVE + INTERVAL_4TH
INTERVAL_13TH       = INTERVAL_OCTAVE + INTERVAL_MAJ_6TH

CHORD3_MAJOR        = [INTERVAL_5TH, INTERVAL_MAJ_3RD, INTERVAL_ROOT]
CHORD3_MINOR        = [INTERVAL_5TH, INTERVAL_MIN_3RD, INTERVAL_ROOT]
CHORD3_SUS2         = [INTERVAL_5TH, INTERVAL_MAJ_2ND, INTERVAL_ROOT]
CHORD3_SUS4         = [INTERVAL_5TH, INTERVAL_4TH, INTERVAL_ROOT]
CHORD3_DIM          = [INTERVAL_DIM_5TH, INTERVAL_MIN_3RD, INTERVAL_ROOT]
CHORD3_AUG          = [INTERVAL_MIN_6TH, INTERVAL_MAJ_3RD, INTERVAL_ROOT]
CHORD4_MINOR_MIN7   = [INTERVAL_MIN_7TH, INTERVAL_5TH, INTERVAL_MIN_3RD, INTERVAL_ROOT]
CHORD4_MINOR7       = CHORD4_MINOR_MIN7
CHORD4_MINOR_MAJ7   = [INTERVAL_MAJ_7TH, INTERVAL_5TH, INTERVAL_MIN_3RD, INTERVAL_ROOT]
CHORD4_MINOR6       = [INTERVAL_MAJ_6TH, INTERVAL_5TH, INTERVAL_MIN_3RD, INTERVAL_ROOT]
CHORD5_MINOR9       = [INTERVAL_9TH, INTERVAL_MIN_7TH, INTERVAL_5TH, INTERVAL_MIN_3RD, INTERVAL_ROOT]
CHORD4_MAJOR_MIN7   = [INTERVAL_MIN_7TH, INTERVAL_5TH, INTERVAL_MAJ_3RD, INTERVAL_ROOT]
CHORD4_MAJOR6       = [INTERVAL_MAJ_6TH, INTERVAL_5TH, INTERVAL_MAJ_3RD, INTERVAL_ROOT]
CHORD4_DOM7         = CHORD4_MAJOR_MIN7
CHORD4_MAJOR_MAJ7   = [INTERVAL_MAJ_7TH, INTERVAL_5TH, INTERVAL_MAJ_3RD, INTERVAL_ROOT]
CHORD4_MAJOR7       = CHORD4_MAJOR_MAJ7
CHORD4_SUS2_MAJ7    = [INTERVAL_MAJ_7TH, INTERVAL_5TH, INTERVAL_MAJ_2ND, INTERVAL_ROOT]
CHORD4_SUS2_MIN7    = [INTERVAL_MIN_7TH, INTERVAL_5TH, INTERVAL_MAJ_2ND, INTERVAL_ROOT]
CHORD4_SUS4_MAJ7    = [INTERVAL_MAJ_7TH, INTERVAL_5TH, INTERVAL_4TH, INTERVAL_ROOT]
CHORD4_SUS4_MIN7    = [INTERVAL_MIN_7TH, INTERVAL_5TH, INTERVAL_4TH, INTERVAL_ROOT]
CHORD4_DIM7         = [INTERVAL_MAJ_6TH, INTERVAL_DIM_5TH, INTERVAL_MIN_3RD, INTERVAL_ROOT]
CHORD4_AUG7         = [INTERVAL_MAJ_7TH, INTERVAL_MIN_6TH, INTERVAL_MAJ_3RD, INTERVAL_ROOT] # is this right??
#CHORD4_TRITONE_MAJ7 = [INTERVAL_MAJ_7TH - INTERVAL_AUG_4TH, INTERVAL_5TH - INTERVAL_AUG_4TH, INTERVAL_MAJ_3RD - INTERVAL_AUG_4TH, INTERVAL_ROOT - INTERVAL_AUG_4TH]
CHORD5_DOM7_FLAT9   = [INTERVAL_FLAT_9TH, INTERVAL_MIN_7TH, INTERVAL_5TH, INTERVAL_MAJ_3RD, INTERVAL_ROOT]
CHORD5_DOM9         = [INTERVAL_9TH, INTERVAL_MIN_7TH, INTERVAL_5TH, INTERVAL_MAJ_3RD, INTERVAL_ROOT]

CHORDS = [
  CHORD3_MAJOR,
  CHORD3_MINOR,
  CHORD3_SUS2,
  CHORD3_SUS4,
  CHORD3_DIM,
  CHORD3_AUG,
  CHORD4_MINOR_MIN7,
  CHORD4_MINOR_MAJ7,
  CHORD4_MINOR6,
  CHORD4_MAJOR_MIN7,
  CHORD4_MAJOR6,
  CHORD4_MAJOR_MAJ7,
  CHORD4_MAJOR7,
  CHORD4_SUS2_MAJ7,
  CHORD4_SUS2_MIN7,
  CHORD4_SUS4_MAJ7,
  CHORD4_SUS4_MIN7,
  CHORD4_DIM7,
  CHORD4_AUG7,
]

RESTRICTED_CHORDS = [
  CHORD3_MAJOR,
  CHORD3_MINOR,
  CHORD3_DIM,
  CHORD3_AUG,
  CHORD4_MINOR_MIN7,
  CHORD4_MINOR6,
  CHORD4_MAJOR6,
  CHORD4_DIM7,
  CHORD4_AUG7
]

# sharp: ♯
# flat: ♭
# diminished: ° o o

"""
In popular music
"In rock and pop music, the diminished triad nearly always appears on the second scale degree,
forming a generally maudlin and dejected iio with its members, 2–4–♭6."[11] Songs that
feature iio include Santo & Johnny's Sleep Walk, Jay and the Americans' "Cara Mia", and
The Hollies' "The Air That I Breathe".[11] Not so rare but rare enough so as to imply
knowledge of and conscious avoidance on the part of rock musicians, examples of its use
include Oasis' "Don't Look Back in Anger", David Bowie's "Space Oddity", and two in
Daryl Hall's "Everytime You Go Away".[12]

If the song is in a minor key, diminished triads are usually on the sharpened seventh
note, ♯7-2-4. This is because the ascending melodic minor scale has a sharpened sixth
and seventh degree. For example, the chord progression ♯viio, i is common.
"""

class Chords (object):

  def __init__(self):
    map = {}
    keys = [
      ['I', '♯VII', '#VII'],
      ['♭II', 'bII', '♯I', '#I'],
      ['II'],
      ['♭III', 'bIII', '♯II', '#II'],
      ['III', '♭IV', 'bIV'],
      ['IV', '♯III', '#III'],
      ['♭V', 'bV', '♯IV', '#IV'],
      ['V'],
      ['♭VI', 'bVI', '♯V', '#V'],
      ['VI'],
      ['♭VII', 'bVII', '♯VI', '#VI'],
      ['VII', '♭I', 'bI']
    ]
    types = [{
      ''         : (CHORD3_MAJOR,       BASE_DIATONIC),
      '+'        : (CHORD3_AUG,         BASE_DIATONICs5), # could be BASE_WHOLE_TONES
      '7'        : (CHORD4_MAJOR_MIN7,  BASE_DIATONICb7),
      '7b9'      : (CHORD5_DOM7_FLAT9,  BASE_DIATONICb7),
      '7♭9'      : (CHORD5_DOM7_FLAT9,  BASE_DIATONICb7),
      '7-9'      : (CHORD5_DOM7_FLAT9,  BASE_DIATONICb7),
      '9'        : (CHORD5_DOM9,        BASE_DIATONICb7),
      '6'        : (CHORD4_MAJOR6,      BASE_DIATONIC),
      'Maj7'     : (CHORD4_MAJOR_MAJ7,  BASE_DIATONIC),
      'M7'       : (CHORD4_MAJOR_MAJ7,  BASE_DIATONIC),
      'sus2'     : (CHORD3_SUS4,        BASE_DIATONIC),
      'sus2Maj7' : (CHORD4_SUS2_MAJ7,   BASE_DIATONIC),
      'sus2M7'   : (CHORD4_SUS2_MAJ7,   BASE_DIATONIC),
      'sus2m7'   : (CHORD4_SUS2_MIN7,   BASE_DIATONICb7),
      'sus2dom7' : (CHORD4_SUS2_MIN7,   BASE_DIATONICb7),
      'sus27'    : (CHORD4_SUS2_MIN7,   BASE_DIATONICb7),
      'sus4'     : (CHORD3_SUS4,        BASE_DIATONIC),
      'sus4Maj7' : (CHORD4_SUS4_MAJ7,   BASE_DIATONIC),
      'sus4M7'   : (CHORD4_SUS4_MAJ7,   BASE_DIATONIC),
      'sus4m7'   : (CHORD4_SUS4_MIN7,   BASE_DIATONICb7),
      'sus4dom7' : (CHORD4_SUS4_MIN7,   BASE_DIATONICb7),
      'sus47'    : (CHORD4_SUS4_MIN7,   BASE_DIATONICb7)
    },
    {
      ''         : (CHORD3_MINOR,       BASE_MINOR),
      'o'        : (CHORD3_DIM,         BASE_MINORb7), # could be BASE_MINOR_STEPS
      '°'        : (CHORD3_DIM,         BASE_MINORb7), # could be BASE_MINOR_STEPS
      '7'        : (CHORD4_MINOR_MIN7,  BASE_MINORb7),
      '9'        : (CHORD5_MINOR9,      BASE_MINORb7),
      '6'        : (CHORD4_MINOR6,      BASE_MINOR),
      'Maj7'     : (CHORD4_MINOR_MAJ7,  BASE_MINOR),
      'M7'       : (CHORD4_MINOR_MAJ7,  BASE_MINOR),
      'o7'       : (CHORD4_DIM7,        BASE_MINORb7), # could be BASE_MINOR_STEPS
      '°7'       : (CHORD4_DIM7,        BASE_MINORb7)  # could be BASE_MINOR_STEPS
    }]
    scale_down = [n - 12 for n in BASE_DIATONIC]
    scale_up   = [n + 12 for n in BASE_DIATONIC]
    for i in range(0, len(keys)):
      map[str(i)] = (i, 0, [0], BASE_DIATONIC)
      map[str(i - 12)] = (i - 12, 0, [0], BASE_DIATONIC)
      map[str(i + 12)] = (i + 12, 0, [0], BASE_DIATONIC)
      map[str(i - 24)] = (i - 24, 0, [0], BASE_DIATONIC)
      map[str(i + 24)] = (i + 24, 0, [0], BASE_DIATONIC)
      map[str(i) + "-"] = (i, 0, [-12], scale_down)
      map[str(i) + "+"] = (i, 0, [ 12], scale_up)
      for numeral in keys[i]:
        for type in types:
          for name, info in type.items():
            (intervals, scale) = info
            intervals = sorted(intervals)
            chord_root = intervals[0] % 12
            sc = set([n % 12 for n in BASE_DIATONIC])\
                 .intersection([(n + chord_root) % 12 for n in BASE_DIATONIC])\
                 .union([i % 12 for i in intervals])
            scale = sorted(list(sc)) # overwrite scale here NOTICE!
            map[numeral + name] = (i, chord_root, intervals, scale)
          numeral = numeral.lower()
    self.map = map

  def from_symbol(self, symbol):
    if symbol == None or len(symbol) == 0:
      raise RuntimeError("Symbol " + symbol + " is None or empty")
    if ',' in symbol:
      symbols = symbol.split(',')
      this_root = None
      this_chord_root = None
      this_intervals = []
      this_scale = []
      for s in symbols:
        (root, chord_root, intervals, scale) = self.from_symbol(s)
        if this_root == None:
          this_root = root
        if this_chord_root == None:
          this_chord_root = chord_root
        this_intervals = this_intervals + intervals
        this_scale = this_scale + scale
      return (this_root, this_chord_root, this_intervals, this_scale)
    if symbol.startswith('@'):
      return self.from_symbol(symbol[1:])
    if symbol not in self.map:
      raise RuntimeError("Unrecognized symbol " + symbol)
    return self.map[symbol]

  @staticmethod
  def safe_symbol(symbol, sharp = '#'):
    map = { '♭' : 'b', '♯' : sharp, '°' : 'o' }
    for key, value in map.items():
      symbol = symbol.replace(key, value)
    return symbol

def _test_interpolate():
  a = SCALE_DIATONIC_C_LIST
  b = SCALE_DIATONIC_FSH_LIST
  c = interpolate(a, b, SCALE_CHROMATIC, True)
  print("A     : " + str(a))
  print("INTERP: " + str(c))
  print("B     : " + str(b))

def _test_chords():
  c = Chords()
  print(c.from_symbol('♭vii°7'))
  
if __name__ == '__main__':
  _test_interpolate()
  _test_chords()
