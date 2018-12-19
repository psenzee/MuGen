#!/usr/local/bin/python3
# coding=utf-8

import math
import random
from Utils import *

class PatternProvider (object):

  def __init__(self, label_count = 2, channel = 0, syncopate = True):
    super().__init__()
    self._label_count = label_count
    self._channel = channel
    self._syncopate = syncopate
    
  def set_label_count(self, count):
    self._label_count = count
    return self

  def get_label_count(self):
    return self._label_count

  def set_channel(self, channel):
    self._channel = channel
    return self

  def get_channel(self):
    return self._channel

  def set_syncopate(self, syncopate):
    self._syncopate = syncopate
    return self

  def get_syncopate(self):
    return self._syncopate

  def create_set(self):
    return []
