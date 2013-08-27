#!/usr/bin/python

"""
Copyright (c) 2013 Michael Flau <michael@flau.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
askIMDB.py
----------

A simple collection of classes which enable the
user to make requests to the IMDB database.
It can also be used as a console based tool,
for requesting information about a movie from
the internet movie database.

Usage as module:
----------------

Simply put 'import askIMDB'
to the head of your script an
instantiate the classes you need
for your purpose.

Usage as standalone app:
------------------------

Trigger app with:

'python askIMDB.py MOVIENAME [[--if=[peymkrbta]] [--of=[rgludkicowtpynesma]]]'

Input Flags
-----------

'--if=' - represent the input flags, by which the request can be made more "demanding"
in terms how much information about a movie is requested

flag explanation:

p - Plot

Will request full plot information instead of basic information

e - Episode

Only interesting if information about a TV show is requested.
This will request a full list overview of the single episodes
of the TV show.

y - YG

m - mt

k - Aka

This will request a complete list of names under which the
movie is known in other countries.

r - Release

Triggers the app to request a complete overview of the release date

b - Business

This flag will request business information about the movie, if not
set, the information won't be requested.

t - Technical

Returns information like 'aspect ratio' or the 'film negative format'.
If not set no technical information will be requested.

a - All

Will enable all switches described prior to this one.


Output Flags
------------

'--of=' - represent the output flags, by which the generated output of the app is shaped

r - Rating

Displays the average Rating of the movie.

g - Genres

Displays the movies genres.

l - Language

Displays the native language of the movie

u - IMDB URL

Displays the URL under which the movie is listed at IMDB.com

d - Directors

Displays the directors of the movie.

k - Aka

Displays names of the movie under which the
movie is also known.

i - IMDB Id

Displays the Id of the movie under which
it is listed in the IMDB database
(A bit of redundance here ;) ).

c - Country

Displays the countries in which the
movie were made.

o - Locations

Displays the filming locations of
the movie.

w - Writers

Lists all the writers incorporated
with the movie.

t - Actors

Lists all the main actors of the movie.

p - Plot

Will print the plot of the movie.

y - Year

Will print the year in which the
movie was released.

n - Runtime

Displays the runtime of the movie.

e - Type

Displays the rating of movie according
to the MPAA.

s - Release

Displays the release date of the movie.

m - Rating count

Displays how many people rated this movie.

a - All

Triggers all switched mentioned prior
in this section.
"""

import json
import sys
from urllib2 import urlopen

