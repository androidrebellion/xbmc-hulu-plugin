import xbmcplugin
import common
import sys
import re
from BeautifulSoup import BeautifulStoneSoup

class Main:

    def __init__( self ):
        if common.args.mode == 'RSS_Shows':
            self.activateShowPage()
        else:
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            self.addListings()
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))


    def activateShowPage( self ):
        import xbmc, urllib
        print 'executing--> %s?url="%s"&mode="TV_Seasons"&name="%s"&fanart="%s"&plot="%s"&genre="%s")' % (sys.argv[0], urllib.quote_plus(common.args.url), common.args.name, urllib.quote_plus(common.args.fanart), common.args.plot, common.args.genre)
        xbmc.executebuiltin('XBMC.activatewindow(MyVideoLibrary,%s?url="%s"&mode="TV_Seasons"&name="%s"&fanart="%s"&plot="%s"&genre="%s")' % (sys.argv[0], urllib.quote_plus(common.args.url), common.args.name, urllib.quote_plus(common.args.fanart), common.args.plot.replace(',',' ').replace('"',''), common.args.genre))


    def addListings ( self ):
        xmlsoup = BeautifulStoneSoup(common.getHTML( common.args.url ))
        items = xmlsoup.findAll('item')
        for item in items:
            name = item.title.contents[0]
            url  = item.guid.contents[0]
            try:
                try:
                    p = re.compile('&lt;p&gt;(.+?)&lt;/p&gt;')
                    plot = p.findall(item.description.contents[0])[0]
                except:
                    p = re.compile('<p>(.+?)</p>')
                    plot = p.findall(str(item.description))[0]
            except:
                plot = 'Unavaliable'
            try:
                p = re.compile('media:thumbnail.+?url="(.+?)"')
                thumb = p.findall(str(item))[0]
            except:
                thumb = ''
            try:
                fanart = 'http://assets.hulu.com/shows/key_art_'+name.split(':')[0].replace('-','_').replace(' ','_').replace('\'','').replace('"','').lower()+'.jpg'
            except:
                fanart = ''

            genre = common.args.name

            if common.args.name == 'Recently Added Shows':
                common.addDirectory(name, url, 'RSS_Shows', thumb, thumb, fanart, plot, genre)
            else:
                common.addDirectory(name, url, 'RSS_play', thumb, thumb, fanart, plot, genre)
