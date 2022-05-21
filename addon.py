"""
This file is part of the Movie Content Filter Kodi Add-on Project.

Movie Content Filter Kodi Add-on Project Copyright (C) 2021, 2022 Jacob Willden
(Released under the GNU General Public License (GNU GPL) Version 3.0 or later)

VideoSkip Browser Extension Copyright (C) 2020, 2021, 2022 Francisco Ruiz
(Released under the GNU General Public License (GNU GPL))
Link: https://github.com/fruiz500/VideoSkip-extension/

LazyTV Kodi Add-on (C) 2013, 2014, 2015 KodeKarnage
(Released under the GNU General Public License (GNU GPL) Version 2.0 or later)
Link: https://github.com/KODeKarnage/script.lazytv

Most of the code below was derived and modified from several source 
code files in the VideoSkip browser extension repository (source 
link above), including "content1.js" and "content2.js", and it is 
explicitly labled as so. One snippet of code below is derived from 
the file "service.py" in the LazyTV Kodi Add-on, also explicitly 
labeled as so.

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

import xbmc, xbmcaddon, xbmcgui, os, re

ADDON = xbmcaddon.Addon()
addonpath = ADDON.getAddonInfo("path")

if (__name__ == "__main__"):
    print("filter addon starting")

    # From "content2.js" from VideoSkip
    # hour:minute:second string to decimal seconds
    def fromHMS(timeString):
        timeString = timeString.replace(",", ".") # in .srt format decimal seconds use a comma
        time = timeString.split(":")
        if len(time) == 3: # has hours
            return (int(time[0]) * 3600) + (int(time[1]) * 60) + float(time[2])
        elif len(time) == 2: # minutes and seconds
            return (int(time[0]) * 60) + float(time[1])
        else: # only seconds
            return float(time[0])

    def parseTagActionInfo(rawText): # 2 tags at the same time?
        category = ""
        severity = ""
        action = ""

        textWithoutComment = rawText.split(" #")[0] # Eliminate tag comments
        textArray = textWithoutComment.split("=")
        
        category = textArray[0]

        if textArray[1] == "high":
            severity = 3
        elif textArray[1] == "medium":
            severity = 2
        elif textArray[1] == "low":
            severity = 1

        if len(textArray) == 2 or textArray[2] == "both":
            action = "skip"
        elif textArray[2] == "video":
            action = "blank"
        elif textArray[2] == "audio":
            action = "mute"
        
        return [category, severity, action]


    def parseFilterFileText(fileText):
        # Modified from code by nqngo at Stack Overflow, used to separate timestamps in the filter file from the tag descriptions
        # https://stackoverflow.com/questions/23620423/parsing-a-srt-file-with-regex
        result = re.findall("(\d+:\d+:\d+.*\d* --> \d+:\d+:\d+.*\d*)\s+(.+)", fileText)

        allCuts = []
        for myTuple in result:
            currentCut = {}
            times = myTuple[0].split(" --> ")
            currentCut["startTime"] = fromHMS(times[0])
            currentCut["endTime"] = fromHMS(times[1])

            actionInfo = parseTagActionInfo(myTuple[1])
            currentCut["category"] = actionInfo[0]
            currentCut["severity"] = actionInfo[1]
            currentCut["action"] = actionInfo[2]
            allCuts.append(currentCut)
        
        return allCuts
        
    userSettings = {}

    def updateUserSettings():
        categoryIdList = ["commercial", "advertBreak", "consumerism", "productPlacement", "discrimination", "ableism", "adultism", "antisemitism", "genderism", "homophobia", "misandry", "misogyny", "racism", "sexism", "sizeism", "supremacism", "transphobia", "xenophobia", "dispensable", "idiocy", "tedious", "drugs", "alcohol", "antipsychotics", "cigarettes", "depressants", "gambling", "hallucinogens", "stimulants", "fear", "accident", "acrophobia", "aliens", "arachnophobia", "astraphobia", "aviophobia", "chemophobia", "claustrophobia", "coulrophobia", "cynophobia", "death", "dentophobia", "emetophobia", "enochlophobia", "explosion", "fire", "gerascophobia", "ghosts", "graves", "hemophobia", "hylophobia", "melissophobia", "misophonia", "musophobia", "mysophobia", "nosocomephobia", "nyctophobia", "siderodromophobia", "thalassophobia", "vampires", "language", "blasphemy", "nameCalling", "sexualDialogue", "swearing", "vulgarity", "nudity", "bareButtocks", "exposedGenitalia", "fullNudity", "toplessness", "sex", "adultery", "analSex", "coitus", "kissing", "masturbation", "objectification", "oralSex", "premaritalSex", "promiscuity", "prostitution", "violence", "choking", "crueltyToAnimals", "culturalViolence", "desecration", "emotionalViolence", "kicking", "massacre", "murder", "punching", "rape", "slapping", "slavery", "stabbing", "torture", "warfare", "weapons"]
        global userSettings
        userSettings = {}
        for category in categoryIdList:
            userSettings[category] = ADDON.getSetting(category)

    # Modified from isSkipped function from "content2.js" from VideoSkip
    def isTagActive(tag, userSettings):
        category = tag["category"]
        return int(tag["severity"]) + int(userSettings[category]) > 3

    activeCuts = []

    # Modified from isSkipped function from "content2.js" from VideoSkip
    def applyFilters(allCuts, userSettings):
        global activeCuts
        activeCuts = []
        for cut in allCuts:
            if isTagActive(cut, userSettings):
                activeCuts.append(cut)
        return activeCuts

    def loadFilterFile():
        try:
            filePath = xbmc.Player().getPlayingFile().rsplit(".", 1)[0] + ".mcf"
            fileInput = open(filePath, "r")
            fileText = fileInput.read()
            allCuts = parseFilterFileText(fileText)
            updateUserSettings()
            global userSettings
            activeCuts = applyFilters(allCuts, userSettings)
            # displayLegalNotice? What about subtitles? Maybe check if it's already popped up?
        except:
            print("Unable to find or process MCF file")

    # Modified from the LazyMonitor class from "service.py" from LazyTV
    class AppMonitor(xbmc.Monitor):
        def __init__(self, *args, **kwargs):
            xbmc.Monitor.__init__(self)

        def onSettingsChanged(self):
            updateUserSettings()

    monitor = AppMonitor()

    class XBMCPlayer(xbmc.Player):
        def __init__(self, *args):
            pass
        def onAVChange(self):
            loadFilterFile()

    player = XBMCPlayer()

    class OverlayBlankScreen(object):
        def __init__(self):
            self.showing = False
            self.window = xbmcgui.Window(12005) # Inheriting from 12005 keeps the black background from overlaying the interface
            origin_x = 0
            origin_y = 0
            # Since Kodi seems to usually report a smaller screen width and height than there really is, multiplying the values can be a hacky way to make sure the whole screen is covered when hiding the video
            window_w = int(xbmc.getInfoLabel("System.ScreenWidth")) * 100
            window_h = int(xbmc.getInfoLabel("System.ScreenHeight")) * 100

            #main window
            self._background = xbmcgui.ControlImage(origin_x, origin_y, window_w, window_h, os.path.join(addonpath,"resources","skins","default","media","black-background.png"))

        def show(self):
            if not self.showing:
                self.showing=True
                self.window.addControl(self._background)

        def hide(self):
            if self.showing:
                self.showing=False
                self.window.removeControl(self._background)

        def _close(self):
            if self.showing:
                self.hide()
            else:
                pass
            try:
                self.window.clearProperties()
                #print("OverlayBlankScreen window closed")
            except: pass

    prevAction = ""

    # Execute filters during playback, derived and modified from anonymous function in "content1.js" from VideoSkip (version 0.4.1), originally "content2.js"
    def doTheFiltering(prevAction, activeCuts, blankScreen):
        startTime = 0
        endTime = 0
        action = ""
        tempAction = ""
        for tag in activeCuts:
            startTime = tag["startTime"]
            endTime = tag["endTime"]
            currentTime = xbmc.Player().getTime()
            if currentTime > startTime and currentTime < endTime:
                tempAction = tag["action"]
            else:
                tempAction = ""

            if tempAction == "skip": # Retain the strongest action valid for the current time. Hierarchy: skip > blank > mute
                action = "skip"
                break # Can't get any stronger, so stop looking for this time
            elif tempAction == "blank":
                if action == "skip":
                    action = action
                else:
                    action = tempAction
            elif tempAction == "mute":
                if action == "skip":
                    action = action
                else:
                    if action == "blank":
                        action = "skip"
                    else:
                        action = "mute"
            
        if action == prevAction:
            return prevAction
        elif action == "skip":
            xbmc.Player().seekTime(float(endTime) + 0.1)
        elif action == "blank":
            blankScreen.show()
        elif action == "mute":
            xbmc.executebuiltin("SetVolume(0)")
        else:
            xbmc.executebuiltin("SetVolume(100)")
            blankScreen.hide()
        prevAction = action
        return prevAction

    while not monitor.abortRequested():
        if monitor.waitForAbort(0.01):
            break
        if xbmc.getCondVisibility("Player.HasMedia"):
            if not "blankScreen" in locals():
                blankScreen = OverlayBlankScreen()
            prevAction = doTheFiltering(prevAction, activeCuts, blankScreen)
            

# To Do List:
# Family Movie Act of 2005 notice
# Filtering editor (how to activate? keyboard shortcut?)