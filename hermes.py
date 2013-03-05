#!/usr/local/bin/python3
#
# TODO
# one line to give the program's name and an idea of what it does.
# Copyright (C) 2013  Petey Aldous
# TODO contact info
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

import argparse
from machine import Machine
from mp3file import MP3File

# TODO read a config file, which should be overridden by the command-line arguments

parser = argparse.ArgumentParser(description =
           "Rename an mp3 file according to its ID3 tag.")
parser.add_argument('files', metavar='f', nargs='+',
                    help='one or more mp3 filenames')
parser.add_argument('--os', '-o', default='linux', action='store',
                    choices=['linux', 'mac'],
                    help='The operating system being used.')
parser.add_argument('--strict', '-s', default=False, action='store',
                    type=bool,
                    help='If true, requires metadata for all parts of the format.')

options = parser.parse_args()
machine = Machine.instances[options.os]
if machine is None:
  raise "Could not find machine named " + options.os

mp3_files = []

for mp3_file in options.files:
  mp3_files.append(MP3File(mp3_file, machine))


print(mp3_files)

# TODO figure out the format for the destination files
# TODO determine which files need to be copied by reading the database
# TODO copy the files
# TODO update the database

# TODO check if any files have been copied to all clients
# TODO if so, remove them and any empty directories that contained them
