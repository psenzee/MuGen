#!/usr/local/bin/python3
# coding=utf-8

import random
from Event import *

# the interface
class Transform (object):

  def transform(self, obj):
    return obj
    
# same as base
class NullTransform (Transform):
  pass

class ChainTransform (Transform):

  def __init__(self):
    self.transforms = []
    
  def add(self, transforms):
    self.transforms.extend([t for t in transforms if t is not None])
    return self

  def transform(self, obj):
    for t in self.transforms:
      obj = t.transform(obj)
    return obj
