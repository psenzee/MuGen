#!/usr/local/bin/python3
# coding=utf-8

import math
import random
import midiutil
import time

from Chord import *
from Track import *
from Event import *
from SplitTransform import *
from MelodyTransform import *
from Melody2Transform import *
from FinalizeEventsTransform import *
from Transforms import *
from Generators import *
from PatternGenerator import *
from SimplePatternProvider import *
from AccompanyGenerator import *
from OrnamentTransforms import *
from InstrumentRoles import SPECIAL_CHANNELS
from progressions import CURRENT_PROGRESSIONS

NO_TRACKS = 6

def generate_track(root, chords, generator, times = 4):
  mf = Track(root).open(NO_TRACKS)
  for channel in range(0, NO_TRACKS):
    mf.set_dynamics(channel, random.choice([4, 6, 8, 16, 32, 64, 128, 256, 512]), 1.0, random.uniform(0, 1))
    mf.get_arrangement().set_channel_swing(channel, 0.25)
  mf.set_base_chords(chords)
  mf.generate(generator, chords * times)
  mf.save()

def random_drum_generator():
  return random.choice([
    AccompanyGenerator.drums_1(),
    AccompanyGenerator.drums_2(),
    AccompanyGenerator.drums_3()
  ]) 

def random_accomp_generator():
  return random.choice([
    AccompanyGenerator.bass_syncopated_1(),
    AccompanyGenerator.bass_syncopated_2(),
    AccompanyGenerator.bass_boardwalk(),
    AccompanyGenerator.salsa_1(),
    AccompanyGenerator.salsa_2(),
    AccompanyGenerator.salsa_3(),
    AccompanyGenerator.cabaret(),
    AccompanyGenerator.bass_fours(),
    AccompanyGenerator.bass_octave_fours(),
    AccompanyGenerator.bass_alternate_fours(),
    AccompanyGenerator.bass_eights(),
    AccompanyGenerator.bass_octave_eights(),
    AccompanyGenerator.bass_alternate_eights(),
    AccompanyGenerator.none(),
    AccompanyGenerator.mirabelle(),
    AccompanyGenerator.block_chords_fours(),
    AccompanyGenerator.block_chords_eights(),
    AccompanyGenerator.arpeggio(),
    AccompanyGenerator.alberti(),
    AccompanyGenerator.bass_twos()
  ])
  
def random_dual_accomp_generator():
  return StackGenerator().add([random_accomp_generator(), random_accomp_generator()])
  
def random_ornament_transform():
  count = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11])
  return random.choice([
    GraceTransform().set_direction('`♯'),
    GraceTransform().set_direction('`♭'),
    GraceTransform().set_direction('`♯').set_note_duration(1),
    GraceTransform().set_direction('`♭').set_note_duration(1),
    GlissandoTransform().set_direction('`♭').set_count(count),
    GlissandoTransform().set_direction('`♯').set_count(count),
    GlissandoTransform().set_direction('`♯').set_note_duration(1).set_count(count),
    GlissandoTransform().set_direction('`♭').set_note_duration(1).set_count(count),
    RingTransform(),
    MordentTransform(),
    TurnTransform(),
    DoubleTurnTransform(),
    TrillTransform().set_count(count),
  ])
  
def random_composite_generator(track_num):
  if track_num in SPECIAL_CHANNELS: # Not for the special ones
    return None
  repeat_every = random.choice([1, 2, 4, 8])
  syncopated = random.choice([True, False])
  use_chords = random.choice([True, False])
  swap = 0 #random.randrange(25, 75)
  octave = random.choice([0, 0, 1, -1, 1, -2])
  split_range = random.randrange(25, 100)
  provider = SimplePatternProvider(2, track_num, syncopated)
  return PatternGenerator(ChainTransform().add([
        SplitTransform().set_overall_split_percent(split_range).set_overall_swap_percent(swap),
        random.choice([
          Melody2Transform().set_use_chords(use_chords),
          MelodyTransform().set_use_chords(use_chords)
        ]),
        random.choice([
          Melody2Transform().set_use_chords(not use_chords),
          MelodyTransform().set_use_chords(not use_chords),
          None
        ]),
        random.choice([random_ornament_transform()]),
        FinalizeEventsTransform()
      ]), provider, repeat_every, octave)

def make_stock_generator():
  chain = [random_dual_accomp_generator(), random_drum_generator()]
  for i in range(0, NO_TRACKS):
    chain.append(random_composite_generator(i))
  return StackGenerator().add(chain)

for i in range(0, 200):
  for chords in CURRENT_PROGRESSIONS:
    generate_track(60, chords, make_stock_generator())
  #time.sleep(10)
