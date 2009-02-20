import xbmcplugin
import xbmcgui
import xbmc

import common

import sys
import re

from BeautifulSoup import MinimalSoup, BeautifulStoneSoup

class Main:

    def __init__( self ):
        if common.args.mode == 'TV' and common.settings['flat_tv_cats']:
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            self.addShowsList()
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
        elif common.args.mode == 'TV_List':
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            self.addShowsList()
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
        elif common.args.mode == 'TV_Seasons':
            self.addSeasonList()
        elif common.args.mode == 'TV_Episodes':
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            self.addEpisodeList()
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
        elif common.args.mode == 'TV_Clips':
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            self.addClipsList()
        else:
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            self.addCategories()
            #ADD 'ALL SHOWS' to Main Category List
            if common.args.mode == "TV":
                #space in string ' All Shows' ensures it is at top of sorted list
                common.addDirectory(' '+xbmc.getLocalizedString(30070), common.args.url, 'TV_List')
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
            elif common.args.mode.startswith("TV_cat"):
                self.addShowsList() #if we're in a category view, add videos that match the selected category
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
                if common.args.mode=="TV_cat_sub2":
                    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ]), updateListing=True ) #if we're going into subcategories, don't add to heirchy
                else:
                    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))



    def addCategories( self ):
        html=common.getHTML(common.args.url)
        p=re.compile('href="http://www.hulu.com/browse/alphabetical/.+?(\?channel=.+?)">[^<]')
        match=p.findall(html)
        del html
        for item in match:
            name=item.split("=")[-1]
            if name!='all':
                if common.args.mode == "TV_cat_sub":#SubCategories _ don't add to dir heirachy
                    item=item.split('&')[-1]
                    name = "(Subcategory) "+name.replace("+"," ").title()
                    common.addDirectory(name, common.args.url+"&"+item, "TV_cat_sub2")
                elif "&" in item.split("=")[-2]:#SubCategories
                    item=item.split('&')[-1]
                    name = "(Subcategory) "+name.replace("+"," ").title()
                    common.addDirectory(name, common.args.url+"&"+item, "TV_cat_sub")
                elif common.args.mode!='TV_categories':#RegularCategory
                    name= name.replace("+"," ").title()
                    common.addDirectory(name, common.args.url+item, "TV_cat")
        

    def addShowsList( self ):
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)

        html=common.getHTML(common.args.url)
        tree=MinimalSoup(html)
        shows=tree.findAll('a', attrs={"class":"show-thumb info_hover"})
        del html
        del tree
        # with clips
        for show in shows:
            name  = show.contents[0].replace('&quot;','"').replace('&amp;','&')
            url   = show['href']
            tmp   = show['href'].split('/')[3]
            art   = "http://assets.hulu.com/shows/key_art_"+tmp.replace('-','_')+".jpg"
            #thumb = "http://assets.hulu.com/shows/show_thumbnail_"+tmp.replace('-','_')+".jpg"
            #icon  = "http://assets.hulu.com/shows/show_thumbnail_"+tmp.replace('-','_')+".jpg"
            #Use higher res fanart (key_art) instead of lower res thumbs & icons
            thumb = art
            icon = art
            if common.settings['get_show_plot'] == True:
                json = common.getHTML("http://www.hulu.com/shows/info/"+tmp)
                try:
                    #this needs better regex, or maybe some sort of json parser
                    p = re.compile('description: "(.+?)"[,}]')
                    match = p.findall(json)
                    plot = match[0].replace('\\','')
                except:
                    plot=xbmc.getLocalizedString(30090)
                try:
                    p = re.compile('channel: "(.+?)"[,}]')
                    match = p.findall(json)
                    genre = match[0]
                except:
                    genre=xbmc.getLocalizedString(30090)
                #hopefully deleting this will help with xbox memory problems
                del json
            else:
                plot=genre=xbmc.getLocalizedString(30090)
            try:
                if show.parent['class'] != "full-episode-icon":
                    name += ' '+xbmc.getLocalizedString(30091)
                    genre += ' '+xbmc.getLocalizedString(30091)
                elif common.args.url != common.BASE_TV_URL:
                    common.addDirectory(name, url, "TV_Seasons", art, icon, art, plot, genre)
            except:
                name += ' '+xbmc.getLocalizedString(30091)
                genre += ' '+xbmc.getLocalizedString(30091)
                if common.settings['only_full_episodes'] == False:
                    common.addDirectory(name, url, "TV_Seasons", art, icon, art, plot, genre)
        
        #if we're doing both clips & full episodes, we need to run through the function again.
        if common.args.url == common.BASE_TV_URL :
            common.args.url = common.BASE_FULLTV_URL
            self.addShowsList()
        
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))



    def addSeasonList( self ):
        tree=MinimalSoup(common.getHTML(common.args.url))  
        seasons=tree.findAll('td', attrs={"class":re.compile('^vex')})
        #flatten seasons by settings
        if common.settings['flat_season'] == 1 or (len(seasons) == 1 and common.settings['flat_season'] == 0):
            common.args.mode='TV_Episodes'
            seasonNums=[]
            for season in seasons:
                common.args.name = season.contents[0]
                seasonNums.append(season.contents[0])
                self.addEpisodeList( )
            #add clips folder
            rss=tree.findAll('a', attrs={'class':'rss-link'})
            clipRSS = None
            for feed in rss:
                if feed['href'].split('/')[-1]=='clips':
                    clipRSS = feed['href']
            if clipRSS != None:
                common.addDirectory(xbmc.getLocalizedString(30095), clipRSS, "TV_Clips")
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))

        else:
            #add one folder for each season
            for season in seasons:
                name=season.contents[0]
                p=re.compile('&quot;(http://.+?)&quot;')
                url=p.findall(season['onclick'])
                url=url[0].replace('&amp;','&')
                ok=common.addDirectory(name, common.args.url, "TV_Episodes")
            #add clips folder
            rss=tree.findAll('a', attrs={'class':'rss-link'})
            for feed in rss:
                if feed['href'].split('/')[-1]=='clips': clipRSS = feed['href']
            common.addDirectory(xbmc.getLocalizedString(30095), clipRSS, "TV_Clips")
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))


    def addEpisodeList( self ):
        #initialize variables
        p=re.compile('(\d+)')#gets last number from "season ##"
        currentSeason=p.findall(common.args.name)[0]
        epRSS=None
        #parse html tree
        tree=MinimalSoup(common.getHTML(common.args.url))
        rss=tree.findAll('a', attrs={'class':'rss-link'})
        for feed in rss:
            if feed['href'].split('/')[-1]=='episodes':
                tree=BeautifulStoneSoup(common.getHTML(feed['href']))
                items=tree.findAll('item')
                for episode in items:
                    p=re.compile('\(s([0-9]*).+?\|.+?e([0-9]*)\)')
                    match=p.findall(episode.title.contents[0])[0]
                    seasonNum  = match[0]
                    episodeNum = match[1]
                    if seasonNum == currentSeason:
                        #add this episode to list
                        name    = episode.title.contents[0].split('(')[0]
                        if len(seasonNum)<2:seasonNum='0'+seasonNum
                        if len(episodeNum)<2:episodeNum='0'+episodeNum
                        name = 's'+seasonNum+'e'+episodeNum+' '+name
                        url = episode.link.contents[0].split('#')[0]
                        try:
                            thumb = episode.findAll('media:thumbnail')[0]['url']
                        except:
                            thumb = ''
                        try:
                            airdate = episode.pubdate.contents[0]
                        except:
                            airdate = ''
                        try:
                            p=re.compile('<p>(.+?)</p>.+?Added: ')
                            plot =''.join(p.findall(str(episode.findAll('description'))))
                            try:
                                p=re.compile('Duration: (.+?)\n')
                                duration=p.findall(plot)[0].split(':')
                                duration=(int(duration[0])*60)+int(duration[1])
                            except:
                                duration=1
                        except:
                            plot = ''
                        common.addDirectory(name,url,'TV_play', thumb, thumb, common.args.fanart, plot, 'genre')



    def addClipsList( self ):
        name = common.args.name.replace(xbmc.getLocalizedString(30091),'')
        tree=BeautifulStoneSoup(common.getHTML(common.args.url))
        clips = tree.findAll('item')
        print clips
        for clip in clips:
            name = clip.title.contents[0].split(': ')[1:][0]
            url  = clip.link.contents[0].split('#')[0]
            try:
                thumb = clip.findAll('media:thumbnail')[0]['url']
            except:
                thumb = common.args.fanart
            try:
                p=re.compile('<p>(.+?)</p>.+?Added: ')
                plot =''.join(p.findall(str(clip.findAll('description')))).replace('<br />','\n').replace('Added: ','\n\nAdded: ')
            except:
                plot = ''
            common.addDirectory(name, url, 'TV_Clips_play', thumb, thumb, common.args.fanart, plot, common.args.genre )
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
