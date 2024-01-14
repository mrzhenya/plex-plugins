
class TV_Show():
  # emulating only a subset of properties that are used in shows.

  title = None # string
  summary = None # string
  originally_available_at = None # date
  content_rating = None # string
  rating = None # float
  studio = None # string
  collections = None # array
  genres = None # array

  def __str__(self) -> str:
    return "\n    title: %s\n    summary: %s\n    originally_available_at: %s" \
           "\n    content_rating: %s\n    rating: %s\n    studio: %s\ncollections: %s\ngenres: %s"\
      % (str(self.title), str(self.summary), str(self.originally_available_at), str(self.content_rating),
         str(self.rating), str(self.studio), str(collections), str(genres))

class RecordObject():
  # emulating only a subset of properties that are used in episodes.

  title = None # string
  summary = None # string
  originally_available_at = None # date
  content_rating = None # string
  rating = None # float
  writers = None # array
  directors = None # array

  def __str__(self) -> str:
    return "\n    title: %s\n    summary: %s\n    originally_available_at: %s" \
           "\n    content_rating: %s\n    rating: %s\n    writers: %s\ndirectors: %s" \
      % (str(self.title), str(self.summary), str(self.originally_available_at), str(self.content_rating),
         str(self.rating), str(self.writers), str(directors))

class Movie():
  title = None # string
  original_title = None # string
  summary = None # string
  year = None # Integer
  originally_available_at = None # date
  tagline = None # string
  content_rating = None # string
  rating = None # float
  studio = None # String
  genres = None # array
  countries = None # array
  collections = None # array
