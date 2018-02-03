import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from collections import OrderedDict
from datetime import datetime
from datetime import date

client_id = 'c5c313824e2d4d55af503c4fcde096ab'
client_secret = 'b9d0930596134732a657981a7bcaab69'
redirect_uri = 'http://localhost:8888/callback'

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-follow-read user-library-read'
# scope = 'user-library-read'



if len(sys.argv) > 2:
    username = sys.argv[1]
    checkingDays = sys.argv[2]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
  start = datetime.now()
  sp = spotipy.Spotify(auth=token)

  results = sp.current_user_followed_artists(limit=50)
  count = 0
  releases = {}
  followedArtists = set()
  while count < results['artists']['total']:
    results = results['artists']
    for item in results['items']:
      count+=1
      artist = item['name']
      lastid = item['id']
      followedArtists.add(artist)
    results = sp.current_user_followed_artists(limit=50,after=lastid)

  results = sp.new_releases(country='CA',limit=50)
  count = 0
  releases = {}
  # print results
  todayDate = date.today()
  maxDate = date.today()
  print todayDate

  print '''
  <!DOCTYPE html>
  <html>
  <body>
  <ul>
  '''

  while (todayDate - maxDate).days <= int(checkingDays):
    maxDate = date(2006, 1, 1)
    for item in results['albums']['items']:
      count+=1
      songName = item['name']
      artists = item['artists']
      albumID = item['id']
      url = item['external_urls']['spotify']
      artistName = artists[0]['name']
      album = sp.album(albumID)
      releaseDate = album['release_date']
      releaseDateSplit = releaseDate.split('-',2)
      print songName.encode("utf-8"), artistName.encode("utf-8")
      if len(releaseDateSplit) > 2:
        releaseDateTime = date(int(releaseDateSplit[0]),int(releaseDateSplit[1]),int(releaseDateSplit[2]))
        if releaseDateTime > maxDate:
          maxDate = releaseDateTime
      if artistName in followedArtists and (todayDate - releaseDateTime).days <= int(checkingDays):
        print '<li><a href="',url,'"">',releaseDate,songName.encode("utf-8"),'by',artistName.encode("utf-8"),'-',album['album_type'],'</a></li>'
      

    # print 'new songs', count
    # offset = 50 * (i+1)
    results = sp.new_releases(limit=50,offset=count)

  # print count
  print '''
  </ul>
  </html>
  </body>
  '''
  # print 'total time',datetime.now()-start
else:
  print "Can't get token for", username