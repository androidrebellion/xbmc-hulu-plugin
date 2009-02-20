"""
        Plugin for streaming media from Hulu.com
"""
#main imports
import sys
import os
import urllib

import resources.lib.common as common

#plugin constants
__plugin__ = "Let's Watch Hulu"
__author__ = "rwparris2"
__url__ = "http://code.google.com/p/rwparris2-xbmc-plugin/"
__svn_url__ = "http://rwparris2-xbmc-plugins.googlecode.com/svn/trunk/plugins/video/Lets%20Watch%20Hulu/"
__credits__ = "zoltar12 for the original hulu plugin, BlueCop for h264 & flv url changes"
__version__ = "1.0"


#temp#
print "\n\n\n\n\n\n\nstart of HULU plugin\n\n\n\n\n\n"
try:print "HULU--> common.args.mode -- > " + common.args.mode
except: print "HULU--> no mode has been defined"
#end temp#


def modes( ):
        if sys.argv[2]=='':
            import resources.lib._home as home
            home.Main()
        elif common.args.mode.endswith('_play'):
            import resources.lib.stream_hulu as stream_media
            stream_media.Main()
        elif common.args.mode.startswith('TV'):
            import resources.lib._tv as tv
            tv.Main()
        elif common.args.mode.startswith('Movie'):
            import resources.lib._movie as movie
            movie.Main()
        elif common.args.mode.startswith('RSS'):
            import resources.lib._rss as rss
            rss.Main()
        elif common.args.mode.startswith('HD'):
            import resources.lib._hd as hd
            hd.Main()
        else:
            import xbmcgui
            xbmcgui.Dialog().ok('common.args.mode',common.args.mode)
            print "unknown mode--> "+common.args.mode



if ( __name__ == "__main__" ):
        #common.login ( )
        modes ( )
        #os.remove(common.COOKIEFILE)
        
sys.modules.clear()
