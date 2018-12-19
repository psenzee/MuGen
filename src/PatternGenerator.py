#!/usr/local/bin/python3
# coding=utf-8

from TemplateGenerator import RandomTemplateGenerator
  
class PatternGenerator (RandomTemplateGenerator):

  def __init__(self, transform, provider, period = 2, octave = 0):
    super().__init__(transform, provider.create_set(), provider.get_label_count(), period, octave)
    self.provider = provider