class IMDBFlagInterpreter(object):
    m_Values = {}
    m_FormattingFlags = {}
    m_Flags  = 0x00
    m_OFlags = 0x00
    m_bReady = False

    #Request flags
    PLOT      = 0x01 # p
    EPISODE   = 0x02 # e
    YG 	      = 0x04 # y
    MT 	      = 0x08 # m
    AKA	      = 0x10 # k
    RELEASE   = 0x20 # r
    BUSINESS  = 0x40 # b
    TECHNICAL = 0x80 # t
    ALL	      = 0xff # a

    #Response formatting flags
    RATING 	= 0x00001 # r
    GENRES 	= 0x00002 # g
    LANGUAGE 	= 0x00004 # l
    IMDB_URL	= 0x00008 # u
    DIRECTORS	= 0x00010 # d
    AKA		= 0x00020 # k
    IMDB_ID	= 0x00040 # i
    COUNTRY	= 0x00080 # c
    LOCATIONS	= 0x00100 # o
    WRITERS	= 0x00200 # w
    ACTORS	= 0x00400 # t
    PLOT	= 0x00800 # p
    YEAR	= 0x01000 # y
    RUNTIME	= 0x02000 # n
    TYPE	= 0x04000 # e
    RELEASE	= 0x08000 # s
    RATING_CNT	= 0x10000 # m
    ALL2	= 0x1ffff # a

    """
    __init__()
    """
    def __init__(self):
        pass

    """
    __init__()
    """
    def __init__(self, flags):
        self.process(flags)

    """
    process()
    """
    def process(self, flags):
        self.m_bReady = self.extractFlags(flags)

        if self.m_bReady:
            self.m_Values = self.interpretRequestFlags()
            self.m_FormattingFlags = self.interpretResponseFlags()
            self.m_Values['title'] = flags[1]
        else:
            self.usage()

    """
    usage()
    """
    def usage(self):
        print "Usage: ./askIMDB.py MOVIENAME [[--if=[peymkrbta]] [--of=[rgludkicowtpynesma]]]"

    """
    isReady()
    """
    def isReady(self):
        return self.m_bReady

    """
    extractFlags()
    """
    def extractFlags(self, flags):

        argCount = len(flags)

        if argCount < 2:
            return False

        elif argCount == 3 :
            if flags[2][0:5] == '--if=':
                self.extractRequestFlags(flags[2])
            elif flags[2][0:5] == '--of=':
                self.extractResponseFlags(flags[2])
            else:
                return False

        elif argCount == 4:
           for item in flags[2:]:
               if item[0:5] == '--if=':
                   self.extractRequestFlags(item)

               elif item[0:5] == '--of=':
                   self.extractResponseFlags(item)

               elif argCount > 4:
                   return False

           return True


    """
    extractRequestFlags()
    """
    def extractRequestFlags(self, flags):
        for char in flags[5:]:

            if char == 'p':
                self.m_Flags |= self.PLOT

            elif char == 'e':
                self.m_Flags |= self.EPISODE

            elif char == 'y':
                self.m_Flags |= self.YG

            elif char == 'm':
                self.m_Flags |= self.MT

            elif char == 'k':
                self.m_Flags |= self.AKA

            elif char == 'r':
                self.m_Flags |= self.RELEASE

            elif char == 'b':
                self.m_Flags |= self.BUSINESS

            elif char == 't':
                self.m_Flags |= self.TECHNICAL

            elif char == 'a':
                self.m_Flags |= self.ALL

            else:
                self.usage()

    """
    interpretRequestFlags()
    """
    def interpretRequestFlags(self):

        values = {}

        if (self.m_Flags & self.PLOT) != 0:
            values['plot'] = 'full'
        else:
            values['plot'] = 'simple'

        if (self.m_Flags & self.EPISODE) != 0:
            values['episode'] = '1'
        else:
            values['episode'] = '0'

        if (self.m_Flags & self.YG) != 0:
            values['yg'] = '1'
        else:
            values['yg'] = '0'

        if (self.m_Flags & self.MT) != 0:
            values['mt'] = '1'
        else:
            values['mt'] = '0'

        if (self.m_Flags & self.AKA) != 0:
            values['aka'] = 'full'
        else:
            values['aka'] = 'simple'

        if (self.m_Flags & self.RELEASE) != 0:
            values['release'] = 'full'
        else:
            values['release'] = 'simple'

        if (self.m_Flags & self.BUSINESS) != 0:
            values['business'] = '1'
        else:
            values['business'] = '0'

        if (self.m_Flags & self.TECHNICAL) != 0:
            values['technical'] = '1'
        else:
            values['technical'] = '0'

        return values

    """
    extractResponseFlags()
    """
    def extractResponseFlags(self, flags):
        for char in flags[5:]:

            if char == 'r':
                self.m_OFlags |= self.RATING
            elif char == 'g':
                self.m_OFlags |= self.GENRES
            elif char == 'l':
                self.m_OFlags |= self.LANGUAGE
            elif char == 'u':
                self.m_OFlags |= self.IMDB_URL
            elif char == 'd':
                self.m_OFlags |= self.DIRECTORS
            elif char == 'k':
                self.m_OFlags |= self.AKA
            elif char == 'i':
                self.m_OFlags |= self.IMDB_ID
            elif char == 'c':
                self.m_OFlags |= self.COUNTRY
            elif char == 'o':
                self.m_OFlags |= self.LOCATIONS
            elif char == 'w':
                self.m_OFlags |= self.WRITERS
            elif char == 't':
                self.m_OFlags |= self.ACTORS
            elif char == 'p':
                self.m_OFlags |= self.PLOT
            elif char == 'y':
                self.m_OFlags |= self.YEAR
            elif char == 'n':
                self.m_OFlags |= self.RUNTIME
            elif char == 'e':
                self.m_OFlags |= self.TYPE
            elif char == 's':
                self.m_OFlags |= self.RELEASE
            elif char == 'm':
                self.m_OFlags |= self.RATING_CNT
            elif char == 'a':
                self.m_OFlags |= self.ALL2
            else:
                self.usage()

	"""
        #interpretResponseFlags()
        """
    def interpretResponseFlags(self):
        values = {}

        if (self.m_OFlags & self.RATING) != 0:
            values['rating'] = True
        else:
            values['rating'] = False

        if (self.m_OFlags & self.GENRES) != 0:
            values['genres'] = True
        else:
            values['genres'] = False

        if (self.m_OFlags & self.LANGUAGE) != 0:
            values['language'] = True
        else:
            values['language'] = False

        if (self.m_OFlags & self.IMDB_URL) != 0:
            values['imdb_url'] = True
        else:
            values['imdb_url'] = False

        if (self.m_OFlags & self.DIRECTORS) != 0:
            values['directors'] = True
        else:
            values['directors'] = False

        if (self.m_OFlags & self.AKA) != 0:
            values['also_known_as'] = True
        else:
            values['also_known_as'] = False

        if (self.m_OFlags & self.IMDB_ID) != 0:
            values['imdb_id'] = True
        else:
            values['imdb_id'] = False

        if (self.m_OFlags & self.COUNTRY) != 0:
            values['country'] = True
        else:
            values['country'] = False

        if (self.m_OFlags & self.LOCATIONS) != 0:
            values['filming_locations'] = True
        else:
            values['filming_locations'] = False

        if (self.m_OFlags & self.WRITERS) != 0:
            values['writers'] = True
        else:
            values['writers'] = False

        if (self.m_OFlags & self.ACTORS) != 0:
            values['actors'] = True
        else:
            values['actors'] = False

        if (self.m_OFlags & self.PLOT) != 0:
            values['plot_simple'] = True
            values['plot'] = True
        else:
            values['plot_simple'] = False
            values['plot'] = False

        if (self.m_OFlags & self.YEAR) != 0:
            values['year'] = True
        else:
            values['year'] = False

        if (self.m_OFlags & self.RUNTIME) != 0:
            values['runtime'] = True
        else:
            values['runtime'] = False

        if (self.m_OFlags & self.TYPE) != 0:
            values['type'] = True
        else:
            values['type'] = False

        if (self.m_OFlags & self.RELEASE) != 0:
            values['release_date'] = True
        else:
            values['release_date'] = False

        if (self.m_OFlags & self.RATING_CNT) != 0:
            values['rating_count'] = True
        else:
            values['rating_count'] = False

        return values

