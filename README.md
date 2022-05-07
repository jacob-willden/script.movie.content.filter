# script.movie.content.filter
Kodi add-on for Movie Content Filter, to allow users to skip objectionable content on streaming services, based on their preferences.

Project Source Code Link: https://github.com/jacob-willden/script.movie.content.filter/

Movie Content Filter Website: https://www.moviecontentfilter.com/

## General Information
This project is in very early development right now, and there are many features to add (and some bugs to fix). It is built on the source code from the open-source VideoSkip browser extension (linked below). The source code is freely available to copy and build on, released under the GNU General Public License (GNU GPL).

VideoSkip Source Code Link: https://github.com/fruiz500/VideoSkip-extension/

## Installation Instructions

1. Download the source code as a ZIP file.
2. Launch the Kodi software.
3. Navigate to the Add-ons screen.
4. Click "Install from zip file".
5. Select the "script.movie.content.filter.zip" file.

## How to Use

1. Install the add-on based on the installation instructions above.
2. Create a filter file in the same folder as the video that you want to watch, with the same name as the video file except with the ".mcf" extension (for example, if you have a video called "Big Buck Bunny.mp4", then the filter file should be called "Big Buck Bunny.mcf" and be in the same folder).
3. Open the video with Kodi, and enjoy it without the objectionable content!

Here's how the filter file should be currently structured, with as many filter tags as you would like (this will be updated as needed):

    00:00:02 --> 00:00:04
    mute

    00:00:06.0 --> 00:00:08.0
    blank

    00:00:10.5 --> 00:00:12.75
    skip
    
    00:00:13.2 --> 00:00:15
    mute

## Legal

The add-on does not alter video files at all, but instead lets "users choose to see or not to see parts of the content, and the app remembers their choice" (quoted from the Read Me file for the VideoSkip extension [here](https://github.com/fruiz500/VideoSkip-extension/blob/master/README.md), which extension's code this add-on is built on). It also does not enable unauthorized access to video files.

The video content that our add-on can filter belongs to its respective copyright holders. We claim no affliation or endorsement from any of these copyright holders.

Notice to All Users: When watching a motion picture (referring to a movie, television show, etc) using this add-on, the performance of the motion picture is altered from the performance intended by the director or copyright holder of the motion picture.
