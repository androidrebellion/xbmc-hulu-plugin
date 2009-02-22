import xbmcplugin

import xbmc
import xbmcgui

import urllib
import urllib2
import sys
import os
import cookielib


"""
    PARSE ARGV
"""

class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )

exec "args = _Info(%s)" % (urllib.unquote_plus(sys.argv[2][1:].replace("&", ", ").replace('"','\'')), )




"""
    DEFINE URLS
"""
#location of main options
BASE_TV_URL        = "http://www.hulu.com/browse/alphabetical/clips"
BASE_FULLTV_URL    = "http://www.hulu.com/browse/alphabetical/episodes"
BASE_MOVIE_URL     = "http://www.hulu.com/browse/alphabetical/film_clips"
BASE_FULLMOVIE_URL = "http://www.hulu.com/browse/alphabetical/feature_film"
HD_GALLERY_URL     = "http://www.hulu.com/videos/slider?season=&category=Full%20Episodes&sort=original_premiere_date&hd_allowed=1&items_per_page=1000&show_id=164"
#rss feeds
RSS_RECENT_SHOWS   = "http://rss.hulu.com/HuluRecentlyAddedShows?format=xml"
RSS_RECENT_MOVIES  = "http://rss.hulu.com/HuluRecentlyAddedMovies?format=xml"
RSS_HIGHEST_RATED  = "http://www.hulu.com/feed/highest_rated/videos"
RSS_MOST_POP_TOD   = "http://rss.hulu.com/HuluPopularVideosToday?format=xml"
RSS_MOST_POP_WEEK  = "http://rss.hulu.com/HuluPopularVideosThisWeek?format=xml"
RSS_MOST_POP_MON   = "http://rss.hulu.com/HuluPopularVideosThisMonth?format=xml"
RSS_MOST_POP_ALL   = "http://rss.hulu.com/HuluPopularVideosAllTime?format=xml"
#define etc.
login_url   = "https://secure.hulu.com/account/authenticate"
profile_url = "http://www.hulu.com/users/profile/5129429"
search_url  = "http://www.hulu.com/videos/search?query="
rss_search  = "http://www.hulu.com/feed/search?query="
geo_check   = "http://releasegeo.hulu.com/geoCheck"
#define file locations
COOKIEFILE  = "cookies.lwp"
imagepath   = os.path.join(os.getcwd().replace(';', ''),'resources','images')







"""
    GET SETTINGS
"""

settings={}
#settings general
if xbmcplugin.getSetting( "resolution_hack" ) == "true" :
    settings['resolution_hack'] = True
else:
    settings['resolution_hack'] = False
settings['quality'] = xbmcplugin.getSetting("quality")
settings['gnash_path'] = xbmcplugin.getSetting("gnash_path")
#settings login
settings['login_name'] = xbmcplugin.getSetting( "login_name" )
settings['login_pass'] = xbmcplugin.getSetting( "login_pass" )

#settings TV
settings['flat_season'] = int(xbmcplugin.getSetting("flat_season"))

if xbmcplugin.getSetting("flat_tv_cats") == "true" :
    settings['flat_tv_cats'] = True
else:
    settings['flat_tv_cats'] = False
    
if xbmcplugin.getSetting('only_full_episodes') == "true" :
    settings['only_full_episodes'] = True
else:
    settings['only_full_episodes'] = False
    
if xbmcplugin.getSetting("get_show_plot") == "true" :
    settings['get_show_plot'] = True
else:
    settings['get_show_plot'] = False
    
if xbmcplugin.getSetting("get_episode_plot") == "true" :
    settings['get_episode_plot'] = True
else:
    settings['get_episode_plot'] = False

#settings Movies
if xbmcplugin.getSetting("flat_movie_cats") == "true" :
    settings['flat_movie_cats'] = True
else:
    settings['flat_movie_cats'] = False

if xbmcplugin.getSetting("only_full_movies") == "true" :
    settings['only_full_movies'] = True
else:
    settings['only_full_movies'] = False

if xbmcplugin.getSetting("get_movie_plot")  == "true" :
    settings['get_movie_plot'] = True
else:
    settings['get_movie_plot'] = False





"""
    Clean Non-Ascii characters from names for XBMC
"""

def cleanNames(string):
    try:
        string = string.replace("'","").replace(unicode(u'\u201c'), '"').replace(unicode(u'\u201d'), '"').replace(unicode(u'\u2019'),'\'').replace('&amp;','&').replace('&quot;','"')
        return string
    except:
        return string





"""
    ADD DIRECTORY
"""

try:
    args.fanart
except:
    args.fanart=''

def addDirectory(name, url='', mode='default', thumb='', icon='', fanart=args.fanart, plot='', genre=''):
    ok=True
    u = sys.argv[0]+'?url="'+urllib.quote_plus(url)+'"&mode="'+mode+'"&name="'+urllib.quote_plus(cleanNames(name))+'"&fanart="'+urllib.quote_plus(fanart)+'"&plot="'+urllib.quote_plus(cleanNames(plot))+'"&genre="'+cleanNames(genre)+'"'
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo( type="Video", infoLabels={ "Title":name, "Plot":cleanNames(plot), "Genre":genre})
    liz.setProperty('fanart_image',fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok




"""
    READ PAGE
"""

def getHTML( url ):
    print 'HULU --> common :: getHTML :: url = '+url
    cj = cookielib.LWPCookieJar()
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Referer', 'http://hulu.com'),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
    usock=opener.open(url)
    response=usock.read()
    usock.close()
    if os.path.isfile(COOKIEFILE):
        cj.save(COOKIEFILE)
    return response




"""
    ATTEMPT LOGIN
"""

def login():
    #don't do anything if they don't have a password or username entered
    if settings['login_name']=='' or settings['login_pass']=='':
        print "Hulu --> WARNING: Could not login.  Please enter a username and password in settings"
        return False

    cj = cookielib.LWPCookieJar()
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Referer', 'http://hulu.com'),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'),
                         ('Connection', 'keep-alive')]
    data =urllib.urlencode({"login":settings['login_name'],"password":settings['login_pass']})
    usock = opener.open(login_url, data)
    response = usock.read()
    usock.close()
    
    print 'HULU -- > These are the cookies we have received:'
    for index, cookie in enumerate(cj):
        print 'HULU--> '+str(index)+': '+str(cookie)
        
    print "HULU --> login_url response (we want 'ok=1'): " + response
    if response == 'ok=1':
        loggedIn = True
    else:
        loggedIn = False
    
    

    



