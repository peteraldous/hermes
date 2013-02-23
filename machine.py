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
