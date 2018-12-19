#!/usr/local/bin/python3
# coding=utf-8

import math
import random
import time
import os
from instruments import get_gm_instrument_name

# https://en.wikipedia.org/wiki/General_MIDI

GM_CHANNEL_DRUMS = 10
GM_CHANNEL_COUNT = 16
GM_INSTRUMENT_DEFAULT = 0
GM_INSTRUMENT_DRUMS = 118
GM_INSTRUMENT_BLACKLIST = [26, 27, 28, 29, 30, 31, 47, 62, 63, 64, 65, 66, 67, 81, 82, 83, 84, 85, 86, 87, 112, 113, 114, 115, 116, 117, 118, 119]
GM_INSTRUMENT_BASS = [0, 1, 2, 16, 17, 18, 19, 20, 32, 33, 34, 35, 36, 37, 42, 43, 57, 58]

LOCAL_CHANNEL_COUNT  = 6

LOCAL_CHANNEL_ACCOMP = 0
LOCAL_CHANNEL_BASS   = 1
LOCAL_CHANNEL_LEAD   = 2
LOCAL_CHANNEL_DRUMS  = 3

SPECIAL_CHANNELS = [LOCAL_CHANNEL_ACCOMP, LOCAL_CHANNEL_BASS, LOCAL_CHANNEL_DRUMS]

class InstrumentRoles (object):
  
  def __init__(self):
    self._role_names = ['ROLE%02d' % c for c in range(0, GM_CHANNEL_COUNT)]
    named = ['ACCOMP', 'BASS', 'LEAD', 'DRUMS']
    for i in range(0, len(named)):
      self._role_names[i] = named[i]
    self._role_gm_instruments = {}
    for i in range(0, GM_CHANNEL_COUNT):
      self._role_gm_instruments[self._role_names[i]] = self._assign_gm_instrument(i)
    self._channel_remap = [i for i in range(0, 16)]
    self._channel_remap[LOCAL_CHANNEL_DRUMS] = GM_CHANNEL_DRUMS
    self._channel_remap[GM_CHANNEL_DRUMS] = LOCAL_CHANNEL_DRUMS
    self._channel_count = LOCAL_CHANNEL_COUNT
   
  def get_channel_count(self):
    return LOCAL_CHANNEL_COUNT

  def get_gm_channel(self, local_channel):
    if not local_channel in self._channel_remap:
      return local_channel
    return self._channel_remap[local_channel]
    
  def get_gm_instrument(self, local_channel):
    role_name = self.get_role_name(local_channel)
    if role_name == None:
      return GM_INSTRUMENT_DEFAULT
    return self._role_gm_instruments[role_name]

  def get_gm_instrument_name(self, local_channel):
    gm_program = self.get_gm_instrument(local_channel)
    if gm_program == None:
      return None
    return get_gm_instrument_name(gm_program)

  def get_role_name(self, local_channel):
    if local_channel >= len(self._role_names):
      return None
    return self._role_names[local_channel]

  def print_map(self):
    for i in range(0, GM_CHANNEL_COUNT):
      print("%02d : %10s : GM CH %02d : INS %03d %s" % (
        i,
        self.get_role_name(i),
        self.get_gm_channel(i),
        self.get_gm_instrument(i),
        self.get_gm_instrument_name(i)))

  # private
  
  @staticmethod
  def _assign_gm_instrument(local_channel):
    if local_channel in [GM_CHANNEL_DRUMS, LOCAL_CHANNEL_DRUMS]:
      return GM_INSTRUMENT_DRUMS
    if local_channel == LOCAL_CHANNEL_BASS: #bass
      return random.choice(GM_INSTRUMENT_BASS)
    ins = random.randrange(0, 127)
    while ins in GM_INSTRUMENT_BLACKLIST:
      ins = random.randrange(0, 127)
    return ins
    
def _test():
  ir = InstrumentRoles()
  ir.print_map()

if __name__ == '__main__':
  _test()
  