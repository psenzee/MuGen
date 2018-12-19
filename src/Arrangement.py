#!/usr/local/bin/python3
# coding=utf-8

import Dynamics
import Articulation
import copy
import random
from instruments import get_gm_instrument_name
from Utils import copy_whole_object

class Arrangement (object):

  def __init__(self):
    self._initialize()
    
  def copy(self):
    chs = Channels()
    chs.articulation = copy_whole_object(self.articulation)
    chs.dynamics = copy_whole_object(self.dynamics)
    chs.tracks = copy_whole_object(self.tracks)
    chs.gm_programs = copy_whole_object(self.gm_programs)
    chs.track_names = copy_whole_object(self.track_names)
    return chs

  def set_channel_should_post_transform(self, channel, transform):
    self.should_post_transform[channel] = transform
    return self
    
  def get_channel_should_post_transform(self, channel):
    if channel in self.should_post_transform:
      return self.should_post_transform[channel]
    return False
    
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

  def apply_basic(self, channel, note, time, duration, volume):
    dynamics = self.get_channel_dynamics(channel)
    if dynamics != None:
      volume = dynamics.volume_in_range(volume)
    #articulation = self.get_channel_articulation(channel)
    #if articulation != None:
    #  duration = articulation.note_duration(duration)
    return (note, time, duration, volume)

  def apply(self, channel, note, time, duration, volume):
    dynamics = self.get_channel_dynamics(channel)
    if dynamics != None:
      volume = dynamics.volume_at_time(time, volume)
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
    return self
