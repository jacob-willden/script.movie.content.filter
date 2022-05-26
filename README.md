# script.movie.content.filter
Kodi add-on for Movie Content Filter, to allow users to skip objectionable content on streaming services, based on their preferences.

Project Source Code Link: https://github.com/jacob-willden/script.movie.content.filter/

Movie Content Filter Website: https://www.moviecontentfilter.com/

## General Information
This project is in very early development right now, and there are many features to add (and some bugs to fix). It is built on the source code from the open-source VideoSkip browser extension (linked below). The source code is freely available to copy and build on, released under the GNU General Public License (GNU GPL).

VideoSkip Source Code Link: https://github.com/fruiz500/VideoSkip-extension/

## Installation Instructions

1. Make sure you have Kodi installed on a device (see the [tutorial on the Kodi Wiki](https://kodi.wiki/view/Installing)). Kodi version 19 or later is currently required.
2. Download the source code for the add-on as a ZIP file.
3. Launch the Kodi software.
4. Navigate to the Add-ons screen.
5. Click "Install from zip file".
6. Select the "script.movie.content.filter.zip" file.

## How to Use

1. Install the add-on based on the installation instructions above.
2. Adjust the add-on settings so the add-on will filter (or not filter) certain content from videos based on your preferences. With the number value for each category in the settings, 0 means nothing will be filtered in that category, 1 means only high severity content will be filtered in that category, 2 means high and medium severity content will be filtered in that category, and 3 means all content (high, medium, and low severity) in that category will be filtered. The settings can be accessed by finding the add-on in the Add-ons screen, bringing up the add-on's Context Menu, and clicking Settings (see the [Add-ons article on the Kodi Wiki](https://kodi.wiki/view/Add-ons) for more information). 
3. Create a filter file in the same folder as the video that you want to watch, with the same name as the video file except with the ".mcf" extension (for example, if you have a video called "Big Buck Bunny.mp4", then the filter file should be called "Big Buck Bunny.mcf" and be in the same folder).
4. Open the video with Kodi, and enjoy it without the objectionable content!

Here's how the filter file should be currently structured, with as many filter tags as you would like (this will be updated as needed):

    00:00:02 --> 00:00:04
    language=high=audio

    00:00:06.0 --> 00:00:08.0
    objectification=medium=video

    00:00:10.5 --> 00:00:12.75
    punching=low=both # A comment
    
    00:00:13.2 --> 00:00:15
    nameCalling=low=audio

Categories for filters can be found in the [Movie Content Filter specifications](https://www.moviecontentfilter.com/specification), with 2 changes. One change is that the "Grave" (represented as "grave" in filter files) is replaced with "Graves" (with "graves" in the filter file). The other change is the addition of the Ableism ("ableism" in filter files) and Sizeism ("sizeism" in filter files) categories.

## Legal

The add-on does not alter video files at all, but instead lets "users choose to see or not to see parts of the content, and the app remembers their choice" (quoted from the [Read Me file for the VideoSkip extension](https://github.com/fruiz500/VideoSkip-extension/blob/master/README.md), which extension's code this add-on is built on). It also does not enable unauthorized access to video files.

The video content that our add-on can filter belongs to its respective copyright holders. We claim no affliation or endorsement from any of these copyright holders.

Notice to All Users: When watching a motion picture (referring to a movie, television show, etc) using this add-on, the performance of the motion picture is altered from the performance intended by the director or copyright holder of the motion picture.
