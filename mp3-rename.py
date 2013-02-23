#!/usr/local/bin/python3

import re
import argparse
import subprocess

class Command:
  def __init__(self, before, after):
    self.before = before
    self.after = after

  def execute(self, parameter):
    args = list(self.before)
    args.append(parameter)
    args.extend(self.after)
    proc = subprocess.Popen(args, bufsize=1, stdout=subprocess.PIPE)
    (output, _) = proc.communicate()
    return output

class Machine:
  def __init__(self, tag_names, tag_indices, regex, command):
    self.tag_names = tag_names
    self.tag_indices = tag_indices
    self.regex = regex
    self.command = command

mac_tag_names =   { 'Title'     : ['TIT2'],
                    'Artist'    : ['TPE1', 'TPE2', 'TPE3'],
                    'Tracknum'  : ['TRCK'], # may be in the form "4" or "4/16"
                    'Album'     : ['TALB'],
                    'Composer'  : ['TCOM'],
                    'Genre'     : ['TCON'],
                    'Year'      : ['TYER'],
}
linux_tag_names = { 'Title'     : ['Title'],
                    'Artist'    : ['Artist'],
                    'Tracknum'  : ['Track'], # may be in the form "4" or "4/16"
                    'Album'     : ['Album'],
                    'Composer'  : [],
                    'Genre'     : ['Genre'],
                    'Year'      : ['Year'],
}
mac_regex =   "=== ([A-Z0-9a-z]*) .*: ([^:]*)$"
linux_regex = "([A-Z0-9a-z]*): (.*)$"
mac_tag_indices = {'tag' : 1, 'value' : 2}
linux_tag_indices = {'tag' : 1, 'value' : 2}
mac_command = Command(["id3info"], [])
linux_command = Command(["id3", "-lR"], [])

machine_instances = {
          'mac' : Machine(mac_tag_names, mac_tag_indices, mac_regex, mac_command),
          'linux' : Machine(linux_tag_names, linux_tag_indices, linux_regex, linux_command)
}

parser = argparse.ArgumentParser(description =
           "Rename an mp3 file according to its ID3 tag.")
parser.add_argument('files', metavar='f', nargs='+',
                    help='one or more mp3 filenames')
parser.add_argument('--os', '-o', default='linux', action='store',
                    choices=['linux', 'mac'],
                    help='The operating system being used.')

options = parser.parse_args()
machine = machine_instances[options.os]

all_tags = {}

for mp3_file in options.files:
  tags = {}
  info = str(machine.command.execute(mp3_file), encoding='utf-8')
  for line in info.splitlines():
    tag_match = re.search(machine.regex, line)
    if tag_match is None:
      continue
    tags[tag_match.group(machine.tag_indices['tag'])] = \
      tag_match.group(machine.tag_indices['value']).strip()
  all_tags[mp3_file] = tags

def get_best_tag_value(tags, tag_list):
  for preferred_tag in tag_list:
    if tags[preferred_tag] is not None:
      return tags[preferred_tag]
  return None

def get_tag_value(machine, filename, tags):
  pass

for (mp3_file, tags) in all_tags:
  title = get_tag_value(machine, mp3_file, tags)
