import xbmc
import xbmcgui
import xbmcplugin
import common
import re
import sys
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

class Main:

    def __init__( self ):
        #select from avaliable streams, then play the file
        self.play()
    
    def play( self):

        #getCID
        print common.args.url
        html=common.getHTML(common.args.url)
        if common.args.mode == 'HD_play':
            p=re.compile('swfObject.addVariable\("content_id", ([0-9]*)\);')
        else:
            p=re.compile('UserHistory.add_watched_history\((.+?)\)')
        cid=p.findall(html)[0]
        cid="http://r.hulu.com/videos?content_id="+cid
        #getPID
        html=common.getHTML(cid)
        cidSoup=BeautifulStoneSoup(html)
        pid=cidSoup.findAll('pid')[0].contents[0]
        #getSMIL
        smilURL = "http://releasegeo.hulu.com/content.select?pid=" + pid + "&mbr=true&format=smil"
        smilXML=common.getHTML(smilURL)
        smilSoup=BeautifulStoneSoup(smilXML)
        print smilSoup.prettify()
        #getRTMP
        video=smilSoup.findAll('video')
        streams=[]
        #label streams
        for stream in video:
            print 'stream--> '+stream['profile']
            if "480K" in stream['src'] or "480k" in stream['src'] or "_480" in stream['src']:
                streams.append([stream['profile'],stream['src']])
            elif "700K" in stream['src'] or "700k" in stream['src'] or "_700" in stream['src']:
                streams.append([stream['profile'],stream['src']])
            elif "H264" in stream['src'] or "h264" in stream['src'] or 'H_264' in stream['src']:
                streams.append([stream['profile'],stream['src']])
            elif "fake_" in stream['src']:
                pass #these seem to freeze xbmc, let's ignore them.
            else:
                streams.append(['unkown quality: '+stream['src'].split('/')[-1],stream['src']])
        #ask user for quality level
        quality=xbmcgui.Dialog().select('Please select a quality level:', [stream[0] for stream in streams])
        print quality
        if quality!=-1:
            #common.args.mode="TV_Episode"
            print "stream url"
            print streams[quality][1]
        #form proper streaming url
            rawurl=streams[quality][1].replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
            mainParts = rawurl.split("?")
            queryStringParts = mainParts[1].split("&")
            v9 = queryStringParts[0]
            v6 = queryStringParts[1]
            
            if "<break>" in queryStringParts[2]:
                breakParts = queryStringParts[2].split("<break>")
                v3 = breakParts[0];
                fileName = breakParts[1]
            else:
                v3 = queryStringParts[2]
                breakFilenameURL = mainParts[0].split("://");
                breakFilenamedir = breakFilenameURL[1].split("/");
                breakFilenames = breakFilenameURL[1].split(breakFilenamedir[1] + "/")
                fileName = breakFilenames[1]
                
            newQueryString = v9 + "&" + v6 + "&" + v3
            
            protocolSplit = rawurl.split("://")
            pathSplit = protocolSplit[1].split("/");
            serverPath = pathSplit[0] + "/" + pathSplit[1];

            server = pathSplit[0];
            appName = pathSplit[1];

            videoIdentIp = server
            
            protocol = "rtmp";
            port = "1935";
            newUrl =  protocol + "://" + videoIdentIp + ":" + port + "/" + appName + "?_fcs_vhost=" + server

            if newQueryString <> "":
                    newUrl += "&" + newQueryString

            print "item url -- > " + newUrl
            print "playPath -- > " + fileName
            xbmcgui.Dialog().ok('',common.args.mode)
            if common.args.mode == 'HD_play':
                SWFPlayer = 'http://www.hulu.com/playerHD.swf'
            else:
                SWFPlayer = 'http://www.hulu.com/player.swf'
                #SWFPlayer = 'http://www.hulu.com/playerembed.swf'
                    
        #define item
            item = xbmcgui.ListItem(common.args.name)
            item.setProperty("SWFPlayer", SWFPlayer)
            item.setProperty("PlayPath", fileName)
            item.setProperty("PageURL", common.args.url)

            #the following *almost* following works, and would be preferable
            #but as is, after the first video plays it crashes xbmc.
            playlist = xbmc.PlayList(1)
            playlist.clear()
            playlist.add(newUrl, item)
            play=xbmc.Player().play(playlist)
            xbmc.executebuiltin('XBMC.ActivateWindow(fullscreenvideo)')
            
            #ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=newUrl,listitem=item)
            #xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), updateListing=False,  succeeded=ok)
            
