import os
import infofileutils, metadatautils

#####################################################################################################################

class localMetadataMovie(Agent.Movies):
  name = 'Local Metadata info (Movies)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  persist_stored_files = False
  contributes_to = ['com.plexapp.agents.imdb', 'com.plexapp.agents.none']

  def search(self, results, media, lang):
    results.Append(MetadataSearchResult(id = 'null', score = 100))
    
  def update(self, metadata, media, lang):
    part = media.items[0].parts[0]
    infoFile = infofileutils.findInfoFileFromMovieFilepath(part.file)
    movieMetadata = infofileutils.parseInfoFileIfExists(infoFile)
    metadatautils.writeMovieMetadata(metadata, movieMetadata)

#####################################################################################################################

class localMetadataMovieTV(Agent.TV_Shows):
  name = 'Local Metadata info (TV)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  persist_stored_files = False
  contributes_to = ['com.plexapp.agents.none']

  def search(self, results, media, lang):
    results.Append(MetadataSearchResult(id = 'null', score = 100))

  def update(self, metadata, media, lang):
    isShowMetadataParsed = False
    for s in media.seasons:
      Log('Creating season %s', s)
      metadata.seasons[s].index = int(s)

      for e in media.seasons[s].episodes:
        episodeMetadata = metadata.seasons[s].episodes[e]
        episodeMedia = media.seasons[s].episodes[e].items[0]
        episodeFile = episodeMedia.parts[0].file

        # Parse show metadata from an info file if it exists.
        if not isShowMetadataParsed:
          showInfoFile = infofileutils.findShowFileFromEpisodeFilepath(episodeFile)
          Log('parsing metadata from the show info file: %s' % str(showInfoFile))
          showMetadata = infofileutils.parseInfoFileIfExists(showInfoFile)
          metadatautils.writeTvShowMetadata(metadata, showMetadata)
          isShowMetadataParsed = True

        episodeInfoFile = infofileutils.findEpisodeFileFromEpisodeFilepath(episodeFile)
        Log('parsing metadata from the episode info file: %s' % str(episodeInfoFile))
        episodeData = infofileutils.parseInfoFileIfExists(episodeInfoFile)
        metadatautils.writeTvEpisodeMetadata(episodeMetadata, episodeData)
