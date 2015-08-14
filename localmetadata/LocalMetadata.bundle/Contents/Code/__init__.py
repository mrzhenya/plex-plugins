# -*- coding: utf-8 -*-
#
# Metadata plugin for Plex Media Server, which updates media's metadata
# using information stored in local info files.
#
# Copyright (C) 2015  Yevgeny Nyden
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# @author zhenya (Yevgeny Nyden)
# @version @PLUGIN.REVISION@
# @revision @REPOSITORY.REVISION@

import re, os, io, datetime


LOGGER = Log

ENCODING_PLEX = 'utf-8'
INFO_FILE_EXTENSION = '.info'

MATCHER_INFO_TAG = re.compile('^\s*\[(.*)\]\s*', re.UNICODE)
MATCHER_COMMENT_LINE = re.compile('^\s*###')
TUPLE_SPLIT_STRING = '|'


def Start():
  LOGGER.Info('***** START *****')


def ValidatePrefs():
  LOGGER.Info('***** updating preferences...')


# Only use unicode if it's supported, which it is on Windows and OS X,
# but not Linux. This allows things to work with non-ASCII characters
# without having to go through a bunch of work to ensure the Linux
# filesystem is UTF-8 "clean".
#
def unicodize(s):
  filename = s
  if os.path.supports_unicode_filenames:
    try: filename = unicode(s.decode(ENCODING_PLEX))
    except: pass
  return filename


def getAndTestInfoFilePath(media):
  part = media.items[0].parts[0]
  filename = unicodize(part.file)
  path = os.path.splitext(filename)[0] + INFO_FILE_EXTENSION
  if os.path.exists(path):
    return path
  else:
    return None


def parsePipeSeparatedTuple(str):
  """Parses a tuple of values separated by '|' from the given string.

  Args:
    str - string to parse
  Returns:
    tuple of strings or empty values if nothing was parsed.
  """
  tokens = str.split(TUPLE_SPLIT_STRING)
  second = ''
  if len(tokens) > 1:
    second = tokens[1].strip()
  return tokens[0].strip(), second


def parseStringValueFromText(lines):
  mergedValue = ''
  for line in lines:
    line = line.strip()
    if not line and not mergedValue:
      # Skipping leading empty lines.
      continue
    if not line:
      mergedValue += '\n'
    elif mergedValue:
      mergedValue += ' '
    mergedValue += line
  return mergedValue


def parseSingleValueFromText(lines):
  for line in lines:
    return line.strip()
  return ''


def parseAndAddActorsFromText(roles, lines):
  for line in lines:
    actor, role = parsePipeSeparatedTuple(line)
    if actor:
      role = roles.new()
      role.actor = actor
      role.role = role


def parseAndAddArrayValuesFromText(container, lines):
  """Parses text values and adds them to a metadata array container.

  Args:
    container: list where parsed values are added;
    lines: list of strings to parse.
  """
  for line in lines:
    line = line.strip()
    if line:
      container.add(line)

def parseIntegerValueFromText(lines):
  return int(parseStringValueFromText(lines))


def parseFloatValueFromText(lines):
  return float(parseStringValueFromText(lines))


def parseDateValueFromText(lines):
  if lines:
    return Datetime.ParseDate(lines[0]).date()


def isCommentLine(line):
  return MATCHER_COMMENT_LINE.search(line)


