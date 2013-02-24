#!/usr/local/bin/python3
#
# TODO
# one line to give the program's name and an idea of what it does.
# Copyright (C) 2013  Petey Aldous
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# *ADDITIONAL TERMS*
# This software or binaries made from this software may not be
# distributed with any form digital rights management or any
# advertisements. Similarly, no software that uses or is
# protected by digital rights management or that displays,
# stores, or transmits advertisements in any form may make use of
# this software.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import re
import argparse
from machine import Machine

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
machine = Machine.instances[options.os]
if machine is None:
  raise "Could not find machine named " + options.os

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

print(all_tags)
for mp3_file, tags in all_tags.items():
  title = get_tag_value(machine.tag_list.title, mp3_file, tags)
  artist = get_tag_value(machine.tag_list.artist, mp3_file, tags)
