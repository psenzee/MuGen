#!/usr/local/bin/python3
# coding=utf-8

import random
import copy
import math
import Utils

SWING_STRENGTH = 0.0 #0.125
SWING_EIGHTH = 1.0 / 4.0
SWING_QUARTER =  1.0 / 8.0
SWING_FREQ = SWING_QUARTER

PI = 3.141592653589793
PI2 = PI * 2.0

def swing(time):
  t = time + (math.cos(time * PI2 * SWING_FREQ - PI) + 1) * SWING_STRENGTH
  return t
