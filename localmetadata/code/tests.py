import os, sys, importlib, unittest, datetime
import infofileutils
import metadatautils

class MyTestCase(unittest.TestCase):
  plex_objects_module = None

  def setUp(self):
    sys.path.append('./plex')
    infofileutils.Datetime = importlib.import_module('Datetime')
    self.plex_objects_module = importlib.import_module('plex_objects')

  def test_parsing_movie(self):
    parsedData = infofileutils.parseInfoFileIfExists('data/movie.info')
    self.assertIsNotNone(parsedData)
    self.assertEqual(12, len(parsedData.keys()), 'wrong number of parsed tags')
    self.assertEqual('Casablanca', parsedData['title'], 'wrong title')
    self.assertEqual('Casablanca original', parsedData['original_title'], 'wrong original title')
    self.assertEqual(1942, parsedData['year'], 'wrong year')
    self.assertEqual(datetime.datetime(1942, 5, 2, 0, 0), parsedData['originally_available_at'], 'wrong date')
    self.assertEqual('Where Love Cuts as Deep as a Dagger!', parsedData['tagline'], 'wrong tagline')
    self.assertEqual('The story of Rick Blaine, a cynical world-weary ex-patriate', parsedData['summary'], 'wrong summary')
    self.assertEqual('PTZP', parsedData['studio'], 'wrong studio')
    self.assertEqual(9.9, parsedData['rating'], 'wrong rating')
    self.assertEqual('PG', parsedData['content_rating'], 'wrong content_rating')
    self.assertEqual(['Drama', 'Romance', 'War'], parsedData['genres'], 'wrong genres')
    self.assertEqual(['USA'], parsedData['countries'], 'wrong countries')
    self.assertEqual(['War', 'Classics'], parsedData['collections'], 'wrong collections')

  def test_writing_movie_metadata(self):
    parsedData = infofileutils.parseInfoFileIfExists('data/movie.info')
    self.assertIsNotNone(parsedData)
    movie = self.plex_objects_module.Movie()
    metadatautils.writeMovieMetadata(movie, parsedData)
    self.assertEqual('Casablanca', movie.title, 'wrong title')
    self.assertEqual('Casablanca original', movie.original_title, 'wrong original title')
    self.assertEqual(1942, parsedData['year'], 'wrong year')
    self.assertEqual(datetime.datetime(1942, 5, 2, 0, 0), movie.originally_available_at, 'wrong date')
    self.assertEqual('Where Love Cuts as Deep as a Dagger!', movie.tagline, 'wrong tagline')
    self.assertEqual('The story of Rick Blaine, a cynical world-weary ex-patriate', movie.summary, 'wrong summary')
    self.assertEqual('PTZP', movie.studio, 'wrong studio')
    self.assertEqual(9.9, movie.rating, 'wrong rating')
    self.assertEqual('PG', movie.content_rating, 'wrong content_rating')
    self.assertEqual(['Drama', 'Romance', 'War'], movie.genres, 'wrong genres')
    self.assertEqual(['USA'], movie.countries, 'wrong countries')
    self.assertEqual(['War', 'Classics'], movie.collections, 'wrong collections')

  def test_parsing_show(self):
    parsedData = infofileutils.parseInfoFileIfExists('data/show.info')
    self.assertIsNotNone(parsedData)
    self.assertEqual(8, len(parsedData.keys()), 'wrong number of parsed tags')
    self.assertEqual('Most fantastic title', parsedData['title'], 'wrong title')
    self.assertEqual('Summary of this title', parsedData['summary'], 'wrong summary')
    self.assertEqual(8.7, parsedData['rating'], 'wrong rating')
    self.assertEqual('PG', parsedData['content_rating'], 'wrong content rating')
    self.assertEqual(datetime.datetime(1997, 9, 1, 0, 0), parsedData['originally_available_at'], 'wrong date')
    self.assertEqual('Nyden Studio', parsedData['studio'], 'wrong studio')
    self.assertEqual(['Family Shows', 'Fun'], parsedData['collections'], 'wrong collections')
    self.assertEqual(['Family'], parsedData['genres'], 'wrong genres')

  def test_writing_show_metadata(self):
    parsedData = infofileutils.parseInfoFileIfExists('data/show.info')
    self.assertIsNotNone(parsedData)
    show = self.plex_objects_module.TV_Show()
    metadatautils.writeTvShowMetadata(show, parsedData)
    self.assertEqual('Most fantastic title', show.title, 'wrong title')
    self.assertEqual('Summary of this title', show.summary, 'wrong summary')
    self.assertEqual(8.7, show.rating, 'wrong rating')
    self.assertEqual('PG', show.content_rating, 'wrong content rating')
    self.assertEqual(datetime.datetime(1997, 9, 1, 0, 0), show.originally_available_at, 'wrong date')
    self.assertEqual('Nyden Studio', show.studio, 'wrong studio')
    self.assertEqual(['Family Shows', 'Fun'], show.collections, 'wrong collections')
    self.assertEqual(['Family'], show.genres, 'wrong genres')

  def test_parsing_episode(self):
    parsedData = infofileutils.parseInfoFileIfExists('data/episode.info')
    self.assertIsNotNone(parsedData)
    self.assertEqual(7, len(parsedData.keys()), 'wrong number of parsed tags')
    self.assertEqual('Most fantastic title', parsedData['title'], 'wrong title')
    self.assertEqual('Summary of this title', parsedData['summary'], 'wrong summary')
    self.assertEqual(8.8, parsedData['rating'], 'wrong rating')
    self.assertEqual('PG', parsedData['content_rating'], 'wrong content rating')
    self.assertEqual(datetime.datetime(1997, 9, 1, 0, 0), parsedData['originally_available_at'], 'wrong date')
    self.assertEqual(['Yev Nyden', 'Victor Nyden'], parsedData['directors'], 'wrong directors')
    self.assertEqual(['Victor Nyden'], parsedData['writers'], 'wrong writers')

  def test_parsing_episode_nonascii(self):
    parsedData = infofileutils.parseInfoFileIfExists('data/nonascii_episode.info')
    self.assertIsNotNone(parsedData)
    self.assertEqual(6, len(parsedData.keys()), 'wrong number of parsed tags')
    self.assertEqual('ГРОТ - Алтай, р. Большие Чили', parsedData['title'], 'wrong title')
    self.assertEqual('Ох Чилевское пиво, очень даже ничево!', parsedData['summary'], 'wrong summary')
    self.assertEqual(9.0, parsedData['rating'], 'wrong rating')
    self.assertEqual('PG', parsedData['content_rating'], 'wrong content rating')
    self.assertEqual(datetime.datetime(2001, 8, 1, 0, 0), parsedData['originally_available_at'], 'wrong date')
    self.assertEqual(['Yevgeny Nyden'], parsedData['directors'], 'wrong directors')

  def test_writing_episode_metadata(self):
    parsedData = infofileutils.parseInfoFileIfExists('data/episode.info')
    self.assertIsNotNone(parsedData)
    episode = self.plex_objects_module.RecordObject()
    metadatautils.writeTvEpisodeMetadata(episode, parsedData)
    self.assertEqual('Most fantastic title', episode.title, 'wrong title')
    self.assertEqual('Summary of this title', episode.summary, 'wrong summary')
    self.assertEqual(8.8, episode.rating, 'wrong rating')
    self.assertEqual('PG', episode.content_rating, 'wrong content rating')
    self.assertEqual(datetime.datetime(1997, 9, 1, 0, 0), episode.originally_available_at, 'wrong date')
    self.assertEqual(['Yev Nyden', 'Victor Nyden'], episode.directors, 'wrong directors')
    self.assertEqual(['Victor Nyden'], episode.writers, 'wrong writers')

  def test_movie_path_utils(self):
    # Info file is in the show directory.
    movieFilepath = 'data/movie/testmovie.mov'
    infoFilename = infofileutils.findInfoFileFromMovieFilepath(movieFilepath)
    self.assertEqual('data/movie/testmovie.info', infoFilename)

  def test_show_path_utils(self):
    # Info file is in the show directory.
    episodeFilepath = 'data/show/season/episode/episode.mov'
    showFilename = infofileutils.findShowFileFromEpisodeFilepath(episodeFilepath)
    self.assertEqual('data/show/show.info', showFilename)

    # Info file is in the season directory.
    episodeFilepath = 'data/show1/season/episode/episode.mov'
    showFilename = infofileutils.findShowFileFromEpisodeFilepath(episodeFilepath)
    self.assertEqual('data/show1/season/show.info', showFilename)

    # No info file exists.
    episodeFilepath = 'data/show2/season/episode/episode.mov'
    showFilename = infofileutils.findShowFileFromEpisodeFilepath(episodeFilepath)
    self.assertIsNone(showFilename)

  def test_episode_path_utils(self):
    # Info file is in the episode own directory and has a standard name.
    episodeFilepath = 'data/show/season/episode/episode.mov'
    infoFilename = infofileutils.findEpisodeFileFromEpisodeFilepath(episodeFilepath)
    self.assertEqual('data/show/season/episode/episode.info', infoFilename)

    # Info file is in the episode directory and has the same name as the movie file.
    episodeFilepath = 'data/show3/season/episode/customname.mov'
    infoFilename = infofileutils.findEpisodeFileFromEpisodeFilepath(episodeFilepath)
    self.assertEqual('data/show3/season/episode/customname.info', infoFilename)

    # No info file exists.
    episodeFilepath = 'data/show2/season/episode/episode.mov'
    infoFilename = infofileutils.findEpisodeFileFromEpisodeFilepath(episodeFilepath)
    self.assertIsNone(infoFilename)

if __name__ == '__main__':
  unittest.main()
