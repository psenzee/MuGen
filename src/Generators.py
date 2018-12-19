#!/usr/local/bin/python3
# coding=utf-8

# the interface
class Generator (object):

  def options(self):
    return {}
    
  def labels(self):
    return []
    
  def duration(self):
    return 0

  def next(self):
    return None

class GroupGenerator (Generator):

  def __init__(self):
    super().__init__()
    self.generators = []
    
  def add(self, generators):
    self.generators.extend([g for g in generators if g is not None])
    return self
    
  def options(self):
    opts = {}
    for g in self.generators:
      opts.update(g.options())
    return opts
    
  def labels(self):
    labs = []
    for g in self.generators:
      labs = labs + g.labels()
    return list(set(labs))
    
  def max_duration(self):
    dur = 0
    for g in self.generators:
      dur = max(dur, g.duration())
    return dur
    
  def sum_duration(self):
    dur = 0
    for g in self.generators:
      dur = dur + g.duration()
    return dur

  def next_list(self):
    return [g.next() for g in self.generators]

class ConcatenateGenerator (GroupGenerator):

  def __init__(self):
    super().__init__()

  def duration(self):
    return self.sum_generator()

  def next(self):
    # todo process the time
    return None
    
class StackGenerator (GroupGenerator):

  def __init__(self):
    super().__init__()

  def duration(self):
    return self.max_duration()

  def next(self):
    return ' | '.join(self.next_list())
