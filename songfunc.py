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


def allSongs(username):

  token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
  filename = 'templates/' + username + 'latest.html'
  f = open(filename,'w+')
  if token:
    f.write('''
    <!DOCTYPE html>
    <html>
    <body>
    <ul>
    ''')
    start = datetime.now()
    sp = spotipy.Spotify(auth=token)

    followedArtists = sp.current_user_followed_artists(limit=50)
    count = 0
    releases = {}
    urls = {}
    while count < followedArtists['artists']['total']:
      
      followedArtists = followedArtists['artists']

      for item in followedArtists['items']:
        # if count>1:
        #   count = 500
        #   break
        count+=1
        # print item
        artist = item['name']
        # uri = item['uri']
        lastid = item['id']
        # print 'ARTIST',artist.encode("utf-8")

        albums = sp.artist_albums(lastid)#,album_type='album')
        albums = albums['items']
        uniqueAlbumsDict = {}
        for album in albums:
          albumName = album['name']
          album = album['id']
          uniqueAlbumsDict[albumName] = album

        for album in uniqueAlbumsDict:
          album = uniqueAlbumsDict[album]
          album = sp.album(album)
          releases[album['name']+" - "+artist+" - "+album['album_type']] = album['release_date']
          urls[album['name']+" - "+artist+" - "+album['album_type']] = album['external_urls']['spotify']

      followedArtists = sp.current_user_followed_artists(limit=50,after=lastid)

    ordered = OrderedDict(sorted(releases.items(), key=lambda t: t[1], reverse=True))
    # ordered = ordered[::-1]
    # ordered = reversed(ordered)
    for item in ordered:
      # print  ordered[item].encode("utf-8"), item.encode("utf-8")
      outtext = '<li><a href="'+urls[item].encode('utf-8', 'ignore')+'"">'+ordered[item].encode('utf-8', 'ignore')+' '+ item.encode('utf-8', 'ignore')+'</a></li>'
      f.write(outtext)
      f.write('\n')

    f.write('</ul>')
    f.write('<h2>')
    f.write(str(count))
    f.write(' ')
    elapsedtime = datetime.now()-start
    totaltime = 'total time'+' '+str(elapsedtime)
    f.write(totaltime)
    f.write('</h2>')

    f.write('''
    <form action="/last" method="POST">
    <button name="listWorked" onclick="copyToLast()">List Worked</button>
    </body>
    </html>
    ''')
    f.close()
  else:
      print "Can't get token for", username