#!/usr/local/bin/python3
# coding=utf-8

CHORDS_MINOR_ANDALUSIAN   = ['i', 'VII', 'VI', 'V']
CHORDS_MINOR_MIXOLYDIAN   = ['I', '♭VII', 'IV', 'V']
CHORDS_MINOR_YOUSTINK     = ['vi', 'V', 'IV', 'V']
CHORDS_MINOR_PENTATONIC_A = ['i', 'III', 'IV', 'VI']
CHORDS_MINOR_PENTATONIC_B = ['i', 'III', 'iv', 'VI']
CHORDS_MINOR_RIFF31       = ['vi', 'I', 'IV', 'V']
CHORDS_MINOR_RIFF31_2B    = ['vi', 'I', 'IV', 'ii', 'iii', 'V']
CHORDS_MINOR_HARMONIC     = ['i', 'iv', 'V', 'V7']
CHORDS_CIRCLE_MAJOR       = ['I', 'IV', 'vii°', 'iii', 'vi', 'ii', 'V']
CHORDS_CIRCLE_MINOR       = ['i', 'iv', '♭VII', 'III', '♭VI', 'ii°', 'V']
CHORDS_NEOPOLITAN         = ['IMaj7', '♭II', '♯IV7', 'V7']

CHORDS_NOTMAKEITSO        = ['vi', 'ivMaj7', 'I7', 'IVMaj7', 'III7', 'vi7', 'ii7', 'V7', 'IMaj7', 'I']
CHORDS_QUIXOTE_1          = ['I', 'V', 'V', 'I', 'I', 'V', 'IV', 'ii7', 'V']

CHORDS_EYESSOBLUE         = ['IMaj7', '♭ii°7', 'ii7', 'V7']
CHORDS_EYESSOBLUE_CHORUS  = ['I', 'iii', 'IV', 'V']
CHORDS_MINOR              = ['vi', 'vi7', 'iii7', 'vi', 'vi7', 'ii7', 'v7']
CHORDS_GLISTEN            = ['I', 'ii', 'II7', 'vi7/-2', 'V/-1', 'V7/-2']
CHORDS_COLTRANE1          = ['iii7', 'IV7', 'VIIMaj7', '♭II7', '♭VMaj7', 'VI7', 'IIMaj7', 'ii7', '♭III7', '♭VIMaj7', 'VII7', 'IIIMaj7', 'V7', 'IMaj7']
CHORDS_COLTRANE1_9TH      = ['I9', 'iii9', 'IV9', 'VIIMaj7', '♭II9', '♭VMaj7', 'VI9', 'IIMaj7', 'ii9', '♭III9', '♭VIMaj7', 'VII9', 'IIIMaj7', 'V9', 'IMaj7']

CHORDS_STANDARD_POP       = ['I', 'vi', 'IV', 'V']
CHORDS_STANDARD_POP_LONG  = ['I', 'iii', 'vi', 'vi', 'IV', 'ii', 'V', 'V7']
CHORDS_LETITBE            = ['I', 'IV', 'vi', 'V']
CHORDS_STANDARD_POP7      = ['IMaj7', 'vi', 'IV', 'V7']
CHORDS_STANDARD_POP_2     = ['I', 'ii', 'vi', 'V']
CHORDS_JPOP               = ['IV', 'V', 'iii', 'vi']
CHORDS_JPOP2              = ['ii', 'V', 'iii', 'vi']
CHORDS_JPOP_MINOR         = ['ii', 'V', 'I', 'vi']
CHORDS_ANOTHER            = ['i', '♭VI', '♭VII', 'iii']
CHORDS_CANON              = ['I', 'V', 'vi', 'iii', 'IV', 'I', 'IV', 'V']
CHORDS_ROLLINGSTONE       = ['I', 'ii', 'iii', 'IV', 'V', 'IV', 'iii', 'ii', 'I']

CHORDS_OTHER              = ['I', 'ii7', 'vi', 'iii7']#, 'I', 'IV', 'V']
CHORDS_WALKAFTERYOU       = ['I', 'ii', 'IV', 'iii7']
CHORDS_MISUNDERSTAND      = ['I', 'I', 'ii', 'ii', 'iii7', 'IV6', 'vi', 'V']

CHORDS_MINOR              = ['vi', 'vi7', 'iii7', 'vi', 'vi7', 'ii7', 'v7']
CHORDS_GLISTEN            = ['I', 'ii', 'II7', 'vi7/-2', 'V/-1', 'V7/-2']
CHORDS_MOSTLY_MINOR       = ['I', 'ii', 'iii7', 'ii7', 'vi', 'V7/-2']
CHORDS_MIRABEL            = ['I9']
CHORDS_MIRABEL_2          = ['vi9/-2']

def _double_chords(chords):
  copy = []
  for c in chords:
    copy.extend([c, c])
  return copy
  
CURRENT_PROGRESSIONS_SHORT = [
  CHORDS_MINOR_ANDALUSIAN,
  CHORDS_MINOR_MIXOLYDIAN,
  CHORDS_MINOR_YOUSTINK,
  CHORDS_MINOR_PENTATONIC_A,
  CHORDS_MINOR_PENTATONIC_B,
  CHORDS_MINOR_RIFF31,
  CHORDS_MINOR_HARMONIC,
  CHORDS_NEOPOLITAN,
  CHORDS_EYESSOBLUE,
  CHORDS_EYESSOBLUE_CHORUS,
  CHORDS_STANDARD_POP,
  CHORDS_LETITBE,
  CHORDS_STANDARD_POP7,
  CHORDS_STANDARD_POP_2,
  CHORDS_JPOP,
  CHORDS_JPOP2,
  CHORDS_JPOP_MINOR,
  CHORDS_ANOTHER,
  CHORDS_OTHER,
  CHORDS_WALKAFTERYOU
]

CURRENT_PROGRESSIONS_LONG = [
  CHORDS_COLTRANE1,
  CHORDS_COLTRANE1_9TH,
  CHORDS_STANDARD_POP_LONG,
  CHORDS_MINOR_RIFF31_2B,
  CHORDS_CIRCLE_MAJOR,
  CHORDS_CIRCLE_MINOR,
  CHORDS_ROLLINGSTONE,
  CHORDS_CANON,
  CHORDS_QUIXOTE_1,
  CHORDS_NOTMAKEITSO
]

ALL_PROGRESSIONS = CURRENT_PROGRESSIONS_LONG
for p in CURRENT_PROGRESSIONS_SHORT:
  ALL_PROGRESSIONS.extend([p, _double_chords(p)])
  
CURRENT_PROGRESSIONS = ALL_PROGRESSIONS

#CURRENT_PROGRESSIONS = [_double_chords(CHORDS_STANDARD_POP), _double_chords(CHORDS_LETITBE)]
CURRENT_PROGRESSIONS = [CHORDS_EYESSOBLUE, _double_chords(CHORDS_EYESSOBLUE), CHORDS_EYESSOBLUE_CHORUS, _double_chords(CHORDS_EYESSOBLUE_CHORUS)]
