#!/usr/local/bin/python3
# coding=utf-8

import random
import copy
import math
import Utils

def value_by_duration(duration, table, default):
  keys = list(table.keys())
  sorted(keys, reverse=True)
  value = default
  for n in keys:
    if duration >= n:
      value = table[n]
      break
  return value

def is_percent_by_duration(duration, table, default = 0, overall = 100):
  percent = value_by_duration(duration, table, default)
  return is_percent(percent * (float(overall) / 100.0))

def shift_index(index, direction, chromatic):
  original = index
  if direction not in [-1, 0, 1]:
    raise RuntimeError('direction must be -1, 0 or 1')
  if direction != 0:
    dir = int(int(direction + 1) / 2)
    if chromatic:
      index = index + ['♭', '♯'][dir]
    else:
      (p, q) = [('-', '+'), ('+', '-')][dir]
      if p in index:
        for i in range(8, 0, -1):
          index = index.replace('%s%d' % (p, i), '%s%d' % (p, i + 1))
      elif q in index:
        index = index.replace(q + '1', '')
        for i in range(2, 10):
          index = index.replace('%s%d' % (q, i), '%s%d' % (q, i - 1))
      else:
        index = index + p + '1'
  return index

def swing(time):
  t = time + (math.cos(time * PI2 * SWING_FREQ - PI) + 1) * SWING_STRENGTH
  return t

def octave_str(octave):
  if not octave:
    return ''
  octave = int(octave)
  if octave > 0:
    return ":o+%d" % int(octave)
  elif octave < 0:
    return ":o%d" % int(octave)
  return ''
  
def xyzw_map_by_chord_count(count, templates):
  if count < 1 or not count in [1, 2, 4]:
    raise RuntimeError("Chord count can only be 1, 2 or 4")
  map = [
    None,
    { 'a' : 'X', 'b' : 'X', 'c' : 'X', 'd' : 'X' },
    { 'a' : 'X', 'b' : 'X', 'c' : 'Y', 'd' : 'Y' },
    None,
    { 'a' : 'X', 'b' : 'Y', 'c' : 'Z', 'd' : 'W' }
  ][count]
  copy = []
  for t in templates:
    for k, v in map.items():
      t = t.replace("{%s}" % k, v)
    copy.append(t)
  return copy

def template_indices(template, indices, octaves):
  labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  for i in range(0, min(len(labels), len(indices), len(octaves))):
    template = template.replace("[%s]" % labels[i], str(indices[i]))
    template = template.replace("[o%s]" % labels[i], octave_str(octaves[i]))
  #print("TEMPLATE0 ", template)
  return template
  
def split_event_symbols(text):
  events = []
  symbols = text.strip().split()
  ignorables = [None, '|', '.', '/']
  for symbol in symbols:
    symbol = symbol.strip()
    if symbol and len(symbol) > 0 and not symbol in ignorables and not symbol.startswith('#'):
      events.append(symbol)
  return events
