"""
Utilities for parsing info files.
"""

import os, re, codecs

ENCODING_PLEX = 'utf-8'
INFO_FILE_EXTENSION = 'info'
INFO_SHOW_FILENAME = 'show.' + INFO_FILE_EXTENSION
INFO_EPISODE_FILENAME = 'episode.' + INFO_FILE_EXTENSION

MATCHER_INFO_TAG = re.compile('^\s*\[(.*)\]\s*', re.UNICODE)
MATCHER_COMMENT_LINE = re.compile('^\s*#')
TUPLE_SPLIT_STRING = '|'

INTEGER_TAGS = {'year': True, 'duration': True}
FLOAT_TAGS = {'rating': True}
DATE_TAGS = {'originally_available_at': True}
ARRAY_TAGS = {
  'genres': True, 'directors': True, 'writers': True, 'countries': True, 'collections': True, 'countries': None
}

def findInfoFileFromMovieFilepath(movieFilepath):
  if not movieFilepath:
    return None
  # Assume movie info file is in the same directory
  # and has the same name as the the movie file.
  infoFilePath = os.path.splitext(movieFilepath)[0] + '.' + INFO_FILE_EXTENSION
  if os.path.exists(infoFilePath):
    return infoFilePath
  return None

def findShowFileFromEpisodeFilepath(episodeFilepath):
  if not episodeFilepath:
    return None
  # Assume episode is in its own directory.
  # Look inside the season directory (one up).
  path = os.path.dirname(os.path.dirname(episodeFilepath))
  infoFilePath = os.path.join(path, INFO_SHOW_FILENAME)
  if os.path.exists(infoFilePath):
    return infoFilePath
  # Last 'stop' - assume it's the show directory.
  path = os.path.dirname(path)
  infoFilePath = os.path.join(path, INFO_SHOW_FILENAME)
  if os.path.exists(infoFilePath):
    return infoFilePath
  return None

def findEpisodeFileFromEpisodeFilepath(episodeFilepath):
  if not episodeFilepath:
    return None
  path = os.path.dirname(episodeFilepath)
  infoFilePath = os.path.join(path, INFO_EPISODE_FILENAME)
  if os.path.exists(infoFilePath):
    return infoFilePath
  # Look for a file named the same as the video file.
  infoFilePath = os.path.splitext(episodeFilepath)[0] + '.' + INFO_FILE_EXTENSION
  if os.path.exists(infoFilePath):
    return infoFilePath
  return None

def isCommentLine(line):
  return MATCHER_COMMENT_LINE.search(line)

def parseMultiLineValue(lines):
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

def parseArrayValue(lines):
  value = []
  for line in lines:
    line = line.strip()
    if line:
      value.append(line)
  return value

def storeTagValuePair(parsedData, tagName, infoLines):
  if not tagName or not infoLines:
    return
  value = None
  if tagName in ARRAY_TAGS:
    value = parseArrayValue(infoLines)
  else:
    value = parseMultiLineValue(infoLines)
  if not value:
    return
  if tagName in INTEGER_TAGS:
    parsedData[tagName] = int(value)
  elif tagName in FLOAT_TAGS:
    parsedData[tagName] = float(value)
  elif tagName in DATE_TAGS:
    parsedData[tagName] = Datetime.ParseDate(value)
  else:
    parsedData[tagName] = value

def parseInfoFileIfExists(infoFilePath):
  """Opens and parses an info file if it exists.
  Parsed data is returned as a dictionary.

  Args:
    infoFilePath: string - path to the info file.
  Returns:
    dictionary with a parsed data or None
  """
  parsedData = {}
  try:
    if not infoFilePath or not os.path.exists(infoFilePath):
      return None

    currTagName = None
    currTagLines = []
    with codecs.open(infoFilePath, "r", encoding='utf-8') as file:
      infoLines = file.readlines()
      for infoLine in infoLines:
        infoLine = infoLine.strip()
        if isCommentLine(infoLine) or not infoLine:
          # skipping a comment line
          continue
        match = MATCHER_INFO_TAG.search(infoLine)
        if match: # It's a tag.
          # first, write the previous tag/value pair if any
          if currTagName:
            storeTagValuePair(parsedData, currTagName, currTagLines)
            currTagLines = []
          currTagName = match.groups()[0]
        else:
          currTagLines.append(infoLine)
      # Write the last tag data.
      storeTagValuePair(parsedData, currTagName, currTagLines)
  except Exception as e:
    Log.Error('Failed to parse tag "' + str(currTagName) + '" - %s' % str(e))
  return parsedData or None
