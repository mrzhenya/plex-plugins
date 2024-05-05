# Plex Local Metadata Files plugin/agent

A plugin for the [Plex Media Server](https://www.plex.tv/) that helps to tag Movie
and TV (Show) media assets using information provided via local `.info` files.
Plex has a decent support for local media files, and you can get by without using
this plugin; however, `Local Metadata Files` agent adds a few extras such as parsing
media title and summary from a local text file, support for the full date (not just
year), and support for additional tags such as rating, content rating, directors,
and more. 

Organizing your family or personal media files in Plex is a great use case for this agent.

## Installation

A recent version of plugin could be found in the
[release](https://github.com/mrzhenya/plex-plugins/tree/master/localmetadata/release)
folder or could be assembled by running the `dist` ant target in the project's
development folder.

1. First, copy the plugin bundle `PlexLocalMetadata.bundle` into the Plex Media Server
   plug-ins directory:
   * on Windows, it's `%LOCALAPPDATA%/Plex Media Server/Plug-ins` (e.g. 
     C:\Users\julie\AppData\Local\Plex Media Server\Plug-ins)
   * on Mac, it's `/Users/USER/Library/Application Support/Plex Media Server/Plug-ins`

2. Restart or start the Plex Media Server.

3. Configure agents priority for `Personal Media Shows` in `Shows` and `Personal Media` 
   in `Movies`:
    * `Local Media Assets` should be first (the very top one);
    * `Local Metadata Info Files` (our plugin) should be next (the second from the top);
    * and make sure the plugins are enabled (the plugin checkbox is checked);
    * see below for an example.

![PMS_agent_configuration](https://github.com/mrzhenya/plex-plugins/assets/9154225/8e002ba6-6f0f-475f-a390-0dc14515cf67)

4. Configure a new library in the Plex Media Server:
   * for `TV Shows` choose `Personal Media Shows` as the Agent and
     the `Plex Series Scanner` as the Scanner;
   * for `Movies` choose `Personal Media` as the Agent and
     the `Plex Movies Scanner` as the Scanner;
   * other settings should be set to defaults;
   * these settings could be found on the `Advanced` tab of the Add/Edit dialog (see below). 

![PMS_edit_library_dialog](https://github.com/mrzhenya/plex-plugins/assets/9154225/6dd4fa4d-3f30-409a-9158-a424f69f02f5)

## Media file organization and naming

If you have a considerable number of personal media files, it is best to organize them
as Plex Personal TV Shows. You will be able to group media files into Shows, which in turn,
will support multiple seasons. Examples are provided below.

### Personal TV Shows

Though Plex local media default support for Shows will recognize multiple episodes placed
in the same directory, this agent requires all single episode media assets to be nested
in its own single directory. More about Plex naming conventions could be found here -
[Naming and Organizing Your TV Show Files](https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/).

In the example below, `My Home Shows` is the root of our Plex TV Shows library, where
`Family Legacy` videos will appear as a single Show, and its videos are grouped into,
years which will appear as seasons. Note, that Plex will render a proper year number as
the season number (`2001` in our case). Most importantly, all files that correspond to
a single video (episode) are nested in a dedicated folder, named the same way as the
episode video file without the extension.

```
  /My Home Shows
    /Family Legacy
      background.jpg
      background-1.jpg
      poster.jpg
      show.info
      theme.mp3
      /Family-2001
        season-2001-background.jpg
        season-2001-poster.jpg
        /Family-2001 - s2001e01 - Easter Egg Hunt
          episode.info
          Family-2001 - s2001e01 - Easter Egg Hunt.jpg
          Family-2001 - s2001e01 - Easter Egg Hunt.mov
```

Note, that it's possible to use multiple episode images by appending thumb, e.g.
`Family-2001 - s2001e01 - Easter Egg Hunt-thumb1.jpg`.  In Plex, they are sorted
alphabetically, so `-thumb1.jpg` will take precedence over the default one in our
example.

Support for parsing the video, image, and audio (theme) content comes from the
default Local Media Assets agent; whereas our agent is responsible for parsing the
`.info` files, which are assumed to be named and located as in the example above.

To learn more about the format of the `.info` files, read the
[Info Files](#info-files) section.

### Personal Movies

Movie files can be placed in their own directories or all reside in a single folder.
More about Plex naming conventions could be found here -
[Naming and organizing your Movie files](https://support.plex.tv/articles/naming-and-organizing-your-movie-media-files/).

Here is an example:

```
  /My Home Movies
    Home Movie (1999).info
    Home Movie (1999).jpg
    Home Movie (1999).mp4
    Home Movie (2021).info
    Home Movie (2021).jpg
    Home Movie (2021).mov
```

## Info Files

Parsing files with `.info` extension is what this custom Plex Media Server agent
was created for. It's important to name these files appropriately; otherwise,
they will not be detected by the agent.

When creating your `.info` files, note that text for the text tags (e.g. `summary` )
could be placed on multiple lines, and empty or missing tags are ignored.

### Personal TV Shows

There are two versions of `.info` file that are used for media Shows - `show.info`
and `episode.info` files which are placed respectively in show and episode
directories.

Example of `show.info`:

```
[title]
Family Legacy
[summary]
My custom show title that is
placed on multiple lines.
[content_rating]
PG
[rating]
10.0
[studio]
My Home Studio
[originally_available_at]
2000-09-01
[collections]
Best of the best
My Shows
[genres]
Action
History
```

Example of `episode.info`:

```
[title]
April 2000 - Easter Egg Hunt
[summary]
[content_rating]
PG
[rating]
9.9
[originally_available_at]
2000-04-16
[directors]
[writers]
```

### Personal Movies

`.info` files for movies should have the same name as their corresponding
movie video files. For example, for a movie `Home Movie (2021).mp4`, the info
file should be named `Home Movie (2021).info`.

Here is an example of a movie info file:

```
[title]
REPLACE ME
[original_title]
REPLACE ME
[year]
1999
[originally_available_at]
1999-05-02
[tagline]
REPLACE ME
[summary]
REPLACE ME
[studio]
REPLACE ME
[rating]
9.9
[content_rating]
PG
[genres]
Drama
Romance
[countries]
USA
[collections]
Classics
```

Templates for the `.info` files could be found in the
[templates](https://github.com/mrzhenya/plex-plugins/tree/master/localmetadata/docs/templates)
directory.

## Debugging

When looking for Plex Media Server logs, search for the com.plexapp.agents.localmetadata
namespace.

When parsing local media assets, Plex default `Local Media` agent looks for the following
patterns:

```
    ... (show|poster|folder)-?[0-9]? (ext: ['jpg', 'png', 'jpeg', 'tbn'])
    ... banner-?[0-9]? (ext: ['jpg', 'png', 'jpeg', 'tbn'])
    ... (fanart|art|background|backdrop)-?[0-9]? (ext: ['jpg', 'png', 'jpeg', 'tbn'])
    ... theme-?[0-9]? (ext: ['mp3'])
```
