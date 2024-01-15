"""
Utilities for writing parsed metadata into the Plex objects.
"""

def writeMovieMetadata(movieMetadata, parsedData):
  """ Writes the passed data into a movie metadata object.

  :param movieMetadata: Framework.models.metadata.com_plexapp_agents_localmetadata.Movie
  :param parsedData: parsed info metadata
  """
  try:
    tagName = None
    for tagName in parsedData.keys():
      value = parsedData[tagName]
      if tagName == 'title':
        movieMetadata.title = value
      if tagName == 'original_title':
        movieMetadata.original_title = value
      elif tagName == 'summary':
        movieMetadata.summary = value
      elif tagName == 'year':
        movieMetadata.year = value
      elif tagName == 'originally_available_at':
        movieMetadata.originally_available_at = value
      elif tagName == 'tagline':
        movieMetadata.tagline = value
      elif tagName == 'content_rating':
        movieMetadata.content_rating = value
      elif tagName == 'rating':
        movieMetadata.rating = value
      elif tagName == 'studio':
        movieMetadata.studio = value
      elif tagName == 'genres':
        movieMetadata.genres = value
      elif tagName == 'countries':
        movieMetadata.countries = value
      elif tagName == 'collections':
        movieMetadata.collections = value
  except Exception as e:
    Log.Error('Failed to write tag "' + str(tagName) + '" - %s' % str(e))

def writeTvShowMetadata(tvShowMetadata, parsedData):
  """Stores the passed metadata into a TV_Show object.
  Framework.models.metadata.com_plexapp_agents_localmetadata.TV_Show

  Args:
    tvShowMetadata:
    parsedData: dict
  """
  try:
    tagName = None
    for tagName in parsedData.keys():
      value = parsedData[tagName]
      if tagName == 'title':
        tvShowMetadata.title = value
      elif tagName == 'summary':
        tvShowMetadata.summary = value
      elif tagName == 'content_rating':
        tvShowMetadata.content_rating = value
      elif tagName == 'rating':
        tvShowMetadata.rating = value
      elif tagName == 'studio':
        tvShowMetadata.studio = value
      elif tagName == 'originally_available_at':
        tvShowMetadata.originally_available_at = value
      elif tagName == 'collections':
        tvShowMetadata.collections = value
      elif tagName == 'genres':
        tvShowMetadata.genres = value

  except Exception as e:
    Log.Error('Failed to write tag "' + str(tagName) + '" - %s' % str(e))

def writeTvEpisodeMetadata(tvEpisodeMetadata, parsedData):
  """Stores the passed metadata into a episode object.

  Args:
    tvEpisodeMetadata:
    parsedData: dict
  """
  try:
    tagName = None
    for tagName in parsedData.keys():
      value = parsedData[tagName]
      if tagName == 'title':
        tvEpisodeMetadata.title = value
      elif tagName == 'summary':
        tvEpisodeMetadata.summary = value
      elif tagName == 'content_rating':
        tvEpisodeMetadata.content_rating = value
      elif tagName == 'rating':
        tvEpisodeMetadata.rating = value
      elif tagName == 'writers':
        tvEpisodeMetadata.writers = value
      elif tagName == 'directors':
        tvEpisodeMetadata.directors = value
      elif tagName == 'originally_available_at':
        tvEpisodeMetadata.originally_available_at = value

  except Exception as e:
    Log.Error('Failed to write tag "' + str(tagName) + '" - %s' % str(e))