class AbstractRESTRequester(object):
    m_bDebugMode = False
    m_sBaseURL = ""

    def __init__(self):
        pass

    #Prints debug information
    def dPrint(self, msg):
        if self.m_bDebugMode:
            print msg

    #Change base URL at runtime
    def redefineBaseURL(url):
        m_sBaseURL = url

    #Set debug mode
    def setDebugMode(self, mode):
        if mode:
            m_bDebugMode = True
        else:
            m_bDebugMode = False

class IMDBRequester(AbstractRESTRequester):

    m_sBaseURL = "http://imdbapi.org/?"
    m_sRequest = ""
    m_bReady  = False
    m_lParts  = []

    def __init__(self, parsedInfo):
        self.dPrint("Init imdb requester object!")
        self.setParts(parsedInfo)
        self.buildRequest()

    def setParts(self, parsedInfo):
        self.m_lParts = []
        self.m_lParts.append("title=" + parsedInfo["title"])
        self.m_lParts.append("type=json")
        self.m_lParts.append("plot=" + parsedInfo["plot"])
        self.m_lParts.append("episode=" + parsedInfo["episode"])
        self.m_lParts.append("limit=1")
        self.m_lParts.append("yg=" + parsedInfo["yg"])
        self.m_lParts.append("mt=" + parsedInfo["mt"])
        self.m_lParts.append("lang=en-US")
        self.m_lParts.append("offset=")
        self.m_lParts.append("aka=" + parsedInfo["aka"])
        self.m_lParts.append("release=" + parsedInfo["release"])
        self.m_lParts.append("business=" + parsedInfo["business"])
        self.m_lParts.append("tech=" + parsedInfo["technical"])

    def buildRequest(self):

        self.dPrint("Building request!")
        self.m_sRequest = self.m_sBaseURL

        for part in self.m_lParts:
            self.m_sRequest += ("&" + part)

            self.dPrint("Request: " + self.m_sRequest)
            self.m_bReady = True

    def makeRequest(self):
        if self.m_bReady:
            rqObject = urlopen(self.m_sRequest)
            response = json.load(rqObject)
            return response
        else:
            print "Request string is invalid!"

