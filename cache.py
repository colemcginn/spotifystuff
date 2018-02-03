import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from collections import OrderedDict
from datetime import datetime
import csv
from unidecode import unidecode


client_id = 'c5c313824e2d4d55af503c4fcde096ab'
client_secret = 'b9d0930596134732a657981a7bcaab69'
redirect_uri = 'http://localhost:8888/callback'

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-follow-read user-library-read'

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def getCsv(id):
  with open('albums.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
      # print row
      if id == row['id']:
        return row
    return None

def saveToCsv(id, name, type, date, spotifyurl, imageurl):
  with open('albums.csv', 'a') as f: #wb, a is append
    writer = csv.writer(f)
    writer.writerow([id, name.encode('utf-8', 'ignore') , type, date, spotifyurl, imageurl])
    # append
    # writer.writerow({'id': id, 'name': name, 'type': type, 'date': date, 'spotifyurl': spotifyurl, 'imageurl': imageurl})


# scope = 'user-library-read'



if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
f = open('templates/allspeedtest.html','w+')
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
  # name = 'Gorillaz'
  # followedArtists = sp.search(q='artist:' + name, type='artist')
  count = 0
  releases = {}
  urls = {}
  images = {}

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
      uniqueAlbums = set()
      uniqueAlbumsDict = {}
      for album in albums:
        albumName = album['name']
        # print album
        va = 'various artists'
        if(album['artists'][0]['name'].lower()==va):
          # print album['artists'][0]['name']
          continue
        # print artist, album
        album = album['id']

        # uniqueAlbums.add(album)
        uniqueAlbumsDict[albumName] = album
        # print artist, albumName
      
      for albumName in uniqueAlbumsDict:
        # print album.encode('utf-8')
        # print uniqueAlbumsDict[album].encode('utf-8')
        albumID = uniqueAlbumsDict[albumName]
        info = getCsv(albumID)
        if info is not None:
          releases[remove_non_ascii(info['name'])+" - "+artist+" - "+info['type']] = info['date']
          urls[remove_non_ascii(info['name'])+" - "+artist+" - "+info['type']] = info['spotifyurl']
          images[remove_non_ascii(info['name'])+" - "+artist+" - "+info['type']] = info['imageurl']
        else: 
          album = sp.album(albumID)
          # print album['name'].encode('utf-8')
          releases[album['name']+" - "+artist+" - "+album['album_type']] = album['release_date']
          urls[album['name']+" - "+artist+" - "+album['album_type']] = album['external_urls']['spotify']
          images[album['name']+" - "+artist+" - "+album['album_type']] = album['images'][-1]['url']
          saveToCsv(albumID, album['name'], album['album_type'], album['release_date'], album['external_urls']['spotify'], album['images'][-1]['url'])



      # for album in uniqueAlbums:
      #   print album.encode('utf-8')
      #   album = sp.album(album)
      #   print album['name'].encode('utf-8')
      #   releases[album['name']+" - "+artist+" - "+album['album_type']] = album['release_date']
      #   urls[album['name']+" - "+artist+" - "+album['album_type']] = album['external_urls']['spotify']

    followedArtists = sp.current_user_followed_artists(limit=50,after=lastid)

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



