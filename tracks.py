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

scope = 'user-follow-read user-library-read user-top-read playlist-read-private playlist-modify-public playlist-modify-private'
# scope = 'user-library-read'

def createPlaylistShort():
  topArtists = sp.current_user_top_artists(limit=50, offset=0, time_range='short_term')
  for artist in topArtists['items']:
    print artist['name']



if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
  start = datetime.now()
  sp = spotipy.Spotify(auth=token)

  createPlaylistShort()
else:
    print "Can't get token for", username



