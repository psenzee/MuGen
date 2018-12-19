#!/usr/local/bin/python3
# coding=utf-8

from Event import Event
from Transforms import Transform

# basic utility transforms
class FinalizeEventsTransform (Transform):

  def transform(self, events):
    return Event.clean_all(events)