class IMDBResponsePrinter(object):
    m_OutputString = ""

    def __init__(self):
        pass

    def resetOutputString(self):
        self.m_OutputString = ""

    def setHead(self, head):
        self.m_OutputString = head

    def printTitle(self, title):
        cnt = len(title)
        print '+' + '*' * (cnt + 2) + '+'
        print '* ' + title + ' *'
        print '+' + '*' * (cnt + 2) + '+'

    def printBaseValue(self, value, recursion, key = None):

        head = ""
        retVal = False

        for item in self.m_OutputString:
            head += item

        if isinstance(value, (int, float)):
            print head + " " + str(value)
            retVal = True
        elif isinstance(value, (basestring)):
            print head + " " + value
            retVal = True

        self.resetOutputString()
        return retVal



    def checkForSubLevel(self, item, recursion):
        if self.printBaseValue(item, recursion + 1):
            return

        if isinstance(item, list):
            for subitem in item:
                self.checkForSubLevel(subitem, recursion)
        elif isinstance(item, dict):
            for key in item.keys():
                tmp = "\t" * recursion, key + ":"
                self.setHead(tmp)
                self.checkForSubLevel(item[key], recursion + 1)

    def printResponse(self, response, formatting):
        print response
        print
        print formatting

        for item in response:
            self.printTitle(item['title'])
            print

            for key in formatting.keys():
                if formatting[key] and key in item.keys():
                    self.setHead(key + ":")
                    self.checkForSubLevel(item[key], 1)
                    print

    def checkResponse(self, response):
        for item in response:
            keys = item.keys()

            for key in keys:
                if key == 'error' and item[key] == 'Film not found':
                    return False

        return True

"""
__main__

In order to use this script as standalone
app the single objects are used to make a
request which is then printed to stdout.
"""
if __name__ == "__main__":
    #pass cmd args to interpreter
    myInterpreter = IMDBFlagInterpreter(sys.argv)

    #check if interpreter is ready
    if myInterpreter.isReady():
        #Create a request object
        #depending on passed arguments
        myRequester = IMDBRequester(myInterpreter.m_Values)

        #make request to IMDB database
        answer = myRequester.makeRequest()

        #create a printer object
        myPrinter = IMDBResponsePrinter()

        #check answer if the film were found
        if not IMDBResponsePrinter().checkResponse(answer):
            print 'Film not found!'
            sys.exit(-1)

        #print response with formatting extracted from cmd line args
        myPrinter.printResponse(answer, myInterpreter.m_FormattingFlags)
    else:
        sys.exit(-1)

