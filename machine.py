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
  instances = {}

  def __init__(self, tag_list, tag_indices, regex, command, directory_delimiter='/'):
    self.tag_list = tag_list
    self.tag_indices = tag_indices
    self.regex = regex
    self.command = command
    self.directory_delimiter = '/'

  class Tags:
    def __init__(self, name, tag_list):
      self.name = name
      self.tag_list = tag_list

    def __iter__(self):
      return self.tag_list.__iter__()

    def __str__(self):
      return self.name

    def __repr__(self):
      return self.__str__()

  class TagList:
    def __init__(self, title, artist, num, album, composer, genre, year):
      self.title = Machine.Tags('title', title)
      self.artist = Machine.Tags('artist', artist)
      self.num = Machine.Tags('num', num) # may be in the form "4" or "4/16"
      self.album = Machine.Tags('album', album)
      self.composer = Machine.Tags('composer', composer)
      self.genre = Machine.Tags('genre', genre)
      self.year = Machine.Tags('year', year)

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
mac_ls = Command(["id3info"], [])
linux_ls = Command(["id3", "-lR"], [])

Machine.instances['mac'] = Machine(mac_tag_names,
      mac_tag_indices,
      mac_regex,
      mac_ls)
Machine.instances['linux'] = Machine(linux_tag_names,
      linux_tag_indices,
      linux_regex,
      linux_ls)
