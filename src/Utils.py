#!/usr/local/bin/python3
# coding=utf-8

import string
import copy
import math
import random
import time
import re
import os
import sys
import shutil
import subprocess

def replace_re(text, find, replace):
  return string.join(re.compile(find, re.M | re.S).split(text), replace)

def distribution_set(map):
  elements = []
  for k, count in map.items():
    if count > 0:
      elements.extend([k] * count)
  return elements

def clamp(value, min, max):
  if value < min:
    value = min
  if value > max:
    value = max
  return value

def any_prefix(text, strs):
  for p in strs:
    if text.startswith(p):
      return p
  return None

def any_suffix(text, strs):
  for p in strs:
    if text.endswith(p):
      return p
  return None
  
def endswith_any(s, strs):   return len([e for e in strs if s.endswith(e)])   != 0
def startswith_any(s, strs): return len([e for e in strs if s.startswith(e)]) != 0
def contains_any(s, strs):   return len([e for e in strs if s.find(e) != -1]) != 0

def is_percent(n):
  if n == 0: # 0 means never
    return False
  if n == 100: # 1 means always
    return True
  return (random.randrange(100) <= (n - 1))

def _copy_dict(map):
  cp = {}
  for k, v in map.items():
    cp[k] = copy_whole_object(v)
  return cp

def _copy_list(ls):
  return [copy_whole_object(e) for e in ls]

def copy_whole_object(v):
  if v == None:
    return v
  elif type(v) is dict:
    return copy_dict(v)
  elif type(v) is list:
    return copy_list(v)
  elif isinstance(v, object):
    try:
      return v.copy()
    except:
      return copy.deepcopy(v)
  return copy.deepcopy(v)

def blank(s):
  return not s or len(s.strip()) == 0
  
def between(s, start, end):
  index = s.find(start)
  if index == -1:
    return None
  s = s[index + len(start):]
  index = s.find(end)
  if index == -1:
    return None
  return s[:index]

def between_any(s, start_list, end):
  for start in start_list:
    result = between(s, start, end)
    if result is not None:
      return result
  return None
  
def dict_value_default(key, dict, default):
  if not key in dict: return default
  return dict[key]

def dict_value(key, dict):
  return dict_value_default(key, dict, None)

def choose(bool_value, on_true_value, on_false_value):
  if bool_value:
    return on_true_value
  return on_false_value
  
def bisect_str(s, find, find_last = False):
  if s == None: return None
  if find_last: idx = s.rfind(find)
  else:         idx = s.find(find)
  if idx == -1: return None
  return [s[:idx], s[idx + 1:]]

def clear_term():
  for i in range(1, 150):
    print("\n")

# files
def read_file(filename):
  s = ""
  try:
    f = open(filename, 'r')
    s = f.read()
    f.close()
  except Exception as e:
    print('Failed to read ' + filename + ' file ' + str(e))
    return s
  return s

def read_line_list(filename):
  s = read_file(filename)
  return s.splitlines()
  
def write_file(filename, s):
  f = open(filename, 'w')
  f.write(s)
  f.close()
  
def write_line_list_file(filename, lines):
  f = open(filename, 'w')
  for line in lines:
    f.write(line)
    f.write("\n")
  f.close()
  
def append_line_list_file(filename, lines):
  f = open(filename, 'a')
  for line in lines:
    f.write(line)
    f.write("\n")
  f.close()
  
def most_recent_file_ending_with(path, ending_with):
  dir_list = os.listdir(path)
  latest_time = None
  latest_file = None
  for fname in dir_list:
    file_time = time.ctime(os.path.getctime(path + "/" + fname))
    if fname.endswith(ending_with):
      if latest_time is None or file_time > latest_time:
        latest_time = file_time
        latest_file = fname
  return latest_file
  
def condense_multiple_spaces(text):
  return replace_re(text, '\s\s+', ' ')

