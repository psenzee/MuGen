#!/usr/local/bin/python3
# coding=utf-8

import Dynamics
import Articulation
import copy
import random
import math
from instruments import get_gm_instrument_name
from Utils import copy_whole_object

DEFAULT_SWING_STRENGTH = 0.0 #0.125

SWING_EIGHTH = 1.0 / 4.0
SWING_QUARTER =  1.0 / 8.0
SWING_FREQ = SWING_QUARTER

PI = 3.141592653589793
PI2 = PI * 2.0

def _swing(time, strength):
  t = time + (math.cos(time * PI2 * SWING_FREQ - PI) + 1) * strength
  return t

APPLY_NONE         = 0
APPLY_DYNAMICS     = 1
APPLY_ARTICULATION = 2
APPLY_SWING        = 4
APPLY_ALL          = APPLY_DYNAMICS | APPLY_ARTICULATION | APPLY_SWING

class Arrangement (object):

  def __init__(self):
    self._initialize()
    
  def copy(self):
    arrangement = Arrangement()
    arrangement.articulation = copy_whole_object(self.articulation)
    arrangement.dynamics = copy_whole_object(self.dynamics)
    arrangement.tracks = copy_whole_object(self.tracks)
    arrangement.gm_programs = copy_whole_object(self.gm_programs)
    arrangement.track_names = copy_whole_object(self.track_names)
    arrangement.channel_properties = copy_whole_object(self.channel_properties)
    return arrangement

  def set_channel_should_post_transform(self, channel, transform):
    self.should_post_transform[channel] = transform
    return self
    
  def get_channel_should_post_transform(self, channel):
    if channel in self.should_post_transform:
      return self.should_post_transform[channel]
    return False
    
  def set_channel_property(self, channel, key, value):
    if channel not in self.channel_properties:
      self.channel_properties[channel] = {}
    props = self.channel_properties[channel]
    props[key] = value
    return self

  def get_channel_property(self, channel, key):
    if channel in self.channel_properties:
      props = self.channel_properties[channel]
      if key in props:
        return props[key]
    return None

  def set_channel_swing(self, channel, value):
    return self.set_channel_property(channel, '_SWING_STRENGTH', value)
    
  def get_channel_swing(self, channel):
    value = self.get_channel_property(channel, '_SWING_STRENGTH')
    if value == None:
      value = 0.0
    return value

  def set_channel_articulation(self, channel, articulation):
    self.articulation[channel] = articulation
    return self
    
  def get_channel_articulation(self, channel):
    if channel in self.articulation:
      return self.articulation[channel]
    return None

  def set_channel_dynamics(self, channel, dynamics):
    self.dynamics[channel] = dynamics
    return self
    
  def get_channel_dynamics(self, channel):
    if channel in self.dynamics:
      return self.dynamics[channel]
    return None

  def get_channel_track(self, channel):
    if not channel in self.tracks:
      return None
    return self.tracks.index(channel)
    
  def get_channel_track_name(self, channel):
    if not channel in self.gm_programs:
      return None
    return self.gm_programs[channel]

  def get_channel_gm_program(self, channel):
    if not channel in self.gm_programs:
      return None
    return self.gm_programs[channel]
    
  def get_channel_instrument_name(self, channel):
    gm_program = self.get_channel_gm_program(channel)
    return get_gm_instrument_name(gm_program)

  def add_channel_track(self, channel, name, gm_program_number):
    if not channel in self.tracks:
      self.tracks.append(channel)
    index = self.tracks.index(channel)
    self.gm_programs[channel] = gm_program_number
    self.track_names[channel] = name
    return index

  def apply(self, channel, note, time, duration, volume, apply_options = APPLY_ALL):
    dynamics = self.get_channel_dynamics(channel)
    if (apply_options & APPLY_SWING) != 0:
      time = _swing(time, self.get_channel_swing(channel))
    if (apply_options & APPLY_DYNAMICS) != 0:
      if dynamics != None:
        volume = dynamics.volume_in_range(volume)
    else:
      if dynamics != None:
        volume = dynamics.volume_at_time(time, volume)
    if (apply_options & APPLY_ARTICULATION) != 0:
      articulation = self.get_channel_articulation(channel)
      if articulation != None:
        duration = articulation.note_duration(duration)
    return (note, time, duration, volume)

  # private

  def _initialize(self):
    self.articulation = {}
    self.dynamics = {}
    self.tracks = []
    self.gm_programs = {}
    self.track_names = {}
    self.should_post_transform = {}
    self.channel_properties = {}
    return self
