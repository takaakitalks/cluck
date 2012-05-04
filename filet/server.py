# -*- coding: utf-8 -*-
import os

import urlparse
import urllib
from datetime import date

from google.appengine.api import urlfetch
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


# /filet/login
class LoginPageHandler(webapp.RequestHandler):
  _FB_APPID = 'your app id'  # Experimental
  _GAE_URI = 'your uri'
  _FB_SCOPE = 'your app\'s scope'
  _FB_APPSECRET = 'your app secret'

  def get(self):
    self.redirect('https://www.facebook.com/dialog/oauth?'
                  'client_id=%s&redirect_uri=%s&scope=%s'
                  % (LoginPageHandler._FB_APPID,
                     LoginPageHandler._GAE_URI,
                     LoginPageHandler._FB_SCOPE))

AT = 'AAAFTUgj0cuoBAIn2WWoPLxZBF0sVm3LPBl5mbSjfMMqLi3dE87uZAw8HTZAsKHRrULw4cw5hd7jYJOhoqlj1Up9NJnTC1n6jzkGVVUnEAZDZD'

_KEYWORDS = [ u'飲み',
              u'呑み',
              u'肉',
              u'飯',
              u'ディナー',
              u'美味しい',
              u'おいしい',
              u'ビール',
              ]

# /filet
class TopPageHandler(webapp.RequestHandler):
  def _RedirectToLoginPage(self):
    # self.response.out.write('need to login first: ')
    # self.response.out.write('<a href="%slogin">login</a><br>'
    #                         % LoginPageHandler._GAE_URI)
    # self.response.out.write('TODO: do login automatically')
    self.redirect(LoginPageHandler._GAE_URI + 'login')

  def get(self):
    # TODO: Handle OAuth error
    # http://YOUR_URL?error_reason=user_denied&error=access_denied&error_description=The+user+denied+your+request.

    # Check if code is provided.
    # http://YOUR_URL?code=A_CODE_GENERATED_BY_SERVER
    query = urlparse.urlparse(self.request.uri).query
    if not query:
      self._RedirectToLoginPage()
      return
    parsed_query = dict([keyval.split('=') for keyval in query.split('&')])
    if 'code' not in parsed_query:
      self._RedirectToLoginPage()
      return

    code = parsed_query['code']

    url = 'https://graph.facebook.com/oauth/access_token'
    query = { 'client_id': LoginPageHandler._FB_APPID,
              'redirect_uri': LoginPageHandler._GAE_URI,
              'client_secret': LoginPageHandler._FB_APPSECRET,
              'code': code }
    uri = url + '?' + urllib.urlencode(query)

    try:
      resp = urlfetch.fetch(uri, deadline=25)
      data = resp.content
    except urlfetch.DownloadError:
      self.response.out.write('<h1>Fetch Error</h1>')
      return

    data_parsed = dict([keyval.split('=') for keyval in data.split('&')])
    access_token = data_parsed['access_token']
    
    url = 'https://graph.facebook.com/me/home'
    query = { 'access_token': access_token,
              'limit': 100 }
    uri = url + '?' + urllib.urlencode(query)
    data = urlfetch.fetch(uri, deadline=25).content
    print data
    json = simplejson.loads(data)
    if 'data' not in json:
      self.response.out.write('json error')
      return

    if hasattr(self.request, 'cookies'):
      cookie = ''
      for k, v in self.request.cookies.iteritems():
        cookie += k + '=' + v + '<br>'
    else:
      cookie = 'NO COOKIES'

    result = []
    for feed in json['data']:
      if ('picture' not in feed) or ('message' not in feed):
        continue
      result.append(feed)
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(
      template.render(path, { 'result': simplejson.dumps(result),
                              'cookie': cookie }))
        
    # self.response.headers['Content-Type'] = 'application/json'
    # simplejson.dump(result, self.response.out, ensure_ascii=False)

#      for kw in _KEYWORDS:
#        if kw in feed['message']:
#      src = feed['picture'].replace('_q.jpg', '_n.jpg').replace('_s.jpg', '_n.jpg')
#      self.response.out.write('<img src="%s" height="200" alt="%s">'
#                              % (src, feed['message']))
#          break
    # self.response.out.write('<div>')
    # self.response.out.write(simplejson.dumps(json))
    # self.response.out.write('</div>')
#    self.response.out.write('</body></html>')

        
    
application = webapp.WSGIApplication(
  [('/filet/', TopPageHandler),
   ('/filet/index.html', TopPageHandler),
   ('/filet/login', LoginPageHandler),
   ],
  debug=True)


def main():
  run_wsgi_app(application)


if __name__ == "__main__":
  main()
