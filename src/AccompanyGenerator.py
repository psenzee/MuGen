#!/usr/local/bin/python3
# coding=utf-8

import math
import random

from Transforms import *
from Event import Event
from TemplateGenerator import TemplateGenerator
from MusicUtils import *

"""The finale measures of the first movement of Ravel's Piano Concerto in G feature the harmonization of a descending hybrid scale (phrygo-major). In this special case, Ravel used a parallel series of major triads to brilliant effect.:(G F♯ E D C B♭ A♭ G)"""

TEMPLATE_MIRABEL_9TH  = "-D16 | X.0:T0:D4:o-1 X.0,1:T0:D2:o+1 X.2:T2:D2 | X.2:T4:D4:o-2 X.0,1:T4:D2:o+1 X.3,4:T6:D4 | X.3:T8:D4:o-2 X.2:T10:D2 | X.2:T12:D4:o-2 X.3,4:T12:D4 X.2:T14:D2"
TEMPLATE_MIRABEL_9TH  = "-D16 | X.0:T0:D4:o-1 X.0,1:T0:D2:o+1 X.2:T2:D2 | X.2:T4:D4:o-2 X.0,1:T4:D2:o+1 X.3,4:T6:D4 | X.3:T8:D4:o-2 X.2:T10:D2 | X.2:T12:D4:o-2 X.3,4:T12:D4 X.2:T14:D2"

TEMPLATE_BASS_1 =  " -D16 | X.0:T0:D10:o-2 X.2:T10:D2:o-2 X.0:T12:D4:o-1 "
TEMPLATE_BASS_1 =  " -D16 | X.0:T0:D10:o-2 X.1:T10:D2:o-2 X.2:T12:D4:o-2 "

TEMPLATE_BASS_1_PART1 =  " X.0:T0:D10:o-2 "
TEMPLATE_BASS_1_PART2 =  "  X.1:T2:D2:o-2 X.2:T4:D4:o-2 "

TEMPLATE_BASS_16_1 =  " X.0:T0:D10:o-2 Z.1:T10:D2:o-2 W.2:T12:D4:o-2 "
TEMPLATE_BASS_16_2 =  " X.0:T0:D4:o-2 Y.0:T4:D4:o-2 Z.0:T8:D4:o-2 W.0:T12:D4:o-2 "

TEMPLATE_BASS_1_2 = " -D16 | X.0:T0:D10:o-2 X.1:T10:D2:o-2 X.2:T12:D4:o-2 | X.0:T0:D10:o-1 X.1:T10:D2:o-1 X.2:T12:D4:o-1 "

TEMPLATE_BASS_2 =  " -D16 | X.*:T0:D2:o-2 X.*:T2:D6:o-2 X.*:T6:D2:o-2 X.*:T8:D6:o-2 X.*:T14:D2:o-2 "

TEMPLATE_BASS_RAINING_UP =  "X.0♭:T0:D2:o-2 X.0:T2:D6:o-2"
TEMPLATE_BASS_RAINING_DN =  "X.3♯♯:T0:D2:o-2 X.3:T2:D6:o-2"

class AccompanyGenerator (TemplateGenerator):

  def __init__(self, transform, templates, label_count = 2, period = 2):
    templates = xyzw_map_by_chord_count(label_count, templates)
    super().__init__(transform, templates, label_count, period, 0)
    
  @staticmethod
  def none(octave = -2, transform = NullTransform()):
    t = " -D16 | "
    return AccompanyGenerator(transform, [t])
    print("ACCOMP none")

  @staticmethod  
  def bass_syncopated_1(octave = -2, transform = NullTransform()):
    t = " -D16 | {a}.0:T0:D10:c1[oa] {c}.1:T10:D2:c1[oa] {d}.2:T12:D4:c1[oa] "
    return AccompanyGenerator(transform, [template_indices(t, [0], [octave])]).set_name("ACCOMP bass_syncopated_1")

  @staticmethod
  def bass_syncopated_2(octave = -2, transform = NullTransform()):
    t = " -D16 | {a}.0:T0:D2:c1[oa] {b}.0:T2:D6:c1[oa] {c}.1:T8:D2:c1[oa] {d}.2:T10:D6:c1[oa] "
    return AccompanyGenerator(transform, [template_indices(t, [0], [octave])]).set_name("ACCOMP bass_syncopated_2")

  @staticmethod
  def bass_eights(indices = [0, 0, 0, 0, 0, 0, 0, 0], octaves = [-2, -2, -2, -2, -2, -2, -2, -2], transform = NullTransform()):
    t = " -D16 | {a}.[a]:T0:D2:c1[oa] {a}.[b]:T2:D2:c1[ob]  {b}.[c]:T4:D2:c1[oc]  {b}.[d]:T6:D2:c1[od] " + \
        "        {c}.[e]:T8:D2:c1[oe] {c}.[f]:T10:D2:c1[of] {d}.[g]:T12:D2:c1[og] {d}.[h]:T14:D2:c1[oh]"
    return AccompanyGenerator(transform, [template_indices(t, indices, octaves)]).set_name("bass_eights")

  @staticmethod
  def alberti(octave = 0, transform = NullTransform()):
    t = " -D16 | {a}.0:T0:D2:c0[oa] {a}.1:T2:D2:c0[oa]  {b}.2:T4:D2:c0[oa]  {b}.1:T6:D2:c0[oa] " + \
        "        {a}.0:T0:D4:c1:o-2 {b}.1:T4:D4:c1:o-2 {c}.0:T8:D4:c1:o-2 {d}.1:T12:D4:c1:o-2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [octave])]).set_name("ACCOMP alberti")
    
  @staticmethod
  def arpeggio(octave = 0, transform = NullTransform()):
    t = " -D16 | {a}.0:T0:D2[oa] {a}.2:T2:D2[oa]  {b}.1:T4:D2[oa]  {b}.2:T6:D2[oa] " + \
        "        {c}.0:T8:D2[oa] {c}.2:T10:D2[oa] {d}.1:T12:D2[oa] {d}.2:T14:D2[oa] " + \
        "        {a}.0:T0:D4:c1:o-2 {b}.1:T4:D4:c1:o-2 {c}.0:T8:D4:c1:o-2 {d}.1:T12:D4:c1:o-2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [octave])]).set_name("ACCOMP arpeggio")

  @staticmethod
  def block_chords_fours(octave = 0, transform = NullTransform()):
    t = " -D16 | {a}:T0:D4[oa] {b}:T4:D4[oa] {c}:T8:D4[oa] {d}:T12:D4[oa] " + \
        "        {a}.0:T0:D4:c1:o-2 {b}.1:T4:D4:c1:o-2 {c}.0:T8:D4:c1:o-2 {d}.1:T12:D4:c1:o-2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [octave])]).set_name("ACCOMP block_chords_fours")
    
  @staticmethod
  def block_chords_eights(octave = 0, transform = NullTransform()):
    t = " -D16 | {a}:T0:D2[oa] {a}:T2:D2[oa] {b}:T4:D2[oa] {b}:T6:D2[oa] {c}:T8:D2[oa] {c}:T10:D2[oa] {d}:T12:D2[oa] {d}:T14:D2[oa]" + \
        "        {a}.0:T0:D4:c1:o-2 {b}.1:T4:D4:c1:o-2 {c}.0:T8:D4:c1:o-2 {d}.1:T12:D4:c1:o-2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [octave])]).set_name("ACCOMP block_chords_eights")

  @staticmethod
  def bass_fours(indices = [0, 0, 0, 0], octaves = [-2, -2, -2, -2], transform = NullTransform()):
    t = " -D16 | {a}.[a]:T0:D4:c1[oa] {b}.[b]:T4:D4:c1[ob] {c}.[c]:T8:D4:c1[oc] {d}.[d]:T12:D4:c1[od] "
    return AccompanyGenerator(transform, [template_indices(t, indices, octaves)]).set_name("ACCOMP bass_fours")

  @staticmethod
  def bass_twos(indices = [0, 0, 0, 0], octaves = [-2, -2, -2, -2], transform = NullTransform()):
    t = " -D16 | {a}.0:T0:D8:c1[oa] {c}.0:T8:D8:c1[oc] "
    return AccompanyGenerator(transform, [template_indices(t, indices, octaves)]).set_name("ACCOMP bass_twos")

  @staticmethod
  def salsa_1(transform = NullTransform()):
    t = " -D16 | {a}.0:T0:D1 {a}.1:T1:D1 {a}.0,2:T2:D2 {b}.0:T4:D4 {c}.1:T10:D4 {d}.2:T14:D2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [0])]).set_name("ACCOMP salsa_1")

  @staticmethod
  def salsa_2(transform = NullTransform()):
    t = " -D16 | {a}.2:T2:D4 {b}.0,1:T6:D2 {c}.1:T10:D4 {d}.0:T14:D2"
    return AccompanyGenerator(transform, [template_indices(t, [0], [0])]).set_name("ACCOMP salsa_2")
    
  @staticmethod
  def salsa_3(transform = NullTransform()):
    t = " -D16 | {a}.1:T0:D2 {a}.0,2:T2:D2 {b}.0:T4:D4 {c}.1:T10:D4 {d}.2:T14:D2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [0])]).set_name("ACCOMP salsa_3")
    
  @staticmethod
  def mirabelle(transform = NullTransform()):
    t = "-D16 | {a}.0:T0:D4:o-1:c1 {a}.0,1:T0:D2:o+1 {a}.2:T2:D2 | {b}.2:T4:D4:o-2:c1 {b}.0,1:T4:D2:o+1 {b}.3,4:T6:D4 | {c}.3:T8:D4:o-2:c1 {c}.2:T10:D2 | {d}.2:T12:D4:o-2:c1 {d}.3,4:T12:D4 {d}.2:T14:D2"
    return AccompanyGenerator(transform, [template_indices(t, [0], [0])]).set_name("ACCOMP mirabelle")

  @staticmethod
  def bass_boardwalk(octave = -2, transform = NullTransform()):
    t = " -D16 | {a}.0:T0:D6:c1[oa] {c}.1:T6:D6:c1[oa] {d}.2:T12:D4:c1[oa] "
    return AccompanyGenerator(transform, [template_indices(t, [0], [octave])]).set_name("ACCOMP bass_boardwalk")
    
  @staticmethod
  def bass_cabaret(octave = -2, transform = NullTransform()):
    t = " -D16 | {a}.0:T0:c1:D4[oa] {b}.0,1:T4:D2:c1:o-1 {b}.0,1:T6:D2:c1:o-1 {c}.2:T8:D4:c1[oa] {d}.0,1:T12:D4:c1:o-1 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [octave])]).set_name("ACCOMP bass_cabaret")

  @staticmethod
  def cabaret(transform = NullTransform()):
    t = " -D16 | {a}.0:T0:c1:D4:o-2 {b}.0,1,2:T4:D2:c0:o0 {b}.0,1,2:T6:D2:c0 {c}.2:T8:D4:c1:o-2 {d}.0,1,2:T12:D4:c0 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [0])]).set_name("ACCOMP cabaret")
    
  @staticmethod
  def drums_1(transform = NullTransform()):
    t = " -D16 | @0:T0:D4:c3:o-2 @2:T4:D4:c3:o-2 @0:T8:D4:c3:o-2 @2:T12:D4:c3:o-2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [0])]).set_name("drums_1")
    
  @staticmethod
  def drums_2(transform = NullTransform()):
    t = " -D16 | @0:T0:D4:c3:o-2 @2:T4:D4:c3:o-2 @0:T8:D4:c3:o-2 @0:T12:D4:c3:o-2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [0])]).set_name("drums_2")
    
  @staticmethod
  def drums_3(transform = NullTransform()):
    t = " -D16 | @0:T0:D4:c3:o-2 @2:T4:D4:c3:o-2 @0:T10:D2:c3:o-2 @0:T12:D4:c3:o-2 "
    return AccompanyGenerator(transform, [template_indices(t, [0], [0])]).set_name("drums_3")

  @staticmethod
  def bass_octave_eights(indices = [0, 0, 0, 0, 0, 0, 0, 0], octaves = [-1, -2, -1, -2, -1, -2, -1, -2], transform = NullTransform()):
    return AccompanyGenerator.bass_eights(indices, octaves, transform).set_name("ACCOMP bass_octave_eights")
    
  @staticmethod
  def bass_alternate_eights(indices = [0, 2, 0, 2, 0, 2, 0, 2], octaves = [-1, -2, -1, -2, -1, -2, -1, -2], transform = NullTransform()):
    return AccompanyGenerator.bass_eights(indices, octaves, transform).set_name("ACCOMP bass_alternate_eights")

  @staticmethod
  def bass_octave_fours(indices = [0, 0, 0, 0], octaves = [-1, -2, -1, -2], transform = NullTransform()):
    return AccompanyGenerator.bass_fours(indices, octaves, transform).set_name("ACCOMP bass_octave_fours")
    
  @staticmethod
  def bass_alternate_fours(indices = [0, 2, 0, 2], octaves = [-1, -2, -1, -2], transform = NullTransform()):
    return AccompanyGenerator.bass_fours(indices, octaves, transform).set_name("ACCOMP bass_alternate_fours")
