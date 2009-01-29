import xbmcplugin
import xbmcgui
import xbmc
import sys
import re
import common
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

class Main:

    def __init__( self ):
        if common.args.mode == 'Movie' and common.settings['flat_movie_cats']:
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            self.addMoviesList()
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
        elif common.args.mode == 'Movie_List':
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            self.addMoviesList()
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
        elif common.args.mode == 'Movie_Items':
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            self.addVideosList()
            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
        elif common.args.mode == 'Movie_Clips':
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            self.addClipsList()
            #it is better to end the directory list in the function
            #it looks fuck-tarded if no clips are found and we end it here.
        else:
            self.addCategories()
            #ADD 'ALL SHOWS' to Main Category
            if common.args.mode == "Movie":
                #space in string ' All Movies' ensures it is at top of sorted list
                common.addDirectory(' All Movies', common.args.url, 'Movie_List')
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ))
            elif common.args.mode.startswith("Movie_cat"):
                self.addMoviesList() #if we're in a category view, add videos that match the selected category
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
                if common.args.mode=="Movie_cat_sub2":
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
                if common.args.mode == "Movie_cat_sub":#SubCategories _ don't add to dir heirachy
                    item=item.split('&')[-1]
                    name = "(Subcategory) "+name.replace("+"," ").title()
                    common.addDirectory(name, common.args.url+"&"+item, "Movie_cat_sub2")
                elif "&" in item.split("=")[-2]:#SubCategories
                    item=item.split('&')[-1]
                    name = "(Subcategory) "+name.replace("+"," ").title()
                    common.addDirectory(name, common.args.url+"&"+item, "Movie_cat_sub")
                elif common.args.mode!='TV_categories':#RegularCategory
                    name= name.replace("+"," ").title()
                    common.addDirectory(name, common.args.url+item, "Movie_cat")



    def addMoviesList( self ):
        
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)

        html=common.getHTML(common.args.url)
        tree=BeautifulSoup(html)
        movies=tree.findAll('a', attrs={"class":"show-thumb info_hover"})
        del html
        del tree
        # with clips
        for movie in movies:
            name  = movie.contents[0].replace('&quot;','"').replace('&amp;','&')
            url   = movie['href']
            tmp   = movie['href'].split('/')[3]
            thumb = "http://assets.hulu.com/shows/show_thumbnail_"+tmp.replace('-','_')+".jpg"
            icon  = "http://assets.hulu.com/shows/show_thumbnail_"+tmp.replace('-','_')+".jpg"
            art   = "http://assets.hulu.com/shows/key_art_"+tmp.replace('-','_')+".jpg"
            if common.settings['get_movie_plot'] == True:
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
                if movie.parent['class'] != "full-movie-icon":
                    name += ' '+xbmc.getLocalizedString(30091)
                    genre = xbmc.getLocalizedString(30091)+' '+genre
                elif common.args.url != common.BASE_MOVIE_URL:
                    common.addDirectory(name, url, "Movie_Items", art, icon, art, plot, genre)
            except:
                name += ' '+xbmc.getLocalizedString(30091)
                genre += ' '+xbmc.getLocalizedString(30091)
                if common.settings['only_full_movies'] == False:
                    common.addDirectory(name, url, "Movie_Items", art, icon, art, plot, genre)
                    
        #if we're doing both clips & full movies, we need to run through the function again.
        if common.args.url == common.BASE_MOVIE_URL :
            common.args.url = common.BASE_FULLMOVIE_URL
            self.addMoviesList()

    def addVideosList( self ):
        if '(clips only)' in common.args.name:
            self.addClipsList()
        else:
            tree=BeautifulSoup(common.getHTML(common.args.url))
            link=tree.find('a', attrs={"class":'info_hover'})
            movieUrl = link['href']
            common.addDirectory(common.args.name, movieUrl, "Movie_play", common.args.fanart, common.args.fanart, common.args.fanart, common.args.plot, common.args.genre)
            common.addDirectory(xbmc.getLocalizedString(30092)+' '+common.args.name.replace(xbmc.getLocalizedString(30091),''), common.args.url, 'Movie_Clips', common.args.fanart,common.args.fanart,common.args.fanart)

    def addClipsList( self ):
        tree=BeautifulSoup(common.getHTML(common.args.url))
        rssLink = tree.find('a', attrs={'class':'rss-link'})
        if rssLink == None:
            xbmcgui.Dialog().ok(xbmc.getLocalizedString(30093),xbmc.getLocalizedString(30094)+' '+common.args.name)
        else:
            name = common.args.name.replace(xbmc.getLocalizedString(30090),'')
            tree=BeautifulStoneSoup(common.getHTML(rssLink['href']))
            clips = tree.findAll('item')
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
