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

class MP3File:
  def __init__(self, filename, machine, strict=False):
    self.filename = filename
    self.tags = {}
    info = str(machine.command.execute(filename), encoding='utf-8')
    for line in info.splitlines():
      tag_match = re.search(machine.regex, line)
      if tag_match is None:
        continue
      self.tags[tag_match.group(machine.tag_indices['tag'])] = \
        tag_match.group(machine.tag_indices['value']).strip()
    self.title = self.get_tag_value(machine.tag_list.title, strict)
    self.artist = self.get_tag_value(machine.tag_list.artist, strict)
    self.num = self.get_tag_value(machine.tag_list.num, strict)
    self.album = self.get_tag_value(machine.tag_list.album, strict)
    self.composer = self.get_tag_value(machine.tag_list.composer, strict)
    self.genre = self.get_tag_value(machine.tag_list.genre, strict)
    self.year = self.get_tag_value(machine.tag_list.year, strict)

  class StrictError(Exception):
    def __init__(self, value):
      self.value = value

    def __str__(self):
      return repr(self.value)

  def get_best_tag_value(self, tag_list):
    for preferred_tag in tag_list:
      if preferred_tag in self.tags:
        return self.tags[preferred_tag]
    return None

  def get_tag_value(self, tag_list, strict=False):
    result = self.get_best_tag_value(tag_list)
    if result is None:
      if strict:
        raise MP3File.StrictError("get_tag_value: " +
              "strict is True and there is no metadata matching " +
              str(tag_list))
      else:
        return self.filename.split("/").pop()
    else:
      return result

  def __str__(self):
    return '"' + self.artist + '/' + self.album + '/' + self.num + ' - ' + self.title + '.mp3"'

  def __repr__(self):
    return self.__str__()
