import xbmcplugin
import common
import sys
from BeautifulSoup import BeautifulSoup


class Main:

    def __init__( self ):
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        self.addListings()
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))

    def addListings( self ):
        tree = BeautifulSoup(common.getHTML(common.args.url))
        items = tree.findAll('li')
        for item in items:
            link  = item.findAll('a','info_hover')
            url   = link[0]['href']
            name  = common.cleanNames(link[-1].contents[0])
            thumb = item.find('img')['src']
            print name
            print url
            print thumb
            common.addDirectory(name, url, 'HD_play', thumb, thumb)
