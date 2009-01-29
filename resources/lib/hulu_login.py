import urllib,urllib2,cookielib,re,os.path

login_url   = 'https://secure.hulu.com/account/authenticate'
profile_url = 'http://www.hulu.com/users/profile/5129429'

username = "rwparris2"        #put your email address here
password = "let'swatchhulu"   #put your password here
data =urllib.urlencode({"login":username,"password":password})

COOKIEFILE='cookies.lwp'
cj = cookielib.LWPCookieJar()
if os.path.isfile(COOKIEFILE):
    cj.load(COOKIEFILE)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

opener.addheaders = [('Referer', 'http://hulu.com'),
                     ('Content-Type', 'application/x-www-form-urlencoded'),
                     ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]

if not os.path.isfile(COOKIEFILE):
    usock = opener.open(login_url, data)
    response = usock.read()
    usock.close()

usock=opener.open(profile_url,data)
link = usock.read()
usock.close()
cj.save(COOKIEFILE)


p=re.compile('('+username+')')
match = p.findall(link)


print "login_url response (we want 'ok=1'): "
print response


print 'These are the cookies we have received:'
for index, cookie in enumerate(cj):

    print index, '  :  ', cookie


if len(match)>1:
    for name in match:
        print "login successful. proof: "
        print name
else:
    print "login not successful. Name not found"
    print "type print link to see the html returned"

#on script exit, we need to delete the cookie, they don't last long

os.remove(COOKIEFILE)
