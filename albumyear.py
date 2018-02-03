import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from collections import OrderedDict
from datetime import datetime

client_id = 'c5c313824e2d4d55af503c4fcde096ab'
client_secret = 'b9d0930596134732a657981a7bcaab69'
redirect_uri = 'http://localhost:8888/callback'

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-follow-read user-library-read'
# scope = 'user-library-read'



if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
f = open('templates/albumyear.html','w+')
if token:
  f.write('''
  <!DOCTYPE html>
  <html>
  <body>
  <ul>
  ''')
  start = datetime.now()
  sp = spotipy.Spotify(auth=token)

  # followedArtists = sp.current_user_followed_artists(limit=50)
  savedAlbums = sp.current_user_saved_albums(limit=50)
  # print savedAlbums
  # name = 'Gorillaz'
  # followedArtists = sp.search(q='artist:' + name, type='artist')
  count = 0
  releases = {}
  urls = {}
  images = {}
  total = savedAlbums['total']
  while count < total:
    
    albums = savedAlbums['items']
    for album in albums:
      count+=1
      album = album['album']
      albumType = album['album_type']
      if albumType == 'album':

        releases[album['name']+" - "+album['artists'][0]['name']] = album['release_date']
        urls[album['name']+" - "+album['artists'][0]['name']] = album['external_urls']['spotify']
        images[album['name']+" - "+album['artists'][0]['name']] = album['images'][-1]['url']
      
    savedAlbums = sp.current_user_saved_albums(limit=50,offset=count)



  ordered = OrderedDict(sorted(releases.items(), key=lambda t: t[1], reverse=True))
  # ordered = ordered[::-1]
  # ordered = reversed(ordered)
  for item in ordered:
    # print  ordered[item].encode("utf-8"), item.encode("utf-8")
    outtext = '<li><img src="'+ images[item].encode('utf-8', 'ignore') +'"><a href="'+urls[item].encode('utf-8', 'ignore')+'"">'+ordered[item].encode('utf-8', 'ignore')+' '+ item.encode('utf-8', 'ignore')+'</a></li>'
    outtext2 = ''

    f.write(outtext)

  f.write('</ul>')
  f.write('<h2>')
  f.write(str(count))
  f.write(' ')
  elapsedtime = datetime.now()-start
  totaltime = 'total time'+' '+str(elapsedtime)
  f.write(totaltime)
  f.write('</h2>')

  f.write('''
  </html>
  </body>
  ''')
else:
    print "Can't get token for", username