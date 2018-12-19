#!/usr/local/bin/python3
# coding=utf-8

import math
import random
from MusicUtils import *
from PatternProvider import *

def _add_channel(temp, channel):
  if temp == None:
    return temp
  temp = temp.strip()
  if len(temp) != 0 and ':c' not in temp and channel != 0:
    return temp + ':c' + str(channel)
  return temp

def base_templates(count, channel = 0, syncopate = True):
  if count < 1 or not count in [1, 2, 4]:
    raise RuntimeError("Chord count can only be 1, 2 or 4")
  base_ab = [
    ['{a}:T0:D8', ''],
    ['{a}:T0:D4', '{b}:T4:D4']
  ]
  base_ab_sync = [
    ['{a}:T0:D2', '{b}:T2:D6'],
    ['{a}:T0:D6', '{b}:T6:D2']
  ]
  if syncopate:
    base_ab = base_ab + base_ab_sync
  base_bc = [
    ['{b}:T4:D8', ''],
    ['{b}:T4:D4', '{c}:T8:D4'],
    ['{b}:T4:D6', '{c}:T8:D2'],
    ['{b}:T4:D2', '{c}:T8:D6']
  ]
  base_cd = [
    ['{c}:T8:D8', ''],
    ['{c}:T8:D4', '{d}:T12:D4']
  ]
  base_cd_sync = [
    ['{c}:T8:D2', '{d}:T10:D6'],
    ['{c}:T8:D6', '{d}:T14:D2']
  ]
  if syncopate:
    base_cd = base_cd + base_cd_sync
  base_ad = [
    ['{a}:T0:D8', ''],
    ['{a}:T0:D4', '{d}:T12:D4'],
    ['{a}:T0:D2', '{d}:T10:D6'],
    ['{a}:T0:D6', '{d}:T14:D2']
  ]
  templates = []
  if count == 1:
    templates.append('{a}:T0:D16:c%d' % channel)
  for ab in base_ab:
    (a, b) = ab
    for cd in base_cd:
      (c, d) = cd
      templates.append(' '.join([_add_channel(p, channel) for p in [a, b, c, d]]))
  if syncopate:
    for bc in base_bc:
      (b, c) = bc
      for ad in base_ad:
        (a, d) = ad
        templates.append(' '.join([_add_channel(p, channel) for p in [a, b, c, d]]))
  return xyzw_map_by_chord_count(count, templates)

class SimplePatternProvider (PatternProvider):
  
  def create_set(self):
    return base_templates(self.get_label_count(), self.get_channel(), self.get_syncopate())