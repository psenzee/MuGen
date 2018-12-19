#!/usr/local/bin/python3
# coding=utf-8

import random
from Arrangement import Arrangement
from Utils import copy_whole_object

class Performance (object):

  def __init__(self, dequantize = 0.05, duration = 0.05, volume = 30):
    self.zero()
    self.dequantize = dequantize
    self.volume = volume
    self.duration = duration

  def copy(self):
    p = Performance(self.dequantize, self.duration, self.volume)
    p.arrangement = copy_whole_object(self.arrangement)
    p.resolution = self.resolution
    p.time_scale = self.time_scale
    return p

  def set_time_scale(self, time_scale):
    self.time_scale = time_scale
    return self
    
  def get_arrangement(self):
    return self.arrangement
    
  def zero(self):
    self.arrangement = Arrangement()
    self.dequantize = 0
    self.volume = 0
    self.duration = 0
    self.resolution = 0
    self.time_scale = 0.25
    return self
    
  def apply(self, channel, note, time, duration, volume):
    if self.dequantize != 0:
      time = time + random.uniform(-self.dequantize * 0.5, self.dequantize * 0.5)
    if self.duration != 0:
      duration = duration + random.uniform(-self.duration * 0.75, self.duration * 0.25)
    if self.volume != 0:
      volume = volume + random.uniform(-self.volume * 0.5, self.volume * 0.5)
    chs = self.get_arrangement()
    (note, time, duration, volume) = chs.apply(channel, note, time, duration, volume)
    if time < 0:
      time = 0
    if volume > 127:
      volume = 127
    if volume <= 1:
      volume = int(1)
    if duration <= 0.2:
      duration = int(0)
    if self.resolution != 0:
      time = int(time * self.resolution) / self.resolution
      duration = int(duration * self.resolution) / self.resolution
    return (int(note) % 128, time * self.time_scale, duration * self.time_scale, int(volume))
    
  def apply_basic(self, channel, note, time, duration, volume):
    if self.dequantize != 0:
      time = time + random.uniform(-self.dequantize * 0.5, self.dequantize * 0.5)
    if self.duration != 0:
      duration = duration + random.uniform(-self.duration * 0.75, self.duration * 0.25)
    if self.volume != 0:
      volume = volume + random.uniform(-self.volume * 0.5, self.volume * 0.5)
    chs = self.get_arrangement()
    (note, time, duration, volume) = chs.apply_basic(channel, note, time, duration, volume)
    if time < 0:
      time = 0
    if volume > 127:
      volume = 127
    if volume <= 1:
      volume = int(1)
    if duration <= 0.2:
      duration = int(0)
    if self.resolution != 0:
      time = int(time * self.resolution) / self.resolution
      duration = int(duration * self.resolution) / self.resolution
    return (int(note) % 128, time * self.time_scale, duration * self.time_scale, int(volume))

PERFORMANCE = Performance()