def uniques(ls):
  ls.sort()
  out = []
  last = ''
  for item in ls:
    item = str.lower(item)
    if item != last:
      out.append(item)
      last = item
  out.sort(key=string.lower)
  return out
  
def lowercase_list(ls):
  return [string.lower(w) for w in ls]
  
def uppercase_list(ls):
  return [string.upper(w) for w in ls]
  
def replace_using_table(s, table):
  for k, v in table.iteritems():
    s = s.replace(k, v)
  return s
  
def word_count(s):
  return len(s.split())
  
def percent_string(number):
  permil = int(number * 1000.0)
  s = str(permil / 10) + '.' + str(permil % 10)
  return s
  
def find_all(text, find):
  return [m.start() for m in re.finditer(find, text)]  

def value_for_colon_separated_key_values(text, key):
  if len(s) <= 0:
    return ''
  s = s.strip()
  lines = s.splitlines()
  for line in lines:
    if line.startswith(key + ':'):
      return line[0][len(key) + 1:].strip()
  return ''

def escape_path(path):
  return path.replace('[', '\[').replace(']', '\]').replace(' ', '\ ')
  
def copy_files_to(source, to):
  cmd = 'cp -R {0} {1}'.format(escape_path(source), escape_path(to))
  os.system(cmd)

def copy_path_to(source, to):
  if os.path.exists(to):
    shutil.rmtree(to)
  if not os.path.exists(to):
    os.mkdir(to)
  copy_files_to(source + '/', to)

def replace_keys(s, dict):
  for k, v in dict.iteritems():
    s = s.replace(k, v)
  return s;
  
def copy_files_from_dict(dict, from_path, to_path):
  for k, v in dict.iteritems():
    try:
       shutil.copyfile(from_path + "/" + k, to_path + "/" + v)
       print("Copying from " + from_path + "/" + k + " to " + to_path + "/" + v)
    except Exception:
       print("") #"File " + from_path + "/" + k + " not found.")

def replace_strings_in_file(filename_in, filename_out, dict):
  if dict is None:
    print("BAD DICT")
  else:
    s = read_file(filename_in)
    if s is not None:
      s = replace_keys(s, dict)
      write_file(filename_out, s)
      
def make_path(path, filename):
  if len(path) != 0:
    return path + "/" + filename
  return filename

def find_file_in_path(path, filename):
  if not os.path.exists(path):
    print("PATH DOESN'T EXIST")
    return None
  for r,d,f in os.walk(path):
    for files in f:
      if files == filename:
         return os.path.join(r,files)
  return None

def copy_file(from_path, to_path):
  try:
     shutil.copyfile(from_path, to_path)
     print("Copying from " + from_path + " to " + to_path)
  except Exception:
     print("FAILED copying from " + from_path + " to " + to_path)
     
def for_each_file(in_path, do_this, args):
  for folder, subs, files in os.walk(in_path):
    for filename in files:
      if not do_this(os.path.join(folder, filename), args):
        return False
  return True

def merge_defaults(dict, defaults):
  for key, value in defaults.iteritems():
    if key not in dict:
      dict[key] = value
  return dict

def abort(message):
  print(message)
  sys.exit()
  
def split_path(filepath):
  (path, fn) = os.path.split(filepath)
  filename = fn
  (fn, ext) = os.path.splitext(fn)
  if len(ext) > 0:
    ext = ext.strip('.')
  return (path, filename, fn, ext)

def clean_line_ends(s):
  lines = []
  for line in s.splitlines():
    lines.append(line.rstrip())
  return "\n".join(lines)

def prefix_lines(text, prefix = None):
  if prefix is None or prefix == '':
    return text
  lines = []
  for line in text.splitlines():
    lines.append(prefix + line.rstrip())
  return "\n".join(lines)

def required_value(map, key):
  if not key in map or map[key] == None:
    abort('Value for key ' + key + ' not found.')
  return map[key]

def optional_value(map, key):
  if not key in map or map[key] == None:
      return None
  return map[key]
