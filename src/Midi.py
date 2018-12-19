#!/usr/local/bin/python3
# coding=utf-8

import math
import random
import midiutil
import time
import os

from Performance import PERFORMANCE
from Dynamics import *
from InstrumentRoles import *
from Arrangement import Arrangement

# https://en.wikipedia.org/wiki/General_MIDI

class Midi (object):
  
  def __init__(self, channel_count):
    self.initial_time = 0
    self.tempo = 120
    self.duration = 0
    self.file_time = None
    self.filename = None
    self.directory = None
    self.midifile = None
    self.midifile_secondary = None
    self.performance = PERFORMANCE.copy()
    self.instruments = InstrumentRoles()
    self.channel_count = channel_count

  def open(self, filename = None):
    self.midifile = midiutil.MIDIFile(self.channel_count + 1, True, True, False, 1)
    self.midifile_secondary = midiutil.MIDIFile(self.channel_count + 1, True, True, False, 1)
    self.file_time = time.time()
    self.set_filename(filename)
    self.midifile.addTempo(0, 0, self.tempo)
    for i in range(0, self.channel_count + 1):
      self._add_track(i)
    return self
    
  def get_performance(self):
    return self.performance
    
  def get_arrangement(self):
    return self.performance.get_arrangement()
    
  def set_dynamics(self, channel, period, overall = 1.0, offset = 0, min_max = (0, 127)):
    arrangement = self.get_arrangement()
   #arrangement.set_channel_dynamics(channel, Sine1Dynamics(period, overall, offset, min_max))
    arrangement.set_channel_dynamics(channel, Sine2Dynamics(period, overall, offset, min_max))
    return self

  def set_filename(self, filename):
    # TODO strip off .midi, .mid if present
    self.filename = filename
    return self

  def set_directory(self, directory):
    self. directory = directory
    return self

  def set_tempo(self, tempo):
    self.tempo = tempo
    return self
    
  def write_note(self, channel, note, time, duration, volume, time_scale = 0.25):
    perf = self.performance
    track = perf.get_arrangement().get_channel_track(channel)
    (note1, time1, duration1, volume1) = perf.apply(channel, note, time, duration, volume)
    (note2, time2, duration2, volume2) = perf.apply_basic(channel, note, time, duration, volume)
    #print("TRACK " + str(track) + " CHANNEL " + str(channel))
    gm_channel = self.instruments.get_gm_channel(channel)
    if duration1 > 0:
      self.midifile.addNote(track, gm_channel, note1, time1, duration1, int(volume1))
      self.midifile_secondary.addNote(track, gm_channel, note2, time2, duration2, int(volume2))

  def close(self):
    filename1 = "%s%s" % (self.filename, "_%d.midi" % self.file_time)
    filename2 = "%s%s" % (self.filename, "_%d-piano-no-dyn.midi" % self.file_time)
    dir = None
    if self.directory != None:
      dir = self.directory
    if dir != None:
      filepath1 = '/'.join([dir, filename1])
      filepath2 = '/'.join([dir, filename2])
    else:
      filepath1 = '/'.join(filename1)
      filepath2 = '/'.join(filename2)
    print ("WRITING FILE %s" % filepath1)
    with open(filepath1, 'wb') as output:
      self.midifile.writeFile(output)
      output.close()
    print ("WRITING FILE %s" % filepath2)
    with open(filepath2, 'wb') as output:
      self.midifile_secondary.writeFile(output)
      output.close()
    print ("COMPLETE\n\n")
      
  # private

  def _add_track(self, channel):
    role_name = self.instruments.get_role_name(channel)
    arrangement = self.performance.get_arrangement()
    gm_instrument = self.instruments.get_gm_instrument(channel)
    track = arrangement.add_channel_track(channel, role_name, gm_instrument)
    ins_name = arrangement.get_channel_instrument_name(channel)
    self.midifile.addTempo(track, 0, self.tempo)
    self.midifile.addTrackName(track, 0, "MIDI %d %s %s" % (self.file_time, role_name, ins_name))
    self.midifile_secondary.addTempo(track, 0, self.tempo)
    self.midifile_secondary.addTrackName(track, 0, "MIDI %d %s %s" % (self.file_time, role_name, ins_name))
    gm_channel = self.instruments.get_gm_channel(channel)
    # this `track + 1` argument below is due to a bug in the midiutil package:
    self.midifile.addProgramChange(track + 1, gm_channel, 0, gm_instrument) # only the main midi file gets the program change
    if gm_channel != GM_CHANNEL_DRUMS:
      gm_instrument = 0 # the secondary is all piano, except drums
    self.midifile_secondary.addProgramChange(track + 1, gm_channel, 0, gm_instrument) 