import xbmc
import xbmcgui
import xbmcplugin

import common
import os
import sys

class Main:
    def __init__( self ):
        self.addMainHomeItems()
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )

    
    def addMainHomeItems( self ):
        #space before " TV Shows" and " Movies" ensures that they are at the top of the list
        if common.settings['only_full_episodes']:
            common.addDirectory(" TV Shows", common.BASE_FULLTV_URL, "TV", xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),   xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),    genre = "list", plot = "A listing of all the Television Shows currently avaliable on Hulu.com")
        else:
            common.addDirectory(" TV Shows", common.BASE_TV_URL, "TV", xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),   xbmc.translatePath(os.path.join(common.imagepath,"tv_icon.png")),    genre = "list", plot = "A listing of all the Television Shows currently avaliable on Hulu.com")
        if common.settings['only_full_movies']:
            common.addDirectory(" Movies", common.BASE_FULLMOVIE_URL, "Movie", xbmc.translatePath(os.path.join(common.imagepath,"movie_icon.png")),xbmc.translatePath(os.path.join(common.imagepath,"movie_icon.png")), genre = "list", plot = "A listing of all the Movies currently avaliable on Hulu.com")
        else:
            common.addDirectory(" Movies", common.BASE_MOVIE_URL, "Movie", xbmc.translatePath(os.path.join(common.imagepath,"movie_icon.png")),xbmc.translatePath(os.path.join(common.imagepath,"movie_icon.png")), genre = "list", plot = "A listing of all the Movies currently avaliable on Hulu.com")

        #Leave this removed until H264 Streams Correctly
        #common.addDirectory("HD Gallery", common.HD_GALLERY_URL, "HD", xbmc.translatePath(os.path.join(common.imagepath,"hd_icon.png")), xbmc.translatePath(os.path.join(common.imagepath,"hd_icon.png")), genre = "HD", plot = "Sample the videos in our HD gallery to preview the future of online video quality today. Videos include trailers for Street Kings, The Indredible Hulk, Leatherheads, Step Brothers, Horton Hears a Who!...")
        #Temporarily removed because It Fucks Shit Up (TM)
        #common.addDirectory("Recently Added Shows", common.RSS_RECENT_SHOWS, "RSS",xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), genre = "rss")
        common.addDirectory("Recently Added Movies", common.RSS_RECENT_MOVIES, "RSS",xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), genre = "rss")
        common.addDirectory("Highest Rated Videos", common.RSS_HIGHEST_RATED, "RSS",xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), genre = "rss")
        common.addDirectory("Most Popular Videos Today", common.RSS_MOST_POP_TOD, "RSS",xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), genre = "rss")
        common.addDirectory("Most Popular Videos this Week", common.RSS_MOST_POP_WEEK, "RSS",xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), genre = "rss")
        common.addDirectory("Most Popular Videos this Month", common.RSS_MOST_POP_MON, "RSS",xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), genre = "rss")
        common.addDirectory("Most Popular Videos of All Time", common.RSS_MOST_POP_ALL, "RSS",xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), xbmc.translatePath(os.path.join(common.imagepath,"rss_icon.png")), genre = "rss")
        #common.addDirectory(name="Search",thumb=xbmc.translatePath(os.path.join(common.imagepath,"search_icon.png")),icon=xbmc.translatePath(os.path.join(common.imagepath,"search_icon.png")),genre="search")
            