def writeTagValueToMetadata(metadata, tagName, tagLines):
  """Parses and stores the passed tag data into metadata object.

  Args:
    metadata: Metadata - Plex metadata object.
    tagName: string - 'info' file tag name
    tagLines: list - lines as parsed from the file
  """
  try:
    if not tagName:
      return
    tagName = tagName.lower()

    # Title.
    if tagName == 'title':
      metadata.title = parseStringValueFromText(tagLines)
    elif tagName == 'original_title':
      metadata.original_title = parseStringValueFromText(tagLines)

    # Year.
    elif tagName == 'year':
      metadata.year = parseIntegerValueFromText(tagLines)

    # Runtime.
    elif tagName == 'duration' or tagName == 'runtime':
      metadata.duration = parseIntegerValueFromText(tagLines) * 1000

    # Genres.
    elif tagName == 'genres':
      parseAndAddArrayValuesFromText(metadata.genres, tagLines)

    # Directors.
    elif tagName == 'directors':
      parseAndAddArrayValuesFromText(metadata.directors, tagLines)

    # Writers.
    elif tagName == 'writers':
      parseAndAddArrayValuesFromText(metadata.writers, tagLines)

    # Actors.
    elif tagName == 'actors':
      parseAndAddActorsFromText(metadata.roles, tagLines)

    # Studio
    elif tagName == 'studio':
      metadata.studio = parseStringValueFromText(tagLines)

    # Tagline.
    elif tagName == 'tagline':
      metadata.tagline = parseStringValueFromText(tagLines)

    # Summary.
    elif tagName == 'summary':
      metadata.summary = parseStringValueFromText(tagLines)

    # Content rating.
    elif tagName == 'content_rating':
      metadata.content_rating = parseSingleValueFromText(tagLines)

    # Release date.
    elif tagName == 'original_date':
      metadata.originally_available_at = parseDateValueFromText(tagLines)

    # Country.
    elif tagName == 'countries':
      parseAndAddArrayValuesFromText(metadata.countries, tagLines)

    # Rating.
    elif tagName == 'rating':
      metadata.rating = parseFloatValueFromText(tagLines)

    # Collections.
    elif tagName == 'collections':
      parseAndAddArrayValuesFromText(metadata.collections, tagLines)


    elif tagName == 'poster':
      pass
    elif tagName == 'still':
      pass
  except:
    LOGGER.Error('Failed to parse tag "' + str(tagName) + '"')


class MyMediaAgent(Agent.Movies):
  name = 'Local Metadata (Movies)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = True
  fallback_agent = False
  accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.none']
  contributes_to = ['com.plexapp.agents.none']


  ##############################################################################
  ############################# S E A R C H ####################################
  ##############################################################################
  def search(self, results, media, lang, manual=False):
    """Searches local directory for the metadata .info file.
    """
    LOGGER.Debug('SEARCH START <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    mediaName = media.name
    mediaYear = media.year
    mediaHash = media.hash
    LOGGER.Debug('searching for name="%s", year="%s", guid="%s", hash="%s"...' %
        (str(mediaName), str(mediaYear), str(media.guid), str(mediaHash)))

    infoFilepath = getAndTestInfoFilePath(media)
    if infoFilepath is None:
      return

    part = media.items[0].parts[0]
    if mediaHash is None:
      mediaHash = part.hash
    if mediaYear is None:
      filename = unicodize(part.file)
      modificationTime = os.path.getmtime(filename)
      date = datetime.date.fromtimestamp(modificationTime)
      mediaYear = date.year
    results.Append(MetadataSearchResult(id=mediaHash, name=mediaName, year=mediaYear, score=100, lang=lang))

    LOGGER.Debug('SEARCH END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')


  ##############################################################################
  ############################# U P D A T E ####################################
  ##############################################################################
  def update(self, metadata, media, lang, force=False):
    """Updates the metadata on a given media item.
    """
    LOGGER.Debug('UPDATE START <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    infoFilepath = getAndTestInfoFilePath(media)
    if infoFilepath is None:
      return

    if force:
      resetMediaAllMetadata(metadata)
    currTagName = None
    currTagLines = []
    for infoLine in io.open(infoFilepath, 'rt'):
      match = MATCHER_INFO_TAG.search(infoLine)
      if match:
        # It's a tag.
        writeTagValueToMetadata(metadata, currTagName, currTagLines)
        currTagLines = []
        currTagName = match.groups()[0]
      elif not isCommentLine(infoLine):
        # Content.
        currTagLines.append(infoLine)
    # Write the last tag data.
    writeTagValueToMetadata(metadata, currTagName, currTagLines)

    LOGGER.Debug('UPDATE END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')


def resetMediaAllMetadata(metadata):
  """Resets all relevant fields on a passed media metadata object.
  """
  metadata.genres.clear()
  metadata.countries.clear()
  metadata.directors.clear()
  metadata.writers.clear()
  metadata.roles.clear()
  metadata.collections.clear()
  metadata.studio = ''
  metadata.summary = ''
  metadata.title = ''
  metadata.year = None
  metadata.originally_available_at = None
  metadata.original_title = ''
  metadata.duration = None
