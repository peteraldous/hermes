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
  def __init__(self, tag_list, tag_indices, regex, command):
    self.tag_list = tag_list
    self.tag_indices = tag_indices
    self.regex = regex
    self.command = command

  class TagList:
    def __init__(self, title, artist, num, album, composer, genre, year):
      self.title = title
      self.artist = artist
      self.num = num # may be in the form "4" or "4/16"
      self.album = album
      self.composer = composer
      self.genre = genre
      self.year = year

mac_tag_names = Machine.TagList(['TIT2'],
                                ['TPE1', 'TPE2', 'TPE3'],
                                ['TRCK'],
                                ['TALB'],
                                ['TCOM'],
                                ['TCON'],
                                ['TYER'])
linux_tag_names = Machine.TagList(['Title'],
                                  ['Artist'],
                                  ['Track'],
                                  ['Album'],
                                  [],
                                  ['Genre'],
                                  ['Year'])

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

# TODO make a class for an MP3 file and get rid of the dicts

parser = argparse.ArgumentParser(description =
           "Rename an mp3 file according to its ID3 tag.")
parser.add_argument('files', metavar='f', nargs='+',
                    help='one or more mp3 filenames')
parser.add_argument('--os', '-o', default='linux', action='store',
                    choices=['linux', 'mac'],
                    help='The operating system being used.')
parser.add_argument('--strict', '-s', default=True, action='store',
                    type=bool,
                    help='If true, requires metadata for all parts of the format.')

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

def get_best_tag_value(tag_list, tags):
  for preferred_tag in tag_list:
    if tags[preferred_tag] is not None:
      return tags[preferred_tag]
  return None

def get_tag_value(tag_list, filename, tags):
  result = get_best_tag_value(tag_list, tags)
  if result is None:
    if strict:
      raise "Strict: no tags found from the list" + tag_list
    else:
      return filename.split("/").pop()
  else:
    return result

#print(all_tags)
for mp3_file, tags in all_tags.items():
  title = get_tag_value(machine.tag_list.title, mp3_file, tags)
  artist = get_tag_value(machine.tag_list.artist, mp3_file, tags)
