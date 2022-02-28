"""
This file is part of the Movie Content Filter Kodi Add-on Project.

Movie Content Filter Kodi Add-on Project Copyright (C) 2021, 2022 Jacob Willden
(Released under the GNU General Public License (GNU GPL) Version 3.0 or later)

VideoSkip Source Code Copyright (C) 2020, 2021 Francisco Ruiz
(Released under the GNU General Public License (GNU GPL))
Link: https://github.com/fruiz500/VideoSkip-extension/

TvSkipIntro Add-on Copyright (C) 2018 aenema
(Released under the GNU General Public License (GNU GPL) Version 3.0 or later)
Link: https://github.com/aenemapy/aenemapyrepo

Most of the code below was derived and modified from several source 
code files in the VideoSkip browser extension repository (source 
link above), including "content1.js", "content2.js", and 
"videoskip.js", and it is explicitly labled as so. Some of the code
below was derived and modified from the "service.py" source code 
file in the TvSkipIntro Add-on inside the "aenemapyrepo" repository
(source link above), and it is explicitly labled as so.

Afformentioned source code derived and modified by Jacob Willden
Start Date of Derivation/Modification: November 20, 2020
Most Recent Date of Derivation/Modification: February 28, 2022

"Movie Content Filter" Website Copyright (C) delight.im
Website Link: https://www.moviecontentfilter.com/

The Movie Content Filter Kodi Add-on Project is free software: 
you can redistribute it and/or modify it under the terms of the GNU
General Public License (GNU GPL) as published by the Free Software
Foundation, either version 3 of the License, or (at your option)
any later version. The project is distributed WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU GPL for more details.

As additional permission under GNU GPL version 3 section 7, you
may distribute non-source (e.g., minimized or compacted) forms of
the code without the copy of the GNU GPL normally required by
section 4, provided you include this license notice and a URL
through which recipients can access the Corresponding Source.

You should have recieved a copy of the GNU General Public License
along with this project. Otherwise, see: https://www.gnu.org/licenses/
"""

import xbmc
import xbmcaddon
import xbmcgui

if (__name__ == '__main__'):
    print("filter addon working")

    allCuts = [
        {"startTime": 10, "endTime": 12, "category": "gambling", "severity": 1, "action": "mute"},
        {"startTime": 17, "endTime": 19, "category": "gambling", "severity": 1, "action": "blank"},
        {"startTime": 24, "endTime": 26, "category": "gambling", "severity": 1, "action": "skip"},
        {"startTime": 31, "endTime": 33, "category": "gambling", "severity": 1, "action": "fast"},
        {"startTime": 38, "endTime": 40, "category": "gambling", "severity": 1, "action": "blur"},
        {"startTime": 45, "endTime": 47, "category": "tedious", "severity": 2, "action": "mute"},
        {"startTime": 52, "endTime": 54, "category": "tedious", "severity": 2, "action": "blank"},
        {"startTime": 59, "endTime": 61, "category": "warfare", "severity": 2, "action": "skip"},
        {"startTime": 66, "endTime": 68, "category": "warfare", "severity": 3, "action": "mute"},
        {"startTime": 73, "endTime": 75, "category": "warfare", "severity": 3, "action": "blank"},
        {"startTime": 80, "endTime": 82, "category": "warfare", "severity": 3, "action": "skip"},
        {"startTime": 87, "endTime": 89, "category": "warfare", "severity": 3, "action": "blank"},
        {"startTime": 87.5, "endTime": 88.5, "category": "warfare", "severity": 3, "action": "skip"}
    ]

    #print(allCuts[0]["startTime"])
    #for tag in allCuts:
    #    print("startTime:", tag["startTime"], "endTime:", tag["endTime"], sep="")

    prevAction = ""

    # Execute filters during playback, derived and modified from anonymous function in "content1.js" from VideoSkip (version 0.4.1), originally "content2.js"
    def doTheFiltering(currentTime):
        startTime = 0
        endTime = 0
        action = ""
        global prevAction
        #print("currentTime: ", currentTime, sep="")
        for tag in allCuts: # change allCuts to activeCuts
            startTime = tag["startTime"]
            endTime = tag["endTime"]
            if currentTime > startTime and currentTime < endTime:
                action = tag["action"]
                break
            # add overlapping filter handling here
        #print("current action:", action, sep="")
        if action == prevAction:
            return
        elif action == "skip":
            xbmc.Player().seekTime(float(endTime) + 0.1)
        elif action == "blank":
            # figuring out how to implement this
            pass
        elif action == "mute":
            xbmc.executebuiltin('Mute')
        else:
            xbmc.executebuiltin('Mute') # Unmute
            # un-blank
        prevAction = action
        return

    # Derived and modified from the ServiceEntryPoint function in "service.py" from TvSkipIntro
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        try:
            if xbmc.Player().isPlaying():
                xbmc.sleep(10)
                currentTime = xbmc.Player().getTime()
                doTheFiltering(currentTime)
        except:
            pass

# How to display Family Movie Act of 2005 notice?