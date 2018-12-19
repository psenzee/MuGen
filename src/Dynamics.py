#!/usr/local/bin/python3
# coding=utf-8

import math
import Utils

PI = 3.141592653589793
PI2 = PI * 2.0

class Dynamics (object):

  def __init__(self, period, overall = 1.0, offset = 0, min_max = (0, 127)):
    self.period = period
    self.overall = overall
    self.offset = offset
    (self.min, self.max) = min_max
    
  def copy(self):
    return Dynamics(self.period, self.overall, self.offset, self.min_max)
    
  def volume_in_range(self, volume):
    return Utils.clamp(volume, max(self.min, 0), min(self.max, 127))

  def volume_at_time(self, time, volume):
    return self.volume_in_range(volume * self.normalized_volume_at_time(time))

  def set_offset(self, offset):
    self.offset = offset
    return self
    
  def normalized_volume_at_time(self, time):
    return self.overall
    
  def test(self):
    periods = [4, 8, 16, 32, 64, 128]
    for period in periods:
      d = self.copy()
      d.period = period
      for i in range(0, 100):
        print ("VALUE (P%d) AT %d: %d" % (period, i, int(d.volume_at_time(i, 100))))

class Sine1Dynamics (Dynamics):

  def copy(self):
    return Sine1Dynamics(self.period, self.overall, self.offset, self.min_max)

  def normalized_volume_at_time(self, time):
    t = (time + self.offset) / self.period
    return Utils.clamp(math.sin(t * PI2) * self.overall, 0.0, 1.0)
    
class Sine2Dynamics (Dynamics):

  def copy(self):
    return Sine2Dynamics(self.period, self.overall, self.offset, self.min_max)

  def normalized_volume_at_time(self, time):
    t = (time + self.offset) / self.period
    return Utils.clamp(((math.sin(t * PI2) + 1) * 0.5) * self.overall, 0.0, 1.0)

if __name__ == '__main__':
  Dynamics(1.0).test()
  Sine1Dynamics(1.0).test()
  Sine2Dynamics(1.0).test()
