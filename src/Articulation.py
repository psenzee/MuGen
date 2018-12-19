#!/usr/local/bin/python3
# coding=utf-8

import math

class Articulation (object):

  def __init__(self, factor = 1.0):
    self.articulation_factor = factor
    
  def copy(self):
    a = Articulation(self.articulation_factor)
    return a

  def set_articulation_factor(self, factor):
    self.articulation_factor = factor
    return self

  def set_staccatissimo(self):
    return self.set_articulation_factor(0.25)
    
  def set_staccato(self):
    return self.set_articulation_factor(0.5)

  def set_legato(self):
    return self.set_articulation_factor(2.0)
    return self
    
  def set_legatissimo(self):
    return self.set_articulation_factor(4.0)

  def note_duration(self, duration):
    return duration * self.articulation_factor
