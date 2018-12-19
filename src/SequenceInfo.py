#!/usr/local/bin/python3
# coding=utf-8

class SequenceInfo (object):

  def __init__(self, duration = None):
    self.duration = duration

  def is_valid(self):
    return not None in [self.duration]

  def parse(self, text):
    # format: D<template duration in 16ths>
    pieces = text.strip().split(':')
    if len(pieces) == 0:
      return None
    if pieces[0] == '#':
      return None # comment
    for p in pieces:
      if p.startswith('D'):
        self.duration = p[len('D'):]
    if self.duration != None: self.duration = float(self.duration)
    return self
    
  def stretch(self, factor):
    self.duration = float(self.duration * factor)
    return self

  def format(self):
    keys = ['D']
    map = { 'D' : self.duration }
    parts = []
    for key in keys:
      parts.append(key + str(map[key]))
    return ':'.join(parts)